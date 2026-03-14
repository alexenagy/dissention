# Synthetic Control Method for Court Dissents Data
# Install required packages if needed
# install.packages("Synth")

library(Synth)

# Read your data (merged SCM dataset produced by dissent/scm/dataset.py)
data <- read.csv("data/processed/scm_dataset.csv")

# Check for balance
cat("\nChecking panel balance:\n")
court_year_counts <- aggregate(Year ~ Court, data = data, FUN = length)
print(court_year_counts)

# Create a numeric ID for each court (needed for Synth package)
courts <- unique(data$Court)
court_ids <- data.frame(Court = courts, CourtID = 1:length(courts))
data <- merge(data, court_ids, by = "Court")

# Identify NC's ID and other courts' IDs
nc_id <- court_ids$CourtID[court_ids$Court == "NC"]
control_ids <- court_ids$CourtID[court_ids$Court != "NC"]

print(paste("NC ID:", nc_id))
print("Control IDs:")
print(control_ids)

# Determine treatment year based on when NC experienced the intervention
treatment_year <- 2018

# Get the range of years
years <- sort(unique(data$Year))
pre_treatment_years <- years[years < treatment_year]
post_treatment_years <- years[years >= treatment_year]

print(paste("Pre-treatment years:", paste(pre_treatment_years, collapse = ", ")))
print(paste("Post-treatment years:", paste(post_treatment_years, collapse = ", ")))

# Prepare data for synthetic control
dataprep.out <- dataprep(
  foo = data,
  predictors = c("CampaignFinance", "CourtProf2019", 
                 "CapAppeals", "CapLowerLag1", 
                 "CrimProcDocket", "IdeoSpread", 
                 "CitizenIdeo", "GovtIdeo",
                 "TermLength", "NumJustices", "ElecStruct", 
                 "ElecCompete", "Opinions"),
  predictors.op = "mean",
  time.predictors.prior = pre_treatment_years,
  dependent = "DissentRate",
  unit.variable = "CourtID",
  unit.names.variable = "Court",
  time.variable = "Year",
  treatment.identifier = nc_id,
  controls.identifier = control_ids,
  time.optimize.ssr = pre_treatment_years,
  time.plot = years
)

# Run synthetic control
synth.out <- synth(data.prep.obj = dataprep.out, method = "BFGS")

# Get result tables
synth.tables <- synth.tab(dataprep.res = dataprep.out, 
                          synth.res = synth.out)

# Print results
cat("\n=== UNIT WEIGHTS ===\n")
cat("Weights assigned to each control court:\n")
weights_df <- data.frame(
  Court = court_ids$Court[match(rownames(synth.tables$tab.w), 
                                court_ids$CourtID)],
  Weight = synth.tables$tab.w[,1]
)
weights_df <- weights_df[weights_df$Weight > 0.001, ]  # Show only meaningful weights
print(weights_df)

cat("\n=== PREDICTOR BALANCE ===\n")
cat("Comparison of covariates between NC and Synthetic NC:\n")
print(synth.tables$tab.pred)

cat("\n=== VARIABLE WEIGHTS (V) ===\n")
cat("Importance of each predictor in creating synthetic control:\n")
print(synth.tables$tab.v)

# Plot results: NC vs Synthetic NC
png("reports/figures/nc-scm-plots.png",
    width = 900, height = 800, res = 120)

par(mfrow = c(2, 1), mar = c(4, 4, 3, 2))

# Plot 1: Treated vs Synthetic
path.plot(
  synth.res = synth.out, 
  dataprep.res = dataprep.out,
  Ylab = "Dissent Rate",
  Xlab = "Year",
  Legend = c("NC (Treated)", "Synthetic NC"),
  Legend.position = "topleft",
  Main = "North Carolina vs Synthetic Control: Dissents"
)
abline(v = treatment_year, lty = 2, col = "red", lwd = 2)

# Plot 2: Gap between treated and synthetic
gaps.plot(
  synth.res = synth.out, 
  dataprep.res = dataprep.out,
  Ylab = "Gap in Dissent Rate",
  Xlab = "Year",
  Main = "Treatment Effect: NC - Synthetic NC"
)
abline(v = treatment_year, lty = 2, col = "red", lwd = 2)
abline(h = 0, lty = 2, col = "gray")

dev.off()

# Calculate MSPE for pre and post-treatment periods
treated <- dataprep.out$Y1plot
synthetic <- dataprep.out$Y0plot %*% synth.out$solution.w

# Pre-treatment MSPE
pre.treated <- treated[rownames(treated) %in% pre_treatment_years, ]
pre.synthetic <- synthetic[rownames(synthetic) %in% pre_treatment_years, ]
mspe.pre <- mean((pre.treated - pre.synthetic)^2)

# Post-treatment MSPE
post.treated <- treated[rownames(treated) %in% post_treatment_years, ]
post.synthetic <- synthetic[rownames(synthetic) %in% post_treatment_years, ]
mspe.post <- mean((post.treated - post.synthetic)^2)

cat("\n=== MODEL FIT ===\n")
cat("Pre-treatment MSPE:", round(mspe.pre, 4), "\n")
cat("Post-treatment MSPE:", round(mspe.post, 4), "\n")
cat("Ratio (Post/Pre):", round(mspe.post / mspe.pre, 2), "\n")

# Calculate average treatment effect
ate <- mean(post.treated - post.synthetic)
cat("\nAverage Treatment Effect on Dissents:", round(ate, 3), "\n")