# R Dependencies Management

This folder uses `renv` for reproducible R package management.

## Quick Start

### First Time Setup
```r
# In R, from the R-code directory:
source("setup_renv.R")
```

Or manually:
```r
# Install renv if needed
install.packages("renv")

# Restore packages from lockfile
renv::restore()
```

## Files

- **renv.lock**: Lockfile with exact package versions
- **.Rprofile**: Auto-activates renv for this project
- **renv/**: Project-specific library directory
- **setup_renv.R**: Setup script for initializing renv

## Required Packages

- **ggplot2** (3.4.4): Publication-quality plots
- **dplyr** (1.1.4): Data manipulation
- **tidyr** (1.3.0): Data reshaping
- **gridExtra** (2.3): Multiple plot arrangements
- **scales** (1.3.0): Axis formatting
- **knitr** (1.45): Document generation
- **svglite** (2.1.3): Vector graphics output

## Running Analysis

```r
# From R-code directory
source("R-code-for-paper.R")
```

This generates archaeological analysis figures in `../figures/`:
- `archaeological_temporal_decline.png/.svg`
- `archaeological_all_excavations.png/.svg`
- `archaeological_variability.png/.svg`

## Managing Dependencies

### Adding New Packages
```r
# Install new package
install.packages("newpackage")

# Update lockfile
renv::snapshot()
```

### Updating Packages
```r
# Update all packages
renv::update()

# Update specific package
renv::update("ggplot2")

# Save changes to lockfile
renv::snapshot()
```

### Sharing/Reproducing Environment
When someone clones this repository:
```r
# Restore exact package versions
renv::restore()
```

## Notes

- R 4.3.0+ recommended
- renv ensures exact reproducibility across machines
- Package versions locked to those used for publication figures
- SVG output requires system cairo libraries on some platforms