library(ggplot2)
library(dplyr)
library(tidyr)
library(gridExtra)
library(scales)
library(knitr)
library(svglite)

# Create directories for saving figures
if (!dir.exists("figures_png")) {
  dir.create("figures_png")
}
if (!dir.exists("figures_svg")) {
  dir.create("figures_svg")
}

# Skjølsvold 1987-1988 - MNI data
skjolsvold_rat <- data.frame(
  Layer = c("Cultural Layer (Earlier)", "Sand Layer (Later)"),
  Rat_MNI = c(300, 21),
  Total_MNI = c(3970, 3345),
  Stratigraphy = "Temporal"
)
skjolsvold_rat$Rat_Percent <- (skjolsvold_rat$Rat_MNI / skjolsvold_rat$Total_MNI) * 100

# Martinsson-Wallin & Crockford 1986-1988 - NISP data
mw_rat <- data.frame(
  Depth = c("230-240cm", "240-260cm", "270-280cm", "280-290cm", "290-300cm"),
  Depth_Numeric = c(235, 250, 275, 285, 295),
  Rat_NISP = c(12, 56, 26, 0, 1),
  Total_NISP = c(75, 336, 177, 4, 80),
  Stratigraphy = "Depth"
)
mw_rat$Rat_Percent <- (mw_rat$Rat_NISP / mw_rat$Total_NISP) * 100

# Steadman 1991 Units 1-3 - NISP data
steadman_u13_rat <- data.frame(
  Depth = c("Surface", "0-20", "20-40", "40-60", "60-80", "80-100", "100-120", ">120"),
  Depth_Numeric = c(0, 10, 30, 50, 70, 90, 110, 130),
  Rat_NISP = c(0, 252, 480, 616, 196, 44, 19, 536),
  Total_NISP = c(20, 912, 1382, 1163, 583, 174, 273, 1926),
  Stratigraphy = "Depth"
)
steadman_u13_rat$Rat_Percent <- (steadman_u13_rat$Rat_NISP / steadman_u13_rat$Total_NISP) * 100

# Steadman 1991 Unit 4 - NISP data
steadman_u4_rat <- data.frame(
  Depth = c("0/3-18/22", "18/22-37/40", "37/40-57/60"),
  Depth_Numeric = c(10, 30, 50),
  Rat_NISP = c(20, 60, 116),
  Total_NISP = c(166, 292, 420),
  Stratigraphy = "Depth"
)
steadman_u4_rat$Rat_Percent <- (steadman_u4_rat$Rat_NISP / steadman_u4_rat$Total_NISP) * 100

# Hunt & Lipo 2004 - NISP data
hl2004_rat <- data.frame(
  Level = paste("Level", c("I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII")),
  Level_Numeric = 1:12,
  Rat_NISP = c(35, 0, 119, 213, 132, 296, 806, 433, 269, 62, 18, 0),
  Total_NISP = c(77, 6, 204, 558, 385, 535, 1191, 805, 385, 102, 171, 1),
  Stratigraphy = "Level"
)
hl2004_rat$Rat_Percent <- (hl2004_rat$Rat_NISP / hl2004_rat$Total_NISP) * 100

# Hunt & Lipo 2005 - NISP data
hl2005_rat <- data.frame(
  Level = paste("Level", c("I", "II", "III", "IV", "V", "VI", "VII")),
  Level_Numeric = 1:7,
  Rat_NISP = c(0, 151, 4, 77, 58, 665, 179),
  Total_NISP = c(2, 263, 11, 100, 96, 1206, 435),
  Stratigraphy = "Level"
)
hl2005_rat$Rat_Percent <- (hl2005_rat$Rat_NISP / hl2005_rat$Total_NISP) * 100


#| label: fig-temporal-decline
#| fig-cap: "Temporal changes in rat abundance from Skjølsvold's 1987-1988 excavation at Anakena. (A) Raw MNI counts show 93% decrease from earlier to later deposits. (B) Rats as percentage of total fauna decline from 7.6% to 0.6%. (C) Comparison with marine vs. terrestrial fauna shows marine intensification (91% to 99%) occurring simultaneously with rat decline."
#| fig-height: 10

