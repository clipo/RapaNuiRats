import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint


class RapaNuiEcosystem:
    """
    Historical ecological simulation of Rattus exulans introduction and palm forest collapse
    on Rapa Nui (1200-1722 CE).

    This model incorporates:
    - Rat population dynamics with realistic average growth and seasonal carrying capacity
    - Seasonal palm nut availability (3 months/year) affecting rat populations
    - Realistic rat carrying capacity: 0.5-4.0 rats per mature palm (seasonal variation)
    - Human population growth from 20 to 3000 individuals over 500 years
    - Palm forest decline due to seed predation and human land clearing
    - Age-dependent palm mortality modeling Jubaea chilensis lifespan (up to 500 years)
    - Senescence effects as palm populations age without recruitment
    - 70-year palm regeneration cycle
    - Comparative analysis capability: Rats-only vs Rats+Humans scenarios
    - Historical timeline matching archaeological evidence
    """

    def __init__(self):
        # Rat population parameters (Rattus exulans) - realistic average reproduction
        # Calculation: 2.5 litters/year × 2.5 offspring/litter = 6.25 offspring per female per year
        # But only ~50% are female and ~80% successfully breed = 6.25 × 0.5 × 0.8 = 2.5 population growth rate
        self.rat_intrinsic_growth = 2.5  # average reproductive rate accounting for sex ratio and breeding success
        self.rat_natural_mortality = 1.0  # 1 year lifespan

        # Realistic seasonal carrying capacity based on palm nut availability
        self.rat_base_carrying_capacity_per_tree = 0.5  # rats sustainable on alternative foods year-round
        self.rat_peak_carrying_capacity_per_tree = 4.0  # maximum during 3-month nut season
        self.nut_season_duration = 0.25  # fraction of year nuts are available (3 months)
        self.rat_minimum_viable_population = 50  # minimum population for persistence

        # Palm tree parameters - including age-dependent mortality
        self.palm_maturation_time = 70  # years to reach reproductive maturity
        self.palm_max_lifespan = 500  # maximum lifespan for Jubaea chilensis
        self.palm_natural_mortality_young = 0.01  # natural annual mortality rate for young palms
        self.palm_natural_mortality_mature = 0.005  # lower mortality for prime mature palms
        self.palm_senescence_age = 400  # age at which senescence mortality increases
        self.palm_max_reproduction = 0.025  # maximum annual reproduction rate
        self.seed_predation_efficiency = 0.95  # fraction of seeds consumed by rats
        self.palm_refugia_effect = 0.0001  # fraction of palms in protected/inaccessible areas

        # Human population parameters
        self.initial_humans = 20  # founding population ca. 1200 CE
        self.human_carrying_capacity = 3000  # maximum sustainable population
        self.human_intrinsic_growth = 0.025  # initial birth rate (2.5% per year)

        # Human impact parameters
        self.clearing_per_person_per_year = 5.0  # palms cleared per person annually (increased for larger forest)
        self.agricultural_intensification = 1.003  # increasing efficiency over time
        self.clearing_efficiency_decline = 0.9995  # decreasing efficiency as accessible palms decline
        self.enable_human_clearing = True  # Flag to enable/disable human forest clearing

        # Rat harvesting for protein
        self.rat_harvest_rate = 0.25  # fraction of rat population humans can harvest annually

        # Initial conditions (ca. 1200 CE) - 15 million palm forest
        self.initial_rats = 2  # introduced breeding pair
        self.initial_mature_palms = 9000000  # mature reproductive palms (60% of total)
        self.initial_young_palms = 6000000  # immature palms (40% of total)
        self.initial_mature_age = 150  # average age of initial mature palm population

    def human_population(self, t):
        """
        Calculate human population at time t using logistic growth model.

        Logistic growth: P(t) = K / (1 + ((K-P0)/P0) * exp(-rt))
        where K = carrying capacity, P0 = initial population, r = intrinsic growth rate
        """
        K = self.human_carrying_capacity
        P0 = self.initial_humans
        r = self.human_intrinsic_growth

        return K / (1 + ((K - P0) / P0) * np.exp(-r * t))

    def seasonal_rat_carrying_capacity(self, t, mature_palms):
        """
        Calculate seasonal rat carrying capacity based on palm nut availability.
        Palm nuts are available for ~3 months per year (0.25 of year).
        """
        # Create seasonal cycle (peak in months 2-5 of each year, roughly)
        seasonal_factor = 0.5 * (1 + np.sin(2 * np.pi * t - np.pi / 2))  # Varies 0 to 1

        # Carrying capacity varies from base (alternative foods) to peak (during nut season)
        carrying_capacity_per_tree = (self.rat_base_carrying_capacity_per_tree +
                                      seasonal_factor *
                                      (self.rat_peak_carrying_capacity_per_tree -
                                       self.rat_base_carrying_capacity_per_tree))

        return max(self.rat_minimum_viable_population,
                   mature_palms * carrying_capacity_per_tree)

    def ecosystem_dynamics(self, state, t):
        """
        Differential equations governing the ecosystem dynamics.

        State vector: [rats, mature_palms, young_palms, mature_palm_avg_age]
        """
        rats, mature_palms, young_palms, mature_avg_age = np.maximum(state, 0)  # Prevent negative populations
        total_palms = mature_palms + young_palms

        # Current human population
        humans = self.human_population(t)

        # Calculate age-dependent mortality for mature palms
        if mature_avg_age < self.palm_senescence_age:
            mature_mortality = self.palm_natural_mortality_mature
        else:
            # Exponentially increasing mortality after senescence age
            senescence_factor = (mature_avg_age - self.palm_senescence_age) / 100
            mature_mortality = self.palm_natural_mortality_mature * (1 + 2 * senescence_factor)

        # Mortality increases dramatically as trees approach maximum lifespan
        if mature_avg_age > (self.palm_max_lifespan * 0.8):  # 80% of max lifespan
            lifespan_factor = (mature_avg_age - self.palm_max_lifespan * 0.8) / (self.palm_max_lifespan * 0.2)
            mature_mortality = mature_mortality * (1 + 5 * lifespan_factor)

        # Cap mortality at reasonable maximum
        mature_mortality = min(mature_mortality, 0.1)  # Maximum 10% annual mortality

        # Calculate seasonal rat carrying capacity based on palm nut availability
        rat_carrying_capacity = self.seasonal_rat_carrying_capacity(t, mature_palms)

        # Human rat harvesting (increasingly important protein source over time)
        if self.enable_human_clearing:
            rat_harvest_pressure = humans * self.rat_harvest_rate * min(1.0, t / 150)
            rat_harvest = min(rat_harvest_pressure, rats * 0.4)  # max 40% harvest rate
        else:
            rat_harvest = 0  # No human harvesting if no human impact

        # Rat population dynamics with birth, natural death, and harvest
        if rats > self.rat_minimum_viable_population:
            rat_growth = (rats * self.rat_intrinsic_growth *
                          (1 - rats / rat_carrying_capacity) -
                          rats * self.rat_natural_mortality -
                          rat_harvest)
        else:
            # Small population growth with Allee effects
            rat_growth = (rats * self.rat_intrinsic_growth * 0.5 *
                          (1 - rats / rat_carrying_capacity) -
                          rats * self.rat_natural_mortality -
                          rat_harvest * (
                              0.1 if self.enable_human_clearing else 0))  # reduced/no harvest pressure on small populations

        # Human clearing pressure (conditionally applied)
        if self.enable_human_clearing:
            # Clearing becomes less efficient as accessible palms decline
            clearing_efficiency = (self.clearing_efficiency_decline ** t) * \
                                  (total_palms / (self.initial_mature_palms + self.initial_young_palms))
            clearing_rate = (humans * self.clearing_per_person_per_year *
                             (self.agricultural_intensification ** t) * clearing_efficiency)
        else:
            clearing_rate = 0  # No human clearing

        # Mature palm dynamics with age-dependent mortality
        # Natural mortality + human clearing (reduced by refugia effect)
        accessible_mature = mature_palms * (1 - self.palm_refugia_effect)
        mature_palm_clearing = min(clearing_rate * 0.75, accessible_mature * 0.18) if self.enable_human_clearing else 0
        mature_palm_loss = mature_palms * mature_mortality + mature_palm_clearing

        # Recruitment from young palms (70-year delay approximated)
        mature_palm_recruitment = young_palms / self.palm_maturation_time
        mature_palm_change = mature_palm_recruitment - mature_palm_loss

        # Average age dynamics for mature palms
        if mature_palms > 100:  # Avoid division by zero
            # Age increases by 1 year per year, modified by recruitment and mortality
            age_increase = 1.0  # All trees age 1 year per year
            # New recruits are 70 years old when they mature
            recruit_age_effect = (mature_palm_recruitment / mature_palms) * (70 - mature_avg_age)
            # Deaths remove trees at current average age (no age effect on average)
            avg_age_change = age_increase + recruit_age_effect
        else:
            avg_age_change = 0

        # Young palm dynamics
        # Potential reproduction from mature palms (refugia palms reproduce at higher rate)
        refugia_palms = mature_palms * self.palm_refugia_effect
        accessible_palms = mature_palms * (1 - self.palm_refugia_effect)

        refugia_reproduction = refugia_palms * self.palm_max_reproduction * 1.1
        accessible_reproduction = accessible_palms * self.palm_max_reproduction
        potential_reproduction = refugia_reproduction + accessible_reproduction

        # Seed predation by rats (functional response with saturation)
        rat_density_effect = rats / (rats + 3000)  # Half-saturation at 3000 rats
        predation_pressure = self.seed_predation_efficiency * rat_density_effect
        # Refugia seeds have lower predation pressure
        refugia_survival = refugia_reproduction * (1 - predation_pressure * 0.4)
        accessible_survival = accessible_reproduction * (1 - predation_pressure)
        actual_reproduction = refugia_survival + accessible_survival

        # Young palm mortality, maturation, and human clearing
        accessible_young = young_palms * (1 - self.palm_refugia_effect)
        young_palm_clearing = min(clearing_rate * 0.25, accessible_young * 0.12) if self.enable_human_clearing else 0
        young_palm_loss = (young_palms * self.palm_natural_mortality_young +
                           young_palms / self.palm_maturation_time +
                           young_palm_clearing)
        young_palm_change = actual_reproduction - young_palm_loss

        return [rat_growth, mature_palm_change, young_palm_change, avg_age_change]

    def run_simulation(self, years=522):
        """
        Run the ecosystem simulation from 1200 CE to European contact (1722 CE).
        Uses higher time resolution to capture seasonal dynamics.
        """
        t = np.linspace(0, years, years * 8)  # Monthly time steps for seasonal resolution
        initial_state = [self.initial_rats, self.initial_mature_palms,
                         self.initial_young_palms, self.initial_mature_age]

        solution = odeint(self.ecosystem_dynamics, initial_state, t)

        # Extract results
        rats = solution[:, 0]
        mature_palms = solution[:, 1]
        young_palms = solution[:, 2]
        mature_avg_age = solution[:, 3]
        total_palms = mature_palms + young_palms

        # Calculate human population over time
        humans = [self.human_population(time) for time in t]

        return t, rats, mature_palms, young_palms, total_palms, humans, mature_avg_age

    def plot_results(self, t, rats, mature_palms, young_palms, total_palms, humans, mature_avg_age, scenario_label="rats_humans"):
        """
        Create comprehensive visualization of simulation results and save as separate files.
        
        Parameters:
        scenario_label: String label for the scenario ("rats_humans" or "rats_only")
        """
        # Convert time to CE dates for historical context
        dates = 1200 + t

        # Set up high-resolution plotting parameters
        plt.rcParams['figure.dpi'] = 600
        plt.rcParams['savefig.dpi'] = 600
        plt.rcParams['savefig.bbox'] = 'tight'

        # Figure 1: Palm forest decline
        fig1, ax1 = plt.subplots(1, 1, figsize=(10, 8))
        ax1.plot(dates, total_palms / 1000, 'g-', linewidth=2.5, label='Total Palms')
        ax1.plot(dates, mature_palms / 1000, 'g--', linewidth=2, label='Mature Palms', alpha=0.7)
        ax1.set_xlabel('Year (CE)')
        ax1.set_ylabel('Palm Trees (thousands)')
        ax1.set_title('Palm Forest Decline on Rapa Nui (1200-1722 CE)')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        ax1.set_ylim(0, max(total_palms / 1000) * 1.1)

        # Save Figure 1
        fig1.savefig(f'../figures/{scenario_label}_palm_decline.pdf', format='pdf', dpi=600, bbox_inches='tight')
        fig1.savefig(f'../figures/{scenario_label}_palm_decline.png', format='png', dpi=600, bbox_inches='tight')

        # Figure 2: Rat population dynamics
        fig2, ax2 = plt.subplots(1, 1, figsize=(10, 8))
        ax2.plot(dates, rats / 1000, 'r-', linewidth=2.5, label='Rat Population (thousands)')
        ax2.set_xlabel('Year (CE)')
        ax2.set_ylabel('Rat Population (thousands)')
        ax2.set_title('Rattus exulans Population Growth')
        ax2.grid(True, alpha=0.3)
        ax2.legend()

        # Save Figure 2
        fig2.savefig(f'../figures/{scenario_label}_rat_population.pdf', format='pdf', dpi=600, bbox_inches='tight')
        fig2.savefig(f'../figures/{scenario_label}_rat_population.png', format='png', dpi=600, bbox_inches='tight')

        # Figure 3: Human population growth
        fig3, ax3 = plt.subplots(1, 1, figsize=(10, 8))
        ax3.plot(dates, humans, 'b-', linewidth=2.5, label='Human Population')
        ax3.set_xlabel('Year (CE)')
        ax3.set_ylabel('Human Population')
        ax3.set_title('Human Population Growth')
        ax3.grid(True, alpha=0.3)
        ax3.legend()

        # Save Figure 3
        fig3.savefig(f'../figures/{scenario_label}_human_population.pdf', format='pdf', dpi=600, bbox_inches='tight')
        fig3.savefig(f'../figures/{scenario_label}_human_population.png', format='png', dpi=600, bbox_inches='tight')

        # Figure 4: Comparative population dynamics (normalized)
        fig4, ax4 = plt.subplots(1, 1, figsize=(10, 8))
        ax4.plot(dates, total_palms / np.max(total_palms), 'g-', linewidth=2.5,
                 label='Palm Forest (normalized)', alpha=0.8)
        ax4.plot(dates, rats / np.max(rats), 'r-', linewidth=2.5,
                 label='Rats (normalized)', alpha=0.8)
        ax4.plot(dates, humans / np.max(humans), 'b-', linewidth=2.5,
                 label='Humans (normalized)', alpha=0.8)
        ax4.set_xlabel('Year (CE)')
        ax4.set_ylabel('Relative Population Size')
        ax4.set_title('Comparative Population Dynamics (Normalized)')
        ax4.grid(True, alpha=0.3)
        ax4.legend()
        ax4.set_ylim(0, 1.1)

        # Save Figure 4
        fig4.savefig(f'../figures/{scenario_label}_comparative_dynamics.pdf', format='pdf', dpi=600, bbox_inches='tight')
        fig4.savefig(f'../figures/{scenario_label}_comparative_dynamics.png', format='png', dpi=600, bbox_inches='tight')

        # Figure 5: Rats and Trees (new figure without humans)
        fig5, ax5 = plt.subplots(1, 1, figsize=(10, 8))

        # Plot palms on left y-axis
        ax5.plot(dates, total_palms / 1000, 'g-', linewidth=3, label='Total Palm Trees')
        ax5.plot(dates, mature_palms / 1000, 'g--', linewidth=2, label='Mature Palm Trees', alpha=0.7)
        ax5.set_xlabel('Year (CE)')
        ax5.set_ylabel('Palm Trees (thousands)', color='green')
        ax5.tick_params(axis='y', labelcolor='green')

        # Plot rats on right y-axis
        ax5_rat = ax5.twinx()
        ax5_rat.plot(dates, rats / 1000, 'r-', linewidth=3, label='Rat Population', alpha=0.8)
        ax5_rat.set_ylabel('Rat Population (thousands)', color='red')
        ax5_rat.tick_params(axis='y', labelcolor='red')

        ax5.set_title('Ecological Collapse: Rat Population vs Palm Forest Decline (1200-1722 CE)')
        ax5.grid(True, alpha=0.3)

        # Combine legends
        lines1, labels1 = ax5.get_legend_handles_labels()
        lines2, labels2 = ax5_rat.get_legend_handles_labels()
        ax5.legend(lines1 + lines2, labels1 + labels2, loc='center right')

        # Save Figure 5
        fig5.savefig(f'../figures/{scenario_label}_rats_vs_trees.pdf', format='pdf', dpi=600, bbox_inches='tight')
        fig5.savefig(f'../figures/{scenario_label}_rats_vs_trees.png', format='png', dpi=600, bbox_inches='tight')

        # Figure 6: Palm Age Dynamics (new figure showing aging effect)
        fig6, ax6 = plt.subplots(1, 1, figsize=(10, 8))

        # Plot mature palm average age and population on dual axes
        ax6.plot(dates, mature_avg_age, 'purple', linewidth=3, label='Average Age of Mature Palms')
        ax6.axhline(y=self.palm_senescence_age, color='orange', linestyle='--',
                    linewidth=2, label=f'Senescence Age ({self.palm_senescence_age} years)')
        ax6.axhline(y=self.palm_max_lifespan, color='red', linestyle='--',
                    linewidth=2, label=f'Maximum Lifespan ({self.palm_max_lifespan} years)')
        ax6.set_xlabel('Year (CE)')
        ax6.set_ylabel('Palm Age (years)', color='purple')
        ax6.tick_params(axis='y', labelcolor='purple')

        # Plot mature palm population on right y-axis
        ax6_pop = ax6.twinx()
        ax6_pop.plot(dates, mature_palms / 1000, 'g-', linewidth=2, label='Mature Palm Population', alpha=0.7)
        ax6_pop.set_ylabel('Mature Palm Population (thousands)', color='green')
        ax6_pop.tick_params(axis='y', labelcolor='green')

        ax6.set_title('Palm Forest Aging and Senescence: Average Age vs Population Decline')
        ax6.grid(True, alpha=0.3)

        # Combine legends
        lines1, labels1 = ax6.get_legend_handles_labels()
        lines2, labels2 = ax6_pop.get_legend_handles_labels()
        ax6.legend(lines1 + lines2, labels1 + labels2, loc='center right')

        # Save Figure 6
        fig6.savefig(f'../figures/{scenario_label}_palm_aging.pdf', format='pdf', dpi=600, bbox_inches='tight')
        fig6.savefig(f'../figures/{scenario_label}_palm_aging.png', format='png', dpi=600, bbox_inches='tight')

        # Figure 7: Seasonal Rat Dynamics - Zoomed view (first 20 years)
        fig7, (ax7a, ax7b) = plt.subplots(2, 1, figsize=(12, 10))

        # Select first 20 years for detailed view
        zoom_years = 20
        zoom_indices = t <= zoom_years
        zoom_dates = dates[zoom_indices]
        zoom_rats = rats[zoom_indices]
        zoom_mature_palms = mature_palms[zoom_indices]

        # Calculate seasonal carrying capacity for zoom period
        zoom_carrying_capacity = [self.seasonal_rat_carrying_capacity(time, mp)
                                  for time, mp in zip(t[zoom_indices], zoom_mature_palms)]

        # Top subplot: Rat population vs carrying capacity
        ax7a.plot(zoom_dates, zoom_rats, 'r-', linewidth=2, label='Actual Rat Population')
        ax7a.plot(zoom_dates, zoom_carrying_capacity, 'k--', linewidth=2,
                  label='Seasonal Carrying Capacity', alpha=0.7)
        ax7a.fill_between(zoom_dates, zoom_carrying_capacity, alpha=0.2, color='gray',
                          label='Carrying Capacity Range')
        ax7a.set_ylabel('Rat Population')
        ax7a.set_title('Seasonal Rat Population Dynamics: First 20 Years (1200-1220 CE)')
        ax7a.legend()
        ax7a.grid(True, alpha=0.3)

        # Bottom subplot: Annual population coefficient of variation
        ax7b.plot(zoom_dates, zoom_rats / 1000, 'r-', linewidth=2)
        ax7b.set_xlabel('Year (CE)')
        ax7b.set_ylabel('Rat Population (thousands)')
        ax7b.set_title('High-Resolution Rat Population Showing Annual Cycles')
        ax7b.grid(True, alpha=0.3)

        # Save Figure 7
        fig7.savefig(f'../figures/{scenario_label}_seasonal_rat_dynamics.pdf', format='pdf', dpi=600, bbox_inches='tight')
        fig7.savefig(f'../figures/{scenario_label}_seasonal_rat_dynamics.png', format='png', dpi=600, bbox_inches='tight')

        # Figure 8: Carrying Capacity vs Population Tracking
        fig8, ax8 = plt.subplots(1, 1, figsize=(10, 8))

        # Calculate full-time series carrying capacity
        full_carrying_capacity = [self.seasonal_rat_carrying_capacity(time, mp)
                                  for time, mp in zip(t, mature_palms)]

        # Plot carrying capacity vs actual population over full time series
        ax8.plot(dates, full_carrying_capacity, 'k-', linewidth=2, label='Carrying Capacity', alpha=0.8)
        ax8.plot(dates, rats, 'r-', linewidth=2, label='Actual Rat Population', alpha=0.8)

        # Add ratio line on secondary axis
        ax8_ratio = ax8.twinx()
        population_ratio = np.array(rats) / np.array(full_carrying_capacity)
        ax8_ratio.plot(dates, population_ratio, 'b-', linewidth=1.5,
                       label='Population/Carrying Capacity Ratio', alpha=0.6)
        ax8_ratio.axhline(y=1.0, color='blue', linestyle='--', alpha=0.5,
                          label='Carrying Capacity Limit')

        ax8.set_xlabel('Year (CE)')
        ax8.set_ylabel('Population', color='black')
        ax8_ratio.set_ylabel('Population Ratio', color='blue')
        ax8_ratio.tick_params(axis='y', labelcolor='blue')
        ax8.set_title('Rat Population Tracking vs Seasonal Carrying Capacity (1200-1722 CE)')
        ax8.grid(True, alpha=0.3)

        # Combine legends
        lines1, labels1 = ax8.get_legend_handles_labels()
        lines2, labels2 = ax8_ratio.get_legend_handles_labels()
        ax8.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

        # Save Figure 8
        fig8.savefig(f'../figures/{scenario_label}_carrying_capacity_tracking.pdf', format='pdf', dpi=600, bbox_inches='tight')
        fig8.savefig(f'../figures/{scenario_label}_carrying_capacity_tracking.png', format='png', dpi=600, bbox_inches='tight')

        # Figure 9: Seasonal Rat Dynamics - Later Period (1400-1500 CE)
        fig9, (ax9a, ax9b) = plt.subplots(2, 1, figsize=(12, 10))

        # Select 1400-1500 CE period for detailed view (200-300 years into simulation)
        late_start_year = 200  # 1400 CE
        late_end_year = 300  # 1500 CE
        late_indices = (t >= late_start_year) & (t <= late_end_year)
        late_dates = dates[late_indices]
        late_rats = rats[late_indices]
        late_mature_palms = mature_palms[late_indices]

        # Calculate seasonal carrying capacity for late period
        late_carrying_capacity = [self.seasonal_rat_carrying_capacity(time, mp)
                                  for time, mp in zip(t[late_indices], late_mature_palms)]

        # Top subplot: Rat population vs carrying capacity (late period)
        ax9a.plot(late_dates, late_rats, 'r-', linewidth=2, label='Actual Rat Population')
        ax9a.plot(late_dates, late_carrying_capacity, 'k--', linewidth=2,
                  label='Seasonal Carrying Capacity', alpha=0.7)
        ax9a.fill_between(late_dates, late_carrying_capacity, alpha=0.2, color='gray',
                          label='Carrying Capacity Range')
        ax9a.set_ylabel('Rat Population')
        ax9a.set_title('Seasonal Rat Population Dynamics: Forest Decline Period (1400-1500 CE)')
        ax9a.legend()
        ax9a.grid(True, alpha=0.3)

        # Bottom subplot: High-resolution rat population for late period
        ax9b.plot(late_dates, late_rats / 1000, 'r-', linewidth=2)
        ax9b.set_xlabel('Year (CE)')
        ax9b.set_ylabel('Rat Population (thousands)')
        ax9b.set_title('High-Resolution Rat Population During Palm Forest Collapse')
        ax9b.grid(True, alpha=0.3)

        # Save Figure 9
        fig9.savefig(f'../figures/{scenario_label}_late_seasonal_dynamics.pdf', format='pdf', dpi=600, bbox_inches='tight')
        fig9.savefig(f'../figures/{scenario_label}_late_seasonal_dynamics.png', format='png', dpi=600, bbox_inches='tight')

        # Display all figures
        plt.show()

        print(f"\nFigures saved in ../figures/ directory with prefix '{scenario_label}_':")
        print(f"- {scenario_label}_palm_decline.pdf/.png")
        print(f"- {scenario_label}_rat_population.pdf/.png")
        print(f"- {scenario_label}_human_population.pdf/.png")
        print(f"- {scenario_label}_comparative_dynamics.pdf/.png")
        print(f"- {scenario_label}_rats_vs_trees.pdf/.png")
        print(f"- {scenario_label}_palm_aging.pdf/.png")
        print(f"- {scenario_label}_seasonal_rat_dynamics.pdf/.png")
        print(f"- {scenario_label}_carrying_capacity_tracking.pdf/.png")
        print(f"- {scenario_label}_late_seasonal_dynamics.pdf/.png")

        # Calculate seasonal variation for both early and late periods

        # Early period analysis (first 20 years: 1200-1220 CE)
        early_analysis_rats = zoom_rats  # Use the zoom data already calculated
        if len(early_analysis_rats) > 8:  # Need at least 2 years of monthly data
            early_rolling_max = []
            early_rolling_min = []
            window = 12  # Monthly data points per year
            for i in range(window, len(early_analysis_rats)):
                year_data = early_analysis_rats[i - window:i]
                early_rolling_max.append(max(year_data))
                early_rolling_min.append(min(year_data))

            if early_rolling_max and early_rolling_min:
                early_seasonal_swing = np.mean([mx / mn if mn > 0 else 0
                                                for mx, mn in zip(early_rolling_max, early_rolling_min)])
            else:
                early_seasonal_swing = 0
        else:
            early_seasonal_swing = 0

        # Late period analysis (1400-1500 CE)
        late_analysis_rats = late_rats
        if len(late_analysis_rats) > 8:  # Need at least 2 years of monthly data
            late_rolling_max = []
            late_rolling_min = []
            window = 12  # Monthly data points per year
            for i in range(window, len(late_analysis_rats)):
                year_data = late_analysis_rats[i - window:i]
                late_rolling_max.append(max(year_data))
                late_rolling_min.append(min(year_data))

            if late_rolling_max and late_rolling_min:
                late_seasonal_swing = np.mean([mx / mn if mn > 0 else 0
                                               for mx, mn in zip(late_rolling_max, late_rolling_min)])
            else:
                late_seasonal_swing = 0
        else:
            late_seasonal_swing = 0

        # Calculate and report annual coefficient of variation for rat populations
        # Focus on years with substantial rat populations (first 50 years)
        analysis_period = min(50, len(t))
        analysis_rats = rats[:analysis_period]
        analysis_time = t[:analysis_period]

        # Calculate year-over-year changes to quantify boom-bust cycles
        annual_changes = []
        for i in range(1, len(analysis_rats)):
            if analysis_rats[i - 1] > 0:
                change = abs(analysis_rats[i] - analysis_rats[i - 1]) / analysis_rats[i - 1]
                annual_changes.append(change)

        mean_annual_change = np.mean(annual_changes) if annual_changes else 0

        # Calculate coefficient of variation for the analysis period
        if len(analysis_rats) > 0 and np.mean(analysis_rats) > 0:
            cv_rats = np.std(analysis_rats) / np.mean(analysis_rats)
        else:
            cv_rats = 0

        # Find maximum seasonal swings
        if len(analysis_rats) > 4:  # Need at least 2 years of data
            rolling_max = []
            rolling_min = []
            window = 4  # Quarterly data points per year
            for i in range(window, len(analysis_rats)):
                year_data = analysis_rats[i - window:i]
                rolling_max.append(max(year_data))
                rolling_min.append(min(year_data))

            if rolling_max and rolling_min:
                avg_seasonal_swing = np.mean([mx / mn if mn > 0 else 0
                                              for mx, mn in zip(rolling_max, rolling_min)])
            else:
                avg_seasonal_swing = 0
        else:
            avg_seasonal_swing = 0

        # Print aging-related statistics
        print(f"\nPalm aging dynamics:")
        print(f"Initial average age of mature palms: {self.initial_mature_age} years")
        print(f"Final average age of mature palms: {mature_avg_age[-1]:.1f} years")
        print(f"Senescence age threshold: {self.palm_senescence_age} years")
        print(f"Maximum lifespan: {self.palm_max_lifespan} years")
        senescence_time = np.where(mature_avg_age > self.palm_senescence_age)[0]
        if len(senescence_time) > 0:
            print(f"Senescence threshold reached: Year {int(dates[senescence_time[0]])}")
        else:
            print("Senescence threshold not reached during simulation")

        # Reset matplotlib parameters
        plt.rcParams.update(plt.rcParamsDefault)

    def run_comparison_simulation(self, years=522):
        """
        Run comparative simulation: Rats-only vs Rats+Humans scenarios
        Both scenarios run to European contact (1722 CE = 522 years)
        Saves separate figure sets for each scenario
        """
        print("Running comparative simulation...")
        print("Both scenarios will run to European contact (1722 CE)")
        
        # Run rats-only scenario to 1722
        print(f"\nScenario 1: Rats only (no human forest clearing) - running to 1722 CE ({years} years)")
        self.enable_human_clearing = False
        t_rats, rats_rats, mature_palms_rats, young_palms_rats, total_palms_rats, humans_rats, mature_avg_age_rats = self.run_simulation(years)
        
        # Save rats-only figures
        print("\nGenerating figures for rats-only scenario...")
        self.plot_results(t_rats, rats_rats, mature_palms_rats, young_palms_rats, 
                         total_palms_rats, humans_rats, mature_avg_age_rats, 
                         scenario_label="rats_only")

        print(f"\nScenario 2: Rats + humans (with forest clearing) - running to 1722 CE ({years} years)")
        # Run rats+humans scenario for same period
        self.enable_human_clearing = True
        t_humans, rats_humans, mature_palms_humans, young_palms_humans, total_palms_humans, humans_humans, mature_avg_age_humans = self.run_simulation(years)
        
        # Save rats+humans figures
        print("\nGenerating figures for rats+humans scenario...")
        self.plot_results(t_humans, rats_humans, mature_palms_humans, young_palms_humans, 
                         total_palms_humans, humans_humans, mature_avg_age_humans, 
                         scenario_label="rats_humans")

        # Create direct comparison plots
        self.plot_comparison_results(t_rats, rats_rats, total_palms_rats, mature_palms_rats, mature_avg_age_rats,
                                     t_humans, rats_humans, total_palms_humans, mature_palms_humans,
                                     mature_avg_age_humans, humans_humans)

        return (t_rats, rats_rats, total_palms_rats, mature_palms_rats, mature_avg_age_rats,
                t_humans, rats_humans, total_palms_humans, mature_palms_humans, mature_avg_age_humans)

    def plot_comparison_results(self, t_rats, rats_rats, total_palms_rats, mature_palms_rats, mature_avg_age_rats,
                                t_humans, rats_humans, total_palms_humans, mature_palms_humans, mature_avg_age_humans,
                                humans_humans):
        """
        Create direct comparison plots for rats-only vs rats+humans scenarios (both to 1722 CE)
        """
        dates_rats = 1200 + t_rats
        dates_humans = 1200 + t_humans

        # Set up high-resolution plotting parameters
        plt.rcParams['figure.dpi'] = 600
        plt.rcParams['savefig.dpi'] = 600
        plt.rcParams['savefig.bbox'] = 'tight'

        # Figure 10: Direct Palm Forest Comparison (1200-1722 CE)
        fig10, ax10 = plt.subplots(1, 1, figsize=(12, 8))

        # Plot both scenarios on same timeline
        ax10.plot(dates_rats, total_palms_rats / 1000, 'g-', linewidth=3,
                   label='Rats Only', alpha=0.8)
        ax10.plot(dates_humans, total_palms_humans / 1000, 'r-', linewidth=3,
                   label='Rats + Humans', alpha=0.8)
        ax10.axvline(x=1722, color='blue', linestyle='--', alpha=0.7, label='European Contact (1722 CE)')
        ax10.set_xlabel('Year (CE)')
        ax10.set_ylabel('Total Palm Trees (thousands)')
        ax10.set_title('Palm Forest Decline Comparison: Rats Only vs Rats + Humans (1200-1722 CE)')
        ax10.legend()
        ax10.grid(True, alpha=0.3)
        ax10.set_xlim(1200, 1750)
        ax10.set_ylim(0, max(max(total_palms_rats), max(total_palms_humans)) / 1000 * 1.1)

        fig10.savefig('../figures/comparison_palm_decline.pdf', format='pdf', dpi=600, bbox_inches='tight')
        fig10.savefig('../figures/comparison_palm_decline.png', format='png', dpi=600, bbox_inches='tight')

        # Figure 11: Rat Population Comparison
        fig11, ax11 = plt.subplots(1, 1, figsize=(12, 8))

        ax11.plot(dates_rats, rats_rats / 1000, 'g-', linewidth=3,
                  label='Rats Only Scenario', alpha=0.8)
        ax11.plot(dates_humans, rats_humans / 1000, 'r-', linewidth=3,
                  label='Rats + Humans Scenario', alpha=0.8)
        ax11.axvline(x=1722, color='blue', linestyle='--', alpha=0.7, label='European Contact (1722 CE)')
        ax11.set_xlabel('Year (CE)')
        ax11.set_ylabel('Rat Population (thousands)')
        ax11.set_title('Rat Population Dynamics Comparison (1200-1722 CE)')
        ax11.legend()
        ax11.grid(True, alpha=0.3)
        ax11.set_xlim(1200, 1750)

        fig11.savefig('../figures/comparison_rat_population.pdf', format='pdf', dpi=600, bbox_inches='tight')
        fig11.savefig('../figures/comparison_rat_population.png', format='png', dpi=600, bbox_inches='tight')

        # Figure 12: Palm Decline with Human Population
        fig12, ax12 = plt.subplots(1, 1, figsize=(12, 8))

        # Plot palm populations
        ax12.plot(dates_rats, total_palms_rats / 1000, 'g-', linewidth=3,
                  label='Rats Only', alpha=0.8)
        ax12.plot(dates_humans, total_palms_humans / 1000, 'r-', linewidth=3,
                  label='Rats + Humans', alpha=0.8)
        ax12.axvline(x=1722, color='blue', linestyle='--', alpha=0.7, label='European Contact')

        ax12.set_xlabel('Year (CE)')
        ax12.set_ylabel('Total Palm Trees (thousands)', color='black')
        ax12.set_title('Palm Forest Decline with Human Population Growth (1200-1722 CE)')
        ax12.grid(True, alpha=0.3)
        ax12.set_xlim(1200, 1750)
        ax12.set_ylim(0, max(max(total_palms_rats), max(total_palms_humans)) / 1000 * 1.1)

        # Add human population on secondary y-axis
        ax12_human = ax12.twinx()
        ax12_human.plot(dates_humans, humans_humans, 'b-', linewidth=2.5,
                        label='Human Population', alpha=0.8)
        ax12_human.set_ylabel('Human Population', color='blue')
        ax12_human.tick_params(axis='y', labelcolor='blue')
        ax12_human.set_ylim(0, max(humans_humans) * 1.1)

        # Combine legends
        lines1, labels1 = ax12.get_legend_handles_labels()
        lines2, labels2 = ax12_human.get_legend_handles_labels()
        ax12.legend(lines1 + lines2, labels1 + labels2, loc='center right')

        fig12.savefig('../figures/comparison_palm_decline_with_humans.pdf', format='pdf', dpi=600, bbox_inches='tight')
        fig12.savefig('../figures/comparison_palm_decline_with_humans.png', format='png', dpi=600, bbox_inches='tight')

        plt.show()

        # Calculate comparative statistics
        self.print_comparison_statistics(t_rats, total_palms_rats, rats_rats, mature_avg_age_rats,
                                         t_humans, total_palms_humans, rats_humans, mature_avg_age_humans,
                                         humans_humans)

        print("\nComparison figures saved in ../figures/ directory:")
        print("- comparison_palm_decline.pdf/.png")
        print("- comparison_rat_population.pdf/.png")
        print("- comparison_palm_decline_with_humans.pdf/.png")

        # Reset matplotlib parameters
        plt.rcParams.update(plt.rcParamsDefault)

    def print_comparison_statistics(self, t_rats, total_palms_rats, rats_rats, mature_avg_age_rats,
                                    t_humans, total_palms_humans, rats_humans, mature_avg_age_humans,
                                    humans_humans):
        """
        Print detailed comparison statistics between scenarios (both to 1722 CE)
        """
        dates_rats = 1200 + t_rats
        dates_humans = 1200 + t_humans

        print("\n" + "=" * 80)
        print("COMPARATIVE ECOLOGICAL ANALYSIS (1200-1722 CE)")
        print("=" * 80)

        # Timeline information
        timeline = int(t_rats[-1])
        print(f"SIMULATION TIMELINE: {timeline} years (1200-1722 CE)")
        print("Both scenarios run to European contact")

        # Final outcomes
        final_palms_rats = total_palms_rats[-1]
        final_palms_humans = total_palms_humans[-1]
        final_rats_rats = rats_rats[-1]
        final_rats_humans = rats_humans[-1]

        print(f"\nFINAL OUTCOMES AT EUROPEAN CONTACT (1722 CE):")
        print(f"Rats Only Scenario:")
        print(f"  Final palm trees: {final_palms_rats:,.0f} ({final_palms_rats / 15000000 * 100:.2f}% remaining)")
        print(f"  Final rat population: {final_rats_rats:,.0f}")

        print(f"Rats + Humans Scenario:")
        print(f"  Final palm trees: {final_palms_humans:,.0f} ({final_palms_humans / 15000000 * 100:.2f}% remaining)")
        print(f"  Final rat population: {final_rats_humans:,.0f}")
        
        print(f"\nDifference:")
        print(f"  Additional palm loss with humans: {final_palms_rats - final_palms_humans:,.0f} trees")
        print(f"  Percentage difference: {((final_palms_rats - final_palms_humans) / final_palms_rats * 100):.1f}% more loss with humans")

        # Peak populations
        peak_rats_rats = max(rats_rats)
        peak_rats_humans = max(rats_humans)
        peak_year_rats = int(dates_rats[np.argmax(rats_rats)])
        peak_year_humans = int(dates_humans[np.argmax(rats_humans)])

        print(f"\nPEAK RAT POPULATIONS:")
        print(f"Rats Only: {peak_rats_rats:,.0f} in year {peak_year_rats}")
        print(f"Rats + Humans: {peak_rats_humans:,.0f} in year {peak_year_humans}")


        # Timeline analysis - key thresholds
        thresholds = [10000000, 5000000, 1000000, 100000, 10000]

        print(f"\nFOREST DECLINE MILESTONES:")
        print(f"{'Palm Trees':>12} {'Rats Only':>12} {'Rats+Humans':>12} {'Acceleration':>12}")
        print("-" * 52)

        for threshold in thresholds:
            # Rats only scenario
            rats_indices = np.where(total_palms_rats < threshold)[0]
            rats_year = int(dates_rats[rats_indices[0]]) if len(rats_indices) > 0 else "Not reached"

            # Rats + humans scenario
            humans_indices = np.where(total_palms_humans < threshold)[0]
            humans_year = int(dates_humans[humans_indices[0]]) if len(humans_indices) > 0 else "Not reached"

            # Calculate difference
            if rats_year != "Not reached" and humans_year != "Not reached":
                difference = f"{humans_year - rats_year:+d} years"
            else:
                difference = "N/A"

            print(f"{threshold:>12,} {str(rats_year):>12} {str(humans_year):>12} {difference:>12}")

        # Final assessment
        print(f"\nKEY FINDINGS:")
        
        # Compare final states
        palm_difference_pct = ((final_palms_rats - final_palms_humans) / final_palms_rats * 100)
        print(f"✓ Human activities accelerate deforestation significantly")
        print(f"  {palm_difference_pct:.1f}% fewer palms remain when humans are present")
        
        # Rat population comparison
        if peak_rats_rats != peak_rats_humans:
            if peak_rats_rats > peak_rats_humans:
                print(f"✓ Rat populations peak slightly higher without human harvesting")
                print(f"  Peak difference: {peak_rats_rats - peak_rats_humans:,.0f} more rats")
            else:
                print(f"✓ Human presence affects rat population dynamics")
                print(f"  Peak difference: {peak_rats_humans - peak_rats_rats:,.0f} more rats with humans")
        
        # Speed comparison
        rat_decline_rate = (15000000 - final_palms_rats) / 522  # trees per year
        human_decline_rate = (15000000 - final_palms_humans) / 522  # trees per year
        print(f"\nDEFORESTATION RATES (1200-1722 CE):")
        print(f"Rats Only: {rat_decline_rate:,.0f} trees lost per year")
        print(f"Rats + Humans: {human_decline_rate:,.0f} trees lost per year")
        if rat_decline_rate > 0:
            print(f"Human acceleration factor: {human_decline_rate / rat_decline_rate:.1f}x faster")


