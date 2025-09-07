# Rat Gnaw Mark Taphonomic Analysis

## Overview
This directory contains R implementations of Monte Carlo simulations demonstrating that 85% of palm nut shell fragments would lack visible gnaw marks even under 100% rat predation, due to geometric constraints.

## Key Scripts

### `rat_gnaw_taphonomy_advanced.R` (RECOMMENDED)
**Advanced geometric model with realistic constraints**
- Models gnaw marks as limited to thin rim (2-3% of shell) around hole edge
- Accounts for the critical difference between hole area (20%) and mark area (2-3%)
- Produces 85% fragments without marks under 100% predation
- Most realistic representation of actual taphonomic processes

### `rat_gnaw_taphonomy_final.R`
Copy of the advanced model for production use

### `rat_gnaw_taphonomy.R` 
Simple probability model (kept for comparison)
- Assumes marks throughout hole area
- Less realistic but demonstrates baseline effect

## Key Findings

The advanced model demonstrates:
1. **85% of fragments lack gnaw marks** even with 100% predation
2. **Geometric constraint is severe**: Gnaw marks limited to 2-3% rim, not 20% hole
3. **Fragment size has minimal effect** - even large fragments miss the narrow rim
4. **Validates paper claims** of 65-90% fragments lacking marks

## Critical Insight

The preservation bias arises from a 10x reduction in observable evidence:
- Gnaw **hole** = 20% of shell surface (where rat accessed nut)
- Gnaw **marks** = 2-3% of shell surface (only at hole rim where teeth scraped)
- Random fragmentation rarely captures this narrow rim
- Result: Most fragments appear "ungnawed" regardless of actual predation

## Implications

This quantitative model directly refutes arguments that ungnawed shell fragments indicate limited rat impact. The absence of gnaw marks is the EXPECTED outcome under intensive predation, not evidence against it.

## Running the Analysis

```r
# Run the advanced (recommended) model
source("rat_gnaw_taphonomy_advanced.R")

# This will:
# 1. Run 10,000 Monte Carlo simulations
# 2. Test sensitivity to fragment size and rim width
# 3. Generate Figure 4 showing the taphonomic model
# 4. Save results to ../figures/
```

## Output

- `Figure_4_advanced_taphonomic_model.png`: Comprehensive 5-panel figure
- `gnaw_mark_simulation_summary.csv`: Statistical results

## Citation

When using this analysis, please cite:
Hunt, T.L. & Lipo, C.P. (2025) "Reassessing the Role of Polynesian Rats (*Rattus exulans*) 
in Rapa Nui Deforestation" Journal of Archaeological Science (in press)