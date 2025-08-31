# Python Dependencies Management

This folder uses standard Python dependency management with `pip` and virtual environments.

## Quick Start

### Automatic Setup (Recommended)
```bash
bash setup_env.sh
```

### Manual Setup
```bash
# Create virtual environment
python3 -m venv venv

# Activate environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt
```

## Files

- **requirements.txt**: Core dependencies for running simulations
  - numpy==1.24.4
  - scipy==1.11.4
  - matplotlib==3.7.3

- **requirements-dev.txt**: Additional development dependencies
  - Testing tools (pytest, coverage)
  - Code quality (black, flake8, mypy)
  - Documentation (sphinx)
  - Profiling tools

- **setup_env.sh**: Automated setup script for Unix systems

## Running Simulations

After activating the virtual environment:

```bash
# Run ecological simulation
python rat_simulation.py

# Run taphonomic analysis
python RatNutGnawModel.py
```

## Updating Dependencies

To update dependencies while maintaining compatibility:

```bash
# Update within version constraints
pip install --upgrade -r requirements.txt

# Freeze current versions
pip freeze > requirements-frozen.txt
```

## Notes

- Python 3.8+ required
- Specific versions ensure reproducible results
- Monte Carlo simulations may produce slightly different results with different numpy versions due to RNG changes