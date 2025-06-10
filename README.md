# Rapa Nui Rats: Ecological Impact Analysis and Population Modeling

This repository contains code and data supporting the paper "Reassessing the Role of Polynesian Rats (*Rattus exulans*) in Rapa Nui's Deforestation" by Terry L. Hunt and Carl P. Lipo.

## Overview

The ecological transformation of Rapa Nui (Easter Island) has become one of the most contested case studies in environmental archaeology. This repository provides computational tools to analyze the role of introduced Polynesian rats (*Rattus exulans*) in the island's deforestation through three complementary approaches:

1. **Archaeological Data Analysis (R)**: Analysis of rat remains from excavations at Anakena (1986-2005) to test competing hypotheses about rat population dynamics
2. **Ecological Simulation (Python)**: Population dynamics modeling to quantify the demographic consequences of rat introduction
3. **Taphonomic Analysis (Python)**: Quantitative model addressing methodological critiques of rat predation evidence in palm nut shell assemblages

## Key Findings

### Population Dynamics and Archaeological Evidence
- Rat populations followed a boom-bust trajectory typical of invasive species, NOT a resource depression "fallback food" pattern
- Archaeological evidence shows a 93% decrease in rat abundance over time
- Modeling demonstrates rats could reach 11.2 million individuals within 47 years
- 95% seed predation by rats was sufficient to prevent palm regeneration
- Synergistic rat-human interactions accelerated deforestation from centuries to ~500 years

### Taphonomic Insights
- **Critical methodological finding**: 65-90% of palm nut shell fragments would lack visible gnaw marks even under intensive rat predation
- Geometric constraints (gnaw marks limited to ~20% of shell surface) combined with post-depositional fragmentation create systematic preservation bias
- Arguments against rat impact based on ungnawed shell fragments represent a fundamental taphonomic fallacy
- Mathematical modeling demonstrates that absence of gnaw marks is the expected outcome, not evidence against predation

## Repository Structure

```
RapaNuiRats/
├── R-code/                    # R analysis of archaeological faunal data
│   └── *.R                    # Analysis and figure generation scripts
├── python/                    # Python ecological simulation and taphonomic analysis
│   ├── rat_simulation.py      # Population dynamics model
│   └── PalmNutGnawModel.py    # Taphonomic analysis of gnaw mark preservation
├── figures/                   # Generated figures (created when code runs)
└── README.md                 # This file
```

## Installation

### R Analysis Setup

