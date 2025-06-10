# =============================================================================
# RAPA NUI RAT IMPACT ANALYSIS - FIGURE GENERATION
# =============================================================================
# This script analyzes archaeological faunal data to test two competing hypotheses
# about Polynesian rat (Rattus exulans) population dynamics on Rapa Nui:
# 
# 1. FALLBACK FOOD HYPOTHESIS: Predicts rats became increasingly important as 
#    marine/bird resources were depleted (part of "ecocide" narrative)
# 2. BOOM-BUST HYPOTHESIS: Predicts explosive growth followed by decline,
#    typical of invasive species trajectories
#
# The analysis examines rat remains from multiple excavations at Anakena 
# spanning 1986-2005 to determine which model best explains the data.
# =============================================================================

# Load required libraries
library(ggplot2)    # For creating publication-quality plots
library(dplyr)      # For data manipulation and summarization
library(tidyr)      # For data reshaping
library(gridExtra)  # For arranging multiple plots
library(scales)     # For axis formatting
library(knitr)      # For document generation
library(svglite)    # For saving vector graphics

# -----------------------------------------------------------------------------
# SETUP: Create directories for saving figures
# -----------------------------------------------------------------------------
# Create separate directories for PNG (raster) and SVG (vector) formats
if (!dir.exists("figures_png")) {
  dir.create("figures_png")
}
if (!dir.exists("figures_svg")) {
  dir.create("figures_svg")
}

# =============================================================================
# DATA PREPARATION
# =============================================================================
# Each dataset represents rat remains from different excavation campaigns.
# These data will test whether rat populations followed:
# - Resource depression model (increasing over time as fallback food)
# - Invasive species model (boom early, bust later as forest depleted)
#
# MNI = Minimum Number of Individuals (counting method based on most frequent element)
# NISP = Number of Identified Specimens (raw count of identifiable bones)

# -----------------------------------------------------------------------------
# Skjølsvold 1987-1988 excavation
# -----------------------------------------------------------------------------
# CRITICAL DATASET: Provides clearest temporal control with two distinct layers
# Shows 93% DECREASE from early to late - key evidence for boom-bust model
skjolsvold_rat <- data.frame(
  Layer = c("Cultural Layer (Earlier)", "Sand Layer (Later)"),
  Rat_MNI = c(300, 21),        # 93% decrease supports boom-bust, not fallback
  Total_MNI = c(3970, 3345),   # Total fauna including fish, birds, etc.
  Stratigraphy = "Temporal"
)
# Calculate percentage of rats in total faunal assemblage
skjolsvold_rat$Rat_Percent <- (skjolsvold_rat$Rat_MNI / skjolsvold_rat$Total_MNI) * 100

# -----------------------------------------------------------------------------
# Martinsson-Wallin & Crockford 1986-1988 excavation
# -----------------------------------------------------------------------------
# Uses NISP counts at different depths (deeper = older)
# Variable abundances reflect depositional processes
mw_rat <- data.frame(
  Depth = c("230-240cm", "240-260cm", "270-280cm", "280-290cm", "290-300cm"),
  Depth_Numeric = c(235, 250, 275, 285, 295),  # Midpoint of each depth range
  Rat_NISP = c(12, 56, 26, 0, 1),              # Note peak at 240-260cm (earlier)
  Total_NISP = c(75, 336, 177, 4, 80),         # Total identifiable bones
  Stratigraphy = "Depth"
)
mw_rat$Rat_Percent <- (mw_rat$Rat_NISP / mw_rat$Total_NISP) * 100

# -----------------------------------------------------------------------------
# Steadman 1991 excavations - Units 1-3
# -----------------------------------------------------------------------------
# Larger excavation showing general decline from deeper (older) deposits
steadman_u13_rat <- data.frame(
  Depth = c("Surface", "0-20", "20-40", "40-60", "60-80", "80-100", "100-120", ">120"),
  Depth_Numeric = c(0, 10, 30, 50, 70, 90, 110, 130),
  Rat_NISP = c(0, 252, 480, 616, 196, 44, 19, 536),  # Peak in middle depths
  Total_NISP = c(20, 912, 1382, 1163, 583, 174, 273, 1926),
  Stratigraphy = "Depth"
)
steadman_u13_rat$Rat_Percent <- (steadman_u13_rat$Rat_NISP / steadman_u13_rat$Total_NISP) * 100

