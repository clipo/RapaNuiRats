# Rapa Nui Rats: Ecological Impact Analysis and Population Modeling

This repository contains code and data supporting the paper "Reassessing the Role of Polynesian Rats (*Rattus exulans*) in Rapa Nui's Deforestation" by Terry L. Hunt and Carl P. Lipo.

## Overview

The ecological transformation of Rapa Nui (Easter Island) has become one of the most contested case studies in environmental archaeology. This repository provides computational tools to analyze the role of introduced Polynesian rats (*Rattus exulans*) in the island's deforestation through two complementary approaches:

1. **Archaeological Data Analysis (R)**: Analysis of rat remains from excavations at Anakena (1986-2005) to test competing hypotheses about rat population dynamics
2. **Ecological Simulation (Python)**: Population dynamics modeling to quantify the demographic consequences of rat introduction

## Key Findings

- Rat populations followed a boom-bust trajectory typical of invasive species, NOT a resource depression "fallback food" pattern
- Archaeological evidence shows a 93% decrease in rat abundance over time
- Modeling demonstrates rats could reach 11.2 million individuals within 47 years
- 95% seed predation by rats was sufficient to prevent palm regeneration
- Synergistic rat-human interactions accelerated deforestation from centuries to ~500 years

## Repository Structure

```
RapaNuiRats/
├── R-code/                 # R analysis of archaeological faunal data
│   └── *.R                 # Analysis and figure generation scripts
├── python/                 # Python ecological simulation
│   └── rat_simulation.py   # Population dynamics model
├── figures/                # Generated figures (created when code runs)
└── README.md              # This file
```

## Installation

### R Analysis Setup

1. Install R (version 4.0 or higher) from [CRAN](https://cran.r-project.org/)

2. Install required R packages:
```r
install.packages(c("ggplot2", "dplyr", "tidyr", "gridExtra", "scales", "knitr", "svglite"))
```

3. Navigate to the R-code directory and run the analysis scripts

### Python Simulation Setup

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

Outputs:
- `fig_temporal_decline.png/svg` - Shows 93% decrease in rat abundance over time
- `fig_all_excavations.png/svg` - Rat patterns across all excavations
- `fig_variability.png/svg` - Coefficient of variation analysis

### Running the Python Simulation

The Python simulation models rat-palm population dynamics from 1200-1722 CE:

```bash
cd python
python rat_simulation.py
```

You'll be prompted to choose:
1. Standard simulation (Rats + Humans)
2. Comparative simulation (Rats Only vs Rats + Humans)

Outputs include:
- Palm forest decline trajectories
- Rat population boom-bust cycles
- Comparative impacts of rats alone vs. rats + humans
- Seasonal dynamics and carrying capacity analysis

## Data Sources

Archaeological data from Anakena excavations:
- Skjølsvold 1987-1988 (MNI data)
- Martinsson-Wallin & Crockford 1986-1988 (NISP data)
- Steadman 1991 Units 1-3 and Unit 4 (NISP data)
- Hunt & Lipo 2004-2005 (NISP data)

## Model Parameters

### Rat Population
- Intrinsic growth rate: 2.5 (accounting for 2.5 litters/year, 2.5 offspring/litter)
- Lifespan: 1 year
- Carrying capacity: 0.5-4.0 rats per palm (seasonal variation)

### Palm Forest
- Initial population: 15 million trees
- Lifespan: up to 500 years
- Maturation time: 70 years
- Seed predation efficiency: 95%

### Human Population
- Initial: 20 individuals (ca. 1200 CE)
- Carrying capacity: 3,000 individuals
- Forest clearing: 5 palms/person/year

## Citation

If you use this code or data, please cite:

Hunt, T.L. and Lipo, C.P. (2025 - in review ). Reassessing the Role of Polynesian Rats (*Rattus exulans*) in Rapa Nui's Deforestation: Faunal Evidence and Ecological Modeling. Journal of Archaeological Science.

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

## Acknowledgments

We thank Sergio Rapu Haoa for his collegiality, and Gina Pakarati and Mike Rapu Haoa for their enduring commitment to community-based archaeology on Rapa Nui.

## Contributing

We welcome contributions! Please feel free to submit issues or pull requests.

## Additional Resources

- Related ecological modeling approaches: [Island Conservation](https://www.islandconservation.org/)