1. Install R (version 4.0 or higher) from [CRAN](https://cran.r-project.org/)

2. Install required R packages:
```r
install.packages(c("ggplot2", "dplyr", "tidyr", "gridExtra", "scales", "knitr", "svglite"))
```

3. Navigate to the R-code directory and run the analysis scripts

### Python Setup

1. Ensure Python 3.8+ is installed

2. Create a virtual environment (recommended):
```bash
cd python
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

3. Install required packages:
```bash
pip install numpy matplotlib scipy
```

## Usage

### Running the R Analysis

The R code analyzes faunal remains from multiple excavations to test two hypotheses:
- **Fallback Food Hypothesis**: Rats became increasingly important as other resources depleted
- **Boom-Bust Hypothesis**: Rats followed invasive species dynamics with explosive growth then decline

```r
# Set working directory to R-code folder
setwd("path/to/RapaNuiRats/R-code")

# Run the analysis
source("your_analysis_script.R")  # Replace with actual script name
```

**Outputs:**
- `fig_temporal_decline.png/svg` - Shows 93% decrease in rat abundance over time
- `fig_all_excavations.png/svg` - Rat patterns across all excavations
- `fig_variability.png/svg` - Coefficient of variation analysis

### Running the Ecological Simulation

The Python simulation models rat-palm population dynamics from 1200-1722 CE:

```bash
cd python
python rat_simulation.py
```

You'll be prompted to choose:
1. Standard simulation (Rats + Humans)
2. Comparative simulation (Rats Only vs Rats + Humans)

**Outputs include:**
- Palm forest decline trajectories
- Rat population boom-bust cycles
- Comparative impacts of rats alone vs. rats + humans
- Seasonal dynamics and carrying capacity analysis

### Running the Taphonomic Analysis

The taphonomic model addresses methodological critiques of rat predation evidence:

```bash
cd python
python PalmNutGnawModel.py
```

**The model provides:**
- Quantitative estimates of gnaw mark preservation rates under different fragmentation scenarios
- Sensitivity analysis across parameter ranges (hole sizes, fragment distributions)
- Statistical validation through Monte Carlo simulation
- Archaeological interpretation framework for shell fragment assemblages

**Key model components:**
- **Simple Probability Model**: Baseline theoretical predictions
- **Fragment Size Model**: Accounts for size-dependent preservation bias using log-normal fragmentation distributions
- **Geometric Overlap Model**: Spatial analysis of fragment-gnaw hole intersections
- **Sensitivity Analysis**: Robustness testing across 5-40% gnaw hole coverage

**Outputs:**
- Statistical summary of preservation bias across parameter space
- Visualization of fragment size effects and hole size sensitivity
- Archaeological scenario comparisons (no predation vs. intensive predation)
- Methodological guidelines for interpreting negative evidence

**Example results:**
```
Fragment size model results:
  Mean fragment area 1.0% of shell: 77.0% ± 3.2% lack gnaw marks
  Mean fragment area 5.0% of shell: 72.0% ± 4.1% lack gnaw marks
  Mean fragment area 10.0% of shell: 65.0% ± 5.3% lack gnaw marks
```

## Data Sources

### Archaeological Faunal Data
Archaeological data from Anakena excavations:
- Skjølsvold 1987-1988 (MNI data)
- Martinsson-Wallin & Crockford 1986-1988 (NISP data)
- Steadman 1991 Units 1-3 and Unit 4 (NISP data)
- Hunt & Lipo 2004-2005 (NISP data)

### Taphonomic Parameters
Based on empirical observations of rat gnaw patterns:
- Gnaw hole coverage: 10-40% of shell surface area (default 20%)
- Fragment size distribution: 1-20% of original shell area
- Post-depositional fragmentation: modeled as stochastic process

## Model Parameters

### Rat Population (Ecological Model)
- Intrinsic growth rate: 2.5 (accounting for 2.5 litters/year, 2.5 offspring/litter)
- Lifespan: 1 year
- Carrying capacity: 0.5-4.0 rats per palm (seasonal variation)

### Palm Forest (Ecological Model)
- Initial population: 15 million trees
- Lifespan: up to 500 years
- Maturation time: 70 years
- Seed predation efficiency: 95%

### Human Population (Ecological Model)
- Initial: 20 individuals (ca. 1200 CE)
- Carrying capacity: 3,000 individuals
- Forest clearing: 5 palms/person/year

### Taphonomic Model Parameters
- **Shell geometry**: Spherical approximation with normalized radius
- **Gnaw hole characteristics**: Circular holes representing 10-40% of surface area
- **Fragment distribution**: Log-normal size distribution (CV = 0.5)
- **Spatial relationships**: Random fragmentation independent of gnaw hole location
- **Monte Carlo iterations**: 1,000-10,000 simulations for statistical stability

## Methodological Innovation

This project demonstrates the importance of quantitative taphonomic modeling in archaeological interpretation. The palm nut analysis specifically addresses:

1. **Geometric constraints** in preservation of biological modifications
2. **Post-depositional bias** affecting archaeological assemblages  
3. **Statistical framework** for evaluating negative evidence
4. **Integration** of taphonomic and ecological approaches

The taphonomic model provides a template for addressing similar preservation bias problems in other archaeological contexts where the absence of evidence has been misinterpreted as evidence of absence.

## Citation

If you use this code or data, please cite:

Hunt, T.L. and Lipo, C.P. (2025 - in review). Reassessing the Role of Polynesian Rats (*Rattus exulans*) in Rapa Nui's Deforestation: Faunal Evidence and Ecological Modeling. Journal of Archaeological Science.

For the taphonomic model specifically:
```
Hunt, T.L. and Lipo, C.P. (2025). PalmNutGnawModel: Taphonomic analysis of gnaw mark 
preservation in fragmented shell assemblages. Software available at: 
https://github.com/[repository-url]
```

## Authors

- **Terry L. Hunt** - School of Anthropology, University of Arizona
  - Email: tlhunt@arizona.edu
  - ORCID: 0009-0008-6257-8533

- **Carl P. Lipo** - Department of Anthropology, Binghamton University
  - Email: clipo@binghamton.edu
  - ORCID: 0000-0003-4391-3590

## License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2025 Terry L. Hunt and Carl P. Lipo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Troubleshooting

### Common Issues

**Python Environment:**
- If you encounter import errors, ensure all required packages are installed in your active environment
- For matplotlib display issues on some systems, you may need to install additional GUI backends

**Memory Requirements:**
- The Monte Carlo simulations in PalmNutGnawModel.py are memory-efficient but may take several minutes for large parameter sweeps
- Reduce `n_simulations` parameter if experiencing performance issues

**R Dependencies:**
- Some plot generation may require additional system dependencies for SVG output
- Install `cairo` system library if experiencing SVG export issues

## Acknowledgments

We thank Sergio Rapu Haoa for his collegiality, and Gina Pakarati and Mike Rapu Haoa for their enduring commitment to community-based archaeology on Rapa Nui. We also acknowledge valuable discussions with colleagues about taphonomic processes and methodological approaches to negative evidence in archaeology.

## Contributing

We welcome contributions! Please feel free to submit issues or pull requests. Particular areas of interest include:

- Extension of taphonomic models to other shell/bone modification scenarios
- Additional ecological parameters for different island systems
- Visualization improvements for model outputs
- Performance optimizations for large-scale parameter exploration

## Additional Resources

- Related ecological modeling approaches: [Island Conservation](https://www.islandconservation.org/)
- Taphonomic analysis in archaeology: [Zooarchaeology methodology](https://academic.oup.com/book/5386)
- Monte Carlo methods in archaeology: [Computer Applications in Archaeology](https://caa-international.org/)