# -----------------------------------------------------------------------------
# Steadman 1991 excavations - Unit 4
# -----------------------------------------------------------------------------
# Shows increasing trend with depth (older deposits have more rats)
steadman_u4_rat <- data.frame(
  Depth = c("0/3-18/22", "18/22-37/40", "37/40-57/60"),
  Depth_Numeric = c(10, 30, 50),
  Rat_NISP = c(20, 60, 116),  # Increases with depth (age)
  Total_NISP = c(166, 292, 420),
  Stratigraphy = "Depth"
)
steadman_u4_rat$Rat_Percent <- (steadman_u4_rat$Rat_NISP / steadman_u4_rat$Total_NISP) * 100

# -----------------------------------------------------------------------------
# Hunt & Lipo 2004 excavation
# -----------------------------------------------------------------------------
# Peak abundance in middle levels (VI-VIII), lower in upper levels
# Pattern consistent with boom-bust trajectory
hl2004_rat <- data.frame(
  Level = paste("Level", c("I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII")),
  Level_Numeric = 1:12,  # Level I is shallowest (most recent)
  Rat_NISP = c(35, 0, 119, 213, 132, 296, 806, 433, 269, 62, 18, 0),
  Total_NISP = c(77, 6, 204, 558, 385, 535, 1191, 805, 385, 102, 171, 1),
  Stratigraphy = "Level"
)
hl2004_rat$Rat_Percent <- (hl2004_rat$Rat_NISP / hl2004_rat$Total_NISP) * 100

# -----------------------------------------------------------------------------
# Hunt & Lipo 2005 excavation
# -----------------------------------------------------------------------------
# Similar pattern: higher in middle levels, lower in upper (recent) levels
hl2005_rat <- data.frame(
  Level = paste("Level", c("I", "II", "III", "IV", "V", "VI", "VII")),
  Level_Numeric = 1:7,
  Rat_NISP = c(0, 151, 4, 77, 58, 665, 179),  # Peak at Level VI
  Total_NISP = c(2, 263, 11, 100, 96, 1206, 435),
  Stratigraphy = "Level"
)
hl2005_rat$Rat_Percent <- (hl2005_rat$Rat_NISP / hl2005_rat$Total_NISP) * 100

# =============================================================================
# FIGURE 1: TEMPORAL DECLINE IN RAT ABUNDANCE - TESTING COMPETING HYPOTHESES
# =============================================================================
# This figure tests two competing hypotheses:
# 1. FALLBACK FOOD: Predicts INCREASING rats over time as other resources depleted
# 2. BOOM-BUST: Predicts DECREASING rats over time following invasive species dynamics
#
# The 93% decrease from early to late directly contradicts fallback food hypothesis
# and strongly supports boom-bust trajectory typical of invasive species

# Save as PNG (high resolution for print)
png("figures_png/fig_temporal_decline.png", width = 10, height = 10, units = "in", res = 300)

# Set up 3-panel layout
par(mfrow = c(3, 1),      # 3 rows, 1 column
    mar = c(4, 4, 3, 2))  # margins: bottom, left, top, right

# -----------------------------------------------------------------------------
# Panel A: Raw MNI counts showing dramatic decline
# -----------------------------------------------------------------------------
# This 93% decrease is the KEY FINDING supporting boom-bust model
barplot(skjolsvold_rat$Rat_MNI, 
        names.arg = c("Earlier\n(Cultural Layer)", "Later\n(Sand Layer)"),
        main = "A. Rat Abundance Decreases Over Time (MNI)",
        ylab = "Number of Individuals (MNI)",
        col = c("darkred", "lightcoral"),  # Darker = older
        ylim = c(0, 350))

# Add value labels on bars
text(c(0.7, 1.9),                                    # x positions for bars
     skjolsvold_rat$Rat_MNI + 15,                    # y positions (above bars)
     skjolsvold_rat$Rat_MNI,                         # values to display
     font = 2, cex = 1.2)                            # bold, larger text

# Add arrow showing decline - emphasizes boom-bust pattern
arrows(0.7, 250, 1.9, 100, length = 0.15, lwd = 3, col = "red")
text(1.3, 200, "93% decrease", col = "red", font = 2, cex = 1.2)