# Save as PNG
png("figures_png/fig_temporal_decline.png", width = 10, height = 10, units = "in", res = 300)
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
marine_pct <- c(91.3, 99.1)
terrestrial_pct <- c(7.6, 0.7)
comparison_data <- rbind(marine_pct, terrestrial_pct)
colnames(comparison_data) <- c("Earlier\n(Cultural Layer)", "Later\n(Sand Layer)")

barplot(comparison_data, 
        beside = TRUE,
        main = "C. Marine vs. Terrestrial Fauna Over Time",
        ylab = "Percentage",
        col = c("blue", "brown"),
        legend = c("Marine", "Terrestrial"),
        args.legend = list(x = "topright", bty = "n"),
        ylim = c(0, 120))
dev.off()

# Save as SVG
svglite("figures_svg/fig_temporal_decline.svg", width = 10, height = 10)
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
marine_pct <- c(91.3, 99.1)
terrestrial_pct <- c(7.6, 0.7)
comparison_data <- rbind(marine_pct, terrestrial_pct)
colnames(comparison_data) <- c("Earlier\n(Cultural Layer)", "Later\n(Sand Layer)")

barplot(comparison_data, 
        beside = TRUE,
        main = "C. Marine vs. Terrestrial Fauna Over Time",
        ylab = "Percentage",
        col = c("blue", "brown"),
        legend = c("Marine", "Terrestrial"),
        args.legend = list(x = "topright", bty = "n"),
        ylim = c(0, 120))
dev.off()

# Display in R/RStudio
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
marine_pct <- c(91.3, 99.1)
terrestrial_pct <- c(7.6, 0.7)
comparison_data <- rbind(marine_pct, terrestrial_pct)
colnames(comparison_data) <- c("Earlier\n(Cultural Layer)", "Later\n(Sand Layer)")

barplot(comparison_data, 
        beside = TRUE,
        main = "C. Marine vs. Terrestrial Fauna Over Time",
        ylab = "Percentage",
        col = c("blue", "brown"),
        legend = c("Marine", "Terrestrial"),
        args.legend = list(x = "topright", bty = "n"),
        ylim = c(0, 120))


#| label: fig-all-excavations
#| fig-cap: "Rat abundance patterns across all Anakena excavations (1986-2005). Rat percentages by depth/level show high variability within and between excavations."
#| fig-height: 10

# Standardize column names before combining
# For datasets with Depth columns
mw_rat_std <- mw_rat %>%
  rename(Context = Depth, Context_Numeric = Depth_Numeric) %>%
  mutate(Excavation = "MW 1986-88", Year = 1986)

steadman_u13_rat_std <- steadman_u13_rat %>%
  rename(Context = Depth, Context_Numeric = Depth_Numeric) %>%
  mutate(Excavation = "Steadman 1991 U1-3", Year = 1991)

steadman_u4_rat_std <- steadman_u4_rat %>%
  rename(Context = Depth, Context_Numeric = Depth_Numeric) %>%
  mutate(Excavation = "Steadman 1991 U4", Year = 1991)

# For datasets with Level columns
hl2004_rat_std <- hl2004_rat %>%
  rename(Context = Level, Context_Numeric = Level_Numeric) %>%
  mutate(Excavation = "Hunt & Lipo 2004", Year = 2004)

hl2005_rat_std <- hl2005_rat %>%
  rename(Context = Level, Context_Numeric = Level_Numeric) %>%
  mutate(Excavation = "Hunt & Lipo 2005", Year = 2005)

# Now combine all standardized data
all_rat_data <- bind_rows(
  mw_rat_std,
  steadman_u13_rat_std,
  steadman_u4_rat_std,
  hl2004_rat_std,
  hl2005_rat_std
)

# Calculate mean rat percentages by excavation
mean_rats <- all_rat_data %>%
  filter(Total_NISP > 50) %>%  # Only well-sampled contexts
  group_by(Excavation, Year) %>%
  summarise(
    Mean_Rat_Percent = mean(Rat_Percent, na.rm = TRUE),
    n_samples = n(),
    .groups = 'drop'
  )

# Add Skjølsvold for temporal comparison
mean_rats <- bind_rows(mean_rats,
                       data.frame(Excavation = "Skjølsvold 1987-88",
                                  Year = 1987,
                                  Mean_Rat_Percent = mean(skjolsvold_rat$Rat_Percent),
                                  n_samples = 2))

# Print to verify all years are included
print("Mean rat percentages by year:")
print(mean_rats)

