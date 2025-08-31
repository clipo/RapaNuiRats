# Dependency Management Guide

This project uses modern dependency management for both Python and R components to ensure reproducibility.

## Overview

- **Python**: Virtual environments with `pip` and `requirements.txt`
- **R**: `renv` package management (modern replacement for packrat)

## Quick Setup

### Python Environment
```bash
cd python
bash setup_env.sh  # Automated setup
# or manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### R Environment
```r
# In R, from R-code directory:
setwd("R-code")
renv::restore()  # Installs exact package versions
```

## Project Structure

```
rapanuirats/
├── python/
│   ├── requirements.txt           # Core Python dependencies
│   ├── requirements-dev.txt       # Development dependencies
│   ├── setup_env.sh              # Setup script
│   └── README_DEPENDENCIES.md    # Python-specific guide
│
├── R-code/
│   ├── renv.lock                 # R package lockfile
│   ├── .Rprofile                 # Auto-activates renv
│   ├── renv/                     # Project library
│   ├── setup_renv.R              # Setup script
│   └── README_DEPENDENCIES.md    # R-specific guide
│
└── DEPENDENCIES.md               # This file
```

## Requirements

### System Requirements
- **Python**: 3.8 or higher
- **R**: 4.3.0 or higher (4.4+ works but may show warnings)
- **OS**: Windows, macOS, or Linux

### Python Packages
Core dependencies:
- numpy==1.24.4
- scipy==1.11.4
- matplotlib==3.7.3

### R Packages
Via renv.lock:
- ggplot2 (3.4.4)
- dplyr (1.1.4)
- tidyr (1.3.0)
- gridExtra (2.3)
- scales (1.3.0)
- knitr (1.45)
- svglite (2.1.3)

## Reproducibility

Both environments use exact version pinning to ensure:
1. Consistent results across machines
2. Reproducible figure generation
3. Stable random number generation for Monte Carlo simulations

## Troubleshooting

### Python Issues
- **Import errors**: Ensure virtual environment is activated
- **Version conflicts**: Use exact versions in requirements.txt
- **matplotlib display**: May need GUI backend on some systems

### R Issues
- **Package installation fails**: Run `renv::restore()` from R-code directory
- **SVG export issues**: Install system cairo libraries
- **Version warnings**: Safe to ignore if packages load correctly

## For Developers

### Updating Dependencies
**Python**:
```bash
pip install --upgrade package_name
pip freeze > requirements-frozen.txt  # Capture exact versions
```

**R**:
```r
renv::update("package_name")
renv::snapshot()  # Update lockfile
```

### Adding New Dependencies
**Python**:
1. Install: `pip install new_package`
2. Add to requirements.txt with version
3. Update requirements-dev.txt if development tool

**R**:
1. Install: `install.packages("new_package")`
2. Update lockfile: `renv::snapshot()`
3. Commit updated renv.lock

## Citation

When using this code, please ensure you can reproduce the exact computational environment:

```
Computational Environment:
- Python 3.8+ with numpy 1.24.4, scipy 1.11.4, matplotlib 3.7.3
- R 4.3.0+ with packages specified in renv.lock
- Full dependency specifications available at: https://github.com/[repository]
```