# -----------------------------------------------------------------------------
# Panel B: Percentages to control for sample size differences
# -----------------------------------------------------------------------------
# Shows decline is not just absolute numbers but proportion of diet
barplot(skjolsvold_rat$Rat_Percent, 
        names.arg = c("Earlier\n(Cultural Layer)", "Later\n(Sand Layer)"),
        main = "B. Rat as Percentage of Total Fauna",
        ylab = "Rat %",
        col = c("darkred", "lightcoral"),
        ylim = c(0, 10))

# Add percentage labels
text(c(0.7, 1.9), 
     skjolsvold_rat$Rat_Percent + 0.5, 
     paste0(round(skjolsvold_rat$Rat_Percent, 1), "%"), 
     font = 2, cex = 1.2)

# -----------------------------------------------------------------------------
# Panel C: Compare marine vs. terrestrial resources
# -----------------------------------------------------------------------------
# Shows marine intensification (91% to 99%) as rats decline
# This pattern contradicts resource depression leading to fallback foods
marine_pct <- c(91.3, 99.1)      # Increases over time
terrestrial_pct <- c(7.6, 0.7)   # Decreases over time (includes rats)
comparison_data <- rbind(marine_pct, terrestrial_pct)
colnames(comparison_data) <- c("Earlier\n(Cultural Layer)", "Later\n(Sand Layer)")

barplot(comparison_data, 
        beside = TRUE,           # Bars side by side, not stacked
        main = "C. Marine vs. Terrestrial Fauna Over Time",
        ylab = "Percentage",
        col = c("blue", "brown"),
        legend = c("Marine", "Terrestrial"),
        args.legend = list(x = "topright", bty = "n"),  # Legend position
        ylim = c(0, 120))

dev.off()  # Close PNG device

# Save as SVG (vector format for publication)
svglite("figures_svg/fig_temporal_decline.svg", width = 10, height = 10)
# [Repeat same plotting code as above]
par(mfrow = c(3, 1), mar = c(4, 4, 3, 2))

# Panel A: Raw MNI counts
barplot(skjolsvold_rat$Rat_MNI, 
        names.arg = c("Earlier\n(Cultural Layer)", "Later\n(Sand Layer)"),
        main = "A. Rat Abundance Decreases Over Time (MNI)",
        ylab = "Number of Individuals (MNI)",
        col = c("darkred", "lightcoral"),
        ylim = c(0, 350))
text(c(0.7, 1.9), skjolsvold_rat$Rat_MNI + 15, skjolsvold_rat$Rat_MNI, font = 2, cex = 1.2)
arrows(0.7, 250, 1.9, 100, length = 0.15, lwd = 3, col = "red")
text(1.3, 200, "93% decrease", col = "red", font = 2, cex = 1.2)

# Panel B: Percentages
barplot(skjolsvold_rat$Rat_Percent, 
        names.arg = c("Earlier\n(Cultural Layer)", "Later\n(Sand Layer)"),
        main = "B. Rat as Percentage of Total Fauna",
        ylab = "Rat %",
        col = c("darkred", "lightcoral"),
        ylim = c(0, 10))
text(c(0.7, 1.9), skjolsvold_rat$Rat_Percent + 0.5, 
     paste0(round(skjolsvold_rat$Rat_Percent, 1), "%"), font = 2, cex = 1.2)

# Panel C: Compare with marine resources
barplot(comparison_data, 
        beside = TRUE,
        main = "C. Marine vs. Terrestrial Fauna Over Time",
        ylab = "Percentage",
        col = c("blue", "brown"),
        legend = c("Marine", "Terrestrial"),
        args.legend = list(x = "topright", bty = "n"),
        ylim = c(0, 120))
dev.off()

# Display in R/RStudio for preview
par(mfrow = c(3, 1), mar = c(4, 4, 3, 2))
# [Same plotting code repeated for display]

# =============================================================================
# FIGURE 2: RAT ABUNDANCE ACROSS ALL EXCAVATIONS - BOOM-BUST PATTERNS
# =============================================================================
# This figure examines whether the 93% decline seen in Skjølsvold's excavation
# represents a broader boom-bust pattern across multiple excavations.
# Generally shows higher abundances in earlier contexts, lower in later ones.