# Create multi-panel visualization
p1 <- ggplot(all_rat_data, aes(x = Context_Numeric, y = Rat_Percent)) +
  geom_point(size = 3, color = "darkred") +
  geom_line(color = "darkred", alpha = 0.5) +
  facet_wrap(~Excavation, scales = "free_x", ncol = 2) +
  theme_minimal(base_size = 12) +
  labs(title = "Rat Percentages",
       x = "Depth/Level", y = "Rat %") +
  theme(plot.title = element_text(size = 14, face = "bold"),
        panel.grid.minor = element_blank(),
        strip.text = element_text(face = "bold"))

# Save combined plot as PNG
png("figures_png/fig_all_excavations.png", width = 10, height = 10, units = "in", res = 300)
grid.arrange(p1, heights = c(1, 1))
dev.off()

# Save combined plot as SVG
svg("figures_svg/fig_all_excavations.svg", width = 10, height = 10)
grid.arrange(p1, heights = c(1, 1))
dev.off()

# Display in R/RStudio
grid.arrange(p1, heights = c(1, 1))


#| label: fig-variability
#| fig-cap: "Coefficients of variation in rat abundance across excavations. Values exceeding 100% (red dashed line) indicate high variability consistent with depositional rather than dietary patterns."
#| fig-height: 6

# Calculate CV for each excavation
cv_data <- data.frame(
  Excavation = c("Skjølsvold MNI", "MW 1986-88", "Steadman U1-3", 
                 "Steadman U4", "HL 2004", "HL 2005"),
  CV_Rat = c(
    sd(skjolsvold_rat$Rat_MNI) / mean(skjolsvold_rat$Rat_MNI) * 100,
    sd(mw_rat$Rat_NISP[mw_rat$Total_NISP > 20]) / mean(mw_rat$Rat_NISP[mw_rat$Total_NISP > 20]) * 100,
    sd(steadman_u13_rat$Rat_NISP) / mean(steadman_u13_rat$Rat_NISP) * 100,
    sd(steadman_u4_rat$Rat_NISP) / mean(steadman_u4_rat$Rat_NISP) * 100,
    sd(hl2004_rat$Rat_NISP[hl2004_rat$Total_NISP > 10]) / mean(hl2004_rat$Rat_NISP[hl2004_rat$Total_NISP > 10]) * 100,
    sd(hl2005_rat$Rat_NISP[hl2005_rat$Total_NISP > 10]) / mean(hl2005_rat$Rat_NISP[hl2005_rat$Total_NISP > 10]) * 100
  )
)

p3 <- ggplot(cv_data, aes(x = reorder(Excavation, CV_Rat), y = CV_Rat)) +
  geom_bar(stat = "identity", fill = "brown", alpha = 0.8) +
  coord_flip() +
  theme_minimal(base_size = 12) +
  labs(title = "High Variability in Rat Abundance Indicates Depositional Effects",
       subtitle = "Coefficients of variation > 100% in most excavations",
       x = "", y = "Coefficient of Variation (%)") +
  geom_hline(yintercept = 100, linetype = "dashed", color = "red", size = 1) +
  annotate("text", x = 1, y = 120, label = "High variability threshold", 
           color = "red", hjust = 0, size = 3.5) +
  theme(plot.title = element_text(size = 14, face = "bold"),
        plot.subtitle = element_text(size = 12, face = "italic"))

# Save as PNG
ggsave("figures_png/fig_variability.png", plot = p3, width = 10, height = 6, dpi = 300)

# Save as SVG
ggsave("figures_svg/fig_variability.svg", plot = p3, width = 10, height = 6)

# Display in R/RStudio
print(p3)

# Print summary message
cat("\nAll figures have been saved to:\n")
cat("PNG files: figures_png/\n")
cat("SVG files: figures_svg/\n")
cat("\nSaved files:\n")
cat("- fig_temporal_decline.png/.svg\n")
cat("- fig_all_excavations.png/.svg\n")
cat("- fig_variability.png/.svg\n")



# Update the final message
cat("\nAll figures have been saved to:\n")
cat("PNG files: figures_png/\n")
cat("SVG files: figures_svg/\n")
cat("\nSaved files:\n")
cat("- fig_temporal_decline.png/.svg\n")
cat("- fig_all_excavations.png/.svg\n")
cat("- fig_variability.png/.svg\n")