# Run the historical simulation
def main():
    """
    Execute the Rapa Nui historical ecosystem simulation (1200-1722 CE).
    """
    print("Rapa Nui Ecological Collapse Simulation")
    print("Modeling the period 1200-1722 CE (European contact)")
    print("Initial palm forest: 15 million trees (Jubaea chilensis-like)")
    print("Human population: logistic growth from 20 individuals (2.5% initial growth rate)")
    print("Human carrying capacity: 4,000 individuals")
    print("Rat biology: Average 2.5 litters/year, 2.5 offspring/litter, 1 year lifespan")
    print("Rat carrying capacity: 0.5-4.0 rats per palm (seasonal variation, 3-month nut season)")
    print("Palm lifespan: Up to 500 years with age-dependent mortality and senescence")
    print("Time resolution: Monthly steps to capture seasonal boom-bust cycles")
    print()

    ecosystem = RapaNuiEcosystem()

    # Ask user which simulation to run
    print("Choose simulation type:")
    print("1. Standard simulation (Rats + Humans)")
    print("2. Comparative simulation (Rats Only vs Rats + Humans)")

    choice = input("Enter choice (1 or 2, or press Enter for standard): ").strip()

    if choice == "2":
        # Run comparative simulation
        print("\n" + "=" * 60)
        print("RUNNING COMPARATIVE ANALYSIS")
        print("=" * 60)
        ecosystem.run_comparison_simulation(years=522)
    else:
        # Run standard simulation (default)
        print("\n" + "=" * 60)
        print("RUNNING STANDARD SIMULATION (Rats + Humans)")
        print("=" * 60)
        t, rats, mature_palms, young_palms, total_palms, humans, mature_avg_age = ecosystem.run_simulation(years=522)
        ecosystem.plot_results(t, rats, mature_palms, young_palms, total_palms, humans, mature_avg_age, scenario_label="rats_humans")


if __name__ == "__main__":
    main()