# -----------------------------------------------------------------------------
# Data preparation: Standardize column names for combining datasets
# -----------------------------------------------------------------------------
# Since some excavations use "Depth" and others use "Level", we need to
# standardize the column names before combining

# Excavations measured by depth
mw_rat_std <- mw_rat %>%
  rename(Context = Depth, Context_Numeric = Depth_Numeric) %>%
  mutate(Excavation = "MW 1986-88", Year = 1986)

steadman_u13_rat_std <- steadman_u13_rat %>%
  rename(Context = Depth, Context_Numeric = Depth_Numeric) %>%
  mutate(Excavation = "Steadman 1991 U1-3", Year = 1991)

steadman_u4_rat_std <- steadman_u4_rat %>%
  rename(Context = Depth, Context_Numeric = Depth_Numeric) %>%
  mutate(Excavation = "Steadman 1991 U4", Year = 1991)

# Excavations measured by arbitrary levels
hl2004_rat_std <- hl2004_rat %>%
  rename(Context = Level, Context_Numeric = Level_Numeric) %>%
  mutate(Excavation = "Hunt & Lipo 2004", Year = 2004)

hl2005_rat_std <- hl2005_rat %>%
  rename(Context = Level, Context_Numeric = Level_Numeric) %>%
  mutate(Excavation = "Hunt & Lipo 2005", Year = 2005)

# Combine all standardized data into one dataframe
all_rat_data <- bind_rows(
  mw_rat_std,
  steadman_u13_rat_std,
  steadman_u4_rat_std,
  hl2004_rat_std,
  hl2005_rat_std
)

# -----------------------------------------------------------------------------
# Calculate mean rat percentages by excavation
# -----------------------------------------------------------------------------
# No directional trend over excavation years - contradicts systematic increase
# expected under fallback food hypothesis
mean_rats <- all_rat_data %>%
  filter(Total_NISP > 50) %>%  # Exclude contexts with very small samples
  group_by(Excavation, Year) %>%
  summarise(
    Mean_Rat_Percent = mean(Rat_Percent, na.rm = TRUE),
    n_samples = n(),            # Number of contexts averaged
    .groups = 'drop'
  )

# Add Skjølsvold data (which uses MNI, not NISP)
mean_rats <- bind_rows(mean_rats,
                       data.frame(Excavation = "Skjølsvold 1987-88",
                                  Year = 1987,
                                  Mean_Rat_Percent = mean(skjolsvold_rat$Rat_Percent),
                                  n_samples = 2))

# Print summary for verification
print("Mean rat percentages by year:")
print(mean_rats)

# -----------------------------------------------------------------------------
# Create faceted plot showing all excavations
# -----------------------------------------------------------------------------
# Patterns generally show higher abundances in deeper/earlier contexts
# Supporting boom-bust rather than increasing fallback food use
p1 <- ggplot(all_rat_data, aes(x = Context_Numeric, y = Rat_Percent)) +
  geom_point(size = 3, color = "darkred") +
  geom_line(color = "darkred", alpha = 0.5) +  # Connect points to show trends
  facet_wrap(~Excavation,                      # Separate panel for each excavation
             scales = "free_x",                 # Allow different x-axis scales
             ncol = 2) +                        # Two columns of panels
  theme_minimal(base_size = 12) +
  labs(title = "Rat Percentages Across Excavations",
       x = "Depth/Level", 
       y = "Rat %") +
  theme(plot.title = element_text(size = 14, face = "bold"),
        panel.grid.minor = element_blank(),     # Cleaner appearance
        strip.text = element_text(face = "bold"))  # Bold excavation names

# Save as PNG
png("figures_png/fig_all_excavations.png", width = 10, height = 10, units = "in", res = 300)
grid.arrange(p1, heights = c(1, 1))
dev.off()

# Save as SVG
svg("figures_svg/fig_all_excavations.svg", width = 10, height = 10)
grid.arrange(p1, heights = c(1, 1))
dev.off()

# Display in R/RStudio
grid.arrange(p1, heights = c(1, 1))

# =============================================================================
# FIGURE 3: COEFFICIENT OF VARIATION ANALYSIS - DEPOSITIONAL EFFECTS
# =============================================================================
# High variability (CV > 100%) indicates depositional processes rather than
# stable dietary patterns. This suggests rat concentrations reflect natural
# death assemblages or specific activity areas, not just food consumption.
# Important for interpreting the boom-bust pattern vs. dietary signal.

