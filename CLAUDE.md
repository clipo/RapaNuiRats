# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an ecological and archaeological analysis project studying the role of Polynesian rats (*Rattus exulans*) in Rapa Nui's deforestation. The codebase contains:
- Python simulations for rat population dynamics and taphonomic analysis
- R scripts for archaeological faunal data analysis

## Commands

### Python Development

```bash
# Navigate to Python directory
cd python

# Install dependencies
pip install -r requirements.txt

# Run rat population simulation
python rat_simulation.py

# Run taphonomic analysis model
python RatNutGnawModel.py
```

### R Development

```bash
# Navigate to R directory
cd R-code

# Run the analysis script
Rscript R-code-for-paper.R
```

## Code Architecture

### Python Components

**rat_simulation.py**: Population dynamics model simulating rat-palm forest interactions from 1200-1722 CE
- Uses scipy's odeint for ODE integration
- Interactive mode selection (standard vs comparative simulations)
- Generates matplotlib figures showing population trajectories

**RatNutGnawModel.py**: Taphonomic analysis quantifying preservation bias in gnaw mark evidence
- Monte Carlo simulations for statistical validation
- Multiple modeling approaches (simple probability, fragment size, geometric overlap)
- Sensitivity analysis across parameter ranges

### R Components

**R-code/R-code-for-paper.R**: Archaeological faunal data analysis
- Tests boom-bust vs fallback food hypotheses
- Analyzes rat remains from multiple excavations (1986-2005)
- Generates publication-quality figures using ggplot2

### Dependencies

Python packages: numpy, matplotlib, scipy
R packages: ggplot2, dplyr, tidyr, gridExtra, scales, knitr, svglite

## Key Parameters

### Ecological Model
- Rat growth rate: 2.5 (accounting for reproductive cycles)
- Palm carrying capacity: 15 million trees initially
- Seed predation efficiency: 95%
- Human population: 20-3000 individuals

### Taphonomic Model
- Gnaw hole coverage: 10-40% of shell surface
- Fragment size distribution: 1-20% of original shell area
- Monte Carlo iterations: 1000-10000 for statistical stability