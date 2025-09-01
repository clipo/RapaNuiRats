# Rapa Nui Rats: Ecological Impact Analysis and Population Modeling

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![R 4.3+](https://img.shields.io/badge/R-4.3+-green.svg)](https://www.r-project.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository contains computational models and archaeological data analysis supporting the paper "Reassessing the Role of Polynesian Rats (*Rattus exulans*) in Rapa Nui's Deforestation" by Terry L. Hunt and Carl P. Lipo.

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

## Quick Start

### Prerequisites
- Python 3.8+ with pip
- R 4.3+ with RStudio (optional)
- Git for version control
- 2GB free disk space for simulations

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/rapanuirats.git
cd rapanuirats
```

2. **Set up Python environment**
```bash
cd python
bash setup_env.sh  # Or manually: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
```

3. **Set up R environment**
```r
# In R, from the R-code directory
setwd("R-code")
renv::restore()  # Installs exact package versions
```

### Running the Analyses

#### Generate All Figures (Recommended)
```bash
# From python directory
python rat_simulation.py  # Choose option 2 for comparative analysis
python RatNutGnawModel.py

# From R-code directory  
Rscript R-code-for-paper.R
```

This generates 25+ publication-quality figures in the `figures/` directory and automatically copies key paper figures to `paper_figures/` with standardized naming.

## Repository Structure

```
rapanuirats/
├── python/                    # Python ecological simulations
│   ├── rat_simulation.py      # Population dynamics model
│   ├── RatNutGnawModel.py     # Taphonomic analysis
│   ├── requirements.txt       # Python dependencies
│   └── setup_env.sh           # Environment setup script
├── R-code/                    # R archaeological analysis
│   ├── R-code-for-paper.R     # Faunal data analysis
│   ├── renv.lock              # R package versions
│   └── renv/                  # Project library
├── figures/                   # Output directory for all visualizations
├── paper_figures/             # Paper-ready figures with standardized naming
│   ├── Figure_9.*             # Archaeological temporal decline
│   ├── Figure_10.*            # All excavations comparison
│   ├── Figure_11.*            # Variability analysis
│   ├── Figure_12.*            # Ecological collapse (rats only)
│   └── Figure_13.*            # Ecological collapse (duplicate)
├── DEPENDENCIES.md            # Dependency management guide
├── CLAUDE.md                  # AI assistant configuration
└── README.md                  # This file
```


## Detailed Usage

### 1. Ecological Simulation (Python)

The population dynamics model simulates rat-palm forest interactions from 1200-1722 CE:

```bash
cd python
python rat_simulation.py
```

**Interactive Options:**
- Option 1: Standard simulation (Rats + Humans)
- Option 2: Comparative simulation (generates both scenarios)

**Generated Figures (18 files):**
- `rats_only_*`: 9 figures showing rats-only scenario
- `rats_humans_*`: 9 figures showing combined impact
- `comparison_*`: 3 direct comparison figures

**Key Parameters:**
- Initial palm forest: 15 million trees
- Rat growth rate: 2.5 (intrinsic)
- Seed predation: 95% efficiency
- Human population: 20-3,000 individuals

### 2. Taphonomic Analysis (Python)

Quantifies preservation bias in archaeological shell fragments:

```bash
cd python
python RatNutGnawModel.py
```

**Output:**
- `palm_nut_gnaw_sensitivity_analysis.png`: 4-panel sensitivity analysis
- Shows 65-90% of fragments would lack gnaw marks even with 100% predation

### 3. Archaeological Analysis (R)

Tests competing hypotheses using faunal data from excavations:

```bash
cd R-code
Rscript R-code-for-paper.R
```

**Generated Figures (3 files):**
- `archaeological_temporal_decline.png`: 93% decrease in rat abundance
- `archaeological_all_excavations.png`: Patterns across 5 excavations
- `archaeological_variability.png`: Coefficient of variation analysis

### Paper Figure Generation

The scripts automatically generate paper-ready figures in the `paper_figures/` directory with standardized naming conventions:

**Automatic Paper Figure Mapping:**
- **Figure 9**: Archaeological temporal decline (3-panel showing 93% rat decrease)
- **Figure 10**: Rat percentages across all excavations  
- **Figure 11**: High variability in rat abundance (coefficient of variation)
- **Figure 12 & 13**: Ecological collapse - rat population vs palm forest decline

To regenerate paper figures:
```bash
# Python figures (generates Figures 12-13)
cd python
echo "2" | python rat_simulation.py  # Option 2 for comparative analysis

# R figures (generates Figures 9-11)
cd ../R-code
Rscript --vanilla R-code-for-paper.R
```

All paper figures are saved in both PNG and PDF/SVG formats for publication use.


## Key Results

### Ecological Modeling
- Rat populations reach **11.2 million** within 47 years
- **77.7% faster deforestation** with human presence
- Palm forest decline from 15 million to <140,000 trees by 1722 CE (rats only)
- Complete deforestation accelerated to ~500 years with rat-human synergy

### Archaeological Evidence  
- **93% decrease** in rat abundance over time (contradicts fallback food hypothesis)
- High variability (CV >100%) indicates depositional effects
- Pattern consistent with invasive species boom-bust dynamics

### Taphonomic Analysis
- **65-90% of shell fragments lack gnaw marks** even with 100% predation
- Geometric constraints limit gnaw marks to ~20% of shell surface
- Post-depositional fragmentation creates systematic preservation bias

## Scientific Contributions

1. **Quantitative taphonomic modeling** - Mathematical framework for preservation bias
2. **Integrated ecological-archaeological approach** - Combines population dynamics with faunal evidence
3. **Resolution of methodological controversy** - Demonstrates fallacy in negative evidence arguments
4. **Reproducible computational science** - Full code and dependency management provided

## Citation

```bibtex
@article{hunt2025rats,
  title={Reassessing the Role of Polynesian Rats (Rattus exulans) in Rapa Nui's Deforestation},
  author={Hunt, Terry L. and Lipo, Carl P.},
  journal={Journal of Archaeological Science},
  year={2025},
  note={In review}
}

@software{hunt2025software,
  title={Rapa Nui Rats: Ecological and Taphonomic Models},
  author={Hunt, Terry L. and Lipo, Carl P.},
  year={2025},
  url={https://github.com/yourusername/rapanuirats}
}
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

- **Python import errors**: Activate virtual environment first (`source venv/bin/activate`)
- **R package errors**: Run `renv::restore()` from R-code directory
- **Memory issues**: Reduce simulation iterations or use a machine with more RAM
- **Missing figures**: Ensure you're in the correct directory when running scripts

## Contributing

We welcome contributions! Areas of interest:
- Extensions to other island systems
- Additional taphonomic scenarios
- Performance optimizations
- Visualization improvements

Please submit issues or pull requests via GitHub.

## Acknowledgments

We thank Sergio Rapu Haoa, Gina Pakarati, and Mike Rapu Haoa for their commitment to community-based archaeology on Rapa Nui.