# -----------------------------------------------------------------------------
# Calculate coefficient of variation for each excavation
# -----------------------------------------------------------------------------
# CV = (standard deviation / mean) × 100
# Higher values indicate more variability from depositional processes

cv_data <- data.frame(
  Excavation = c("Skjølsvold MNI", "MW 1986-88", "Steadman U1-3", 
                 "Steadman U4", "HL 2004", "HL 2005"),
  CV_Rat = c(
    # Skjølsvold: Using MNI counts - still shows high variability
    sd(skjolsvold_rat$Rat_MNI) / mean(skjolsvold_rat$Rat_MNI) * 100,
    
    # MW 1986-88: Only use contexts with adequate sample size
    sd(mw_rat$Rat_NISP[mw_rat$Total_NISP > 20]) / 
      mean(mw_rat$Rat_NISP[mw_rat$Total_NISP > 20]) * 100,
    
    # Steadman U1-3: All contexts
    sd(steadman_u13_rat$Rat_NISP) / mean(steadman_u13_rat$Rat_NISP) * 100,
    
    # Steadman U4: All contexts
    sd(steadman_u4_rat$Rat_NISP) / mean(steadman_u4_rat$Rat_NISP) * 100,
    
    # HL 2004: Only contexts with adequate sample
    sd(hl2004_rat$Rat_NISP[hl2004_rat$Total_NISP > 10]) / 
      mean(hl2004_rat$Rat_NISP[hl2004_rat$Total_NISP > 10]) * 100,
    
    # HL 2005: Only contexts with adequate sample
    sd(hl2005_rat$Rat_NISP[hl2005_rat$Total_NISP > 10]) / 
      mean(hl2005_rat$Rat_NISP[hl2005_rat$Total_NISP > 10]) * 100
  )
)

# Create horizontal bar plot (easier to read excavation names)
p3 <- ggplot(cv_data, aes(x = reorder(Excavation, CV_Rat), y = CV_Rat)) +
  geom_bar(stat = "identity", fill = "brown", alpha = 0.8) +
  coord_flip() +  # Flip to horizontal
  theme_minimal(base_size = 12) +
  labs(title = "High Variability in Rat Abundance Indicates Depositional Effects",
       subtitle = "Coefficients of variation > 100% in most excavations",
       x = "", 
       y = "Coefficient of Variation (%)") +
  geom_hline(yintercept = 100,        # Reference line at 100%
             linetype = "dashed", 
             color = "red", 
             size = 1) +
  annotate("text",                     # Label the reference line
           x = 1, y = 120, 
           label = "High variability threshold", 
           color = "red", 
           hjust = 0, 
           size = 3.5) +
  theme(plot.title = element_text(size = 14, face = "bold"),
        plot.subtitle = element_text(size = 12, face = "italic"))

# Save as PNG
ggsave("figures_png/fig_variability.png", plot = p3, width = 10, height = 6, dpi = 300)

# Save as SVG
ggsave("figures_svg/fig_variability.svg", plot = p3, width = 10, height = 6)

# Display in R/RStudio
print(p3)

# =============================================================================
# FINAL OUTPUT MESSAGE
# =============================================================================
# Print summary of what was created and key findings

cat("\n=== FIGURE GENERATION COMPLETE ===\n")
cat("\nAll figures have been saved to:\n")
cat("PNG files: figures_png/\n")
cat("SVG files: figures_svg/\n")
cat("\nSaved files:\n")
cat("- fig_temporal_decline.png/.svg (3-panel showing 93% rat decline)\n")
cat("- fig_all_excavations.png/.svg (Faceted plot of all excavations)\n")
cat("- fig_variability.png/.svg (Coefficient of variation analysis)\n")
cat("\nKey findings visualized:\n")
cat("1. 93% decrease in rats over time SUPPORTS boom-bust invasive species model\n")
cat("2. Pattern CONTRADICTS fallback food hypothesis (would predict increase)\n")
cat("3. High variability (CV >100%) indicates depositional effects\n")
cat("4. Results consistent with ecological modeling showing 11.2 million rats\n")
cat("   within 47 years, followed by decline as palm forest depleted\n")
cat("\nConclusion: Invasive rat dynamics, not resource depression/ecocide narrative\n")
