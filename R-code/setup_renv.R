# Setup script for R dependency management using renv
# This replaces the older packrat system with the modern renv approach

# Install renv if not already installed
if (!requireNamespace("renv", quietly = TRUE)) {
  install.packages("renv")
}

# Load renv
library(renv)

# Initialize renv project
renv::init(project = ".", bare = FALSE)

# Install required packages for the analysis
required_packages <- c(
  "ggplot2",      # For creating publication-quality plots
  "dplyr",        # For data manipulation 
  "tidyr",        # For data reshaping
  "gridExtra",    # For arranging multiple plots
  "scales",       # For axis formatting
  "knitr",        # For document generation
  "svglite"       # For saving vector graphics
)

# Install packages
for (pkg in required_packages) {
  if (!requireNamespace(pkg, quietly = TRUE)) {
    install.packages(pkg)
  }
}

# Create a snapshot of the current library
renv::snapshot()

cat("\nrenv setup complete!\n")
cat("The following files have been created:\n")
cat("- renv.lock: lockfile with exact package versions\n")
cat("- .Rprofile: automatically activates renv for this project\n")
cat("- renv/: directory containing the project library\n")
cat("\nTo restore this environment on another machine, run:\n")
cat("  renv::restore()\n")