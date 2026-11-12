# Monthly average gas prices by location from md_gas_prices.csv
# Groups by the month of scraped_date (column A) and location (column B),
# then averages regular, mid_grade, premium and diesel (columns C-F).

# install.packages(c("dplyr", "readr"))  # run once if needed
library(dplyr)
library(readr)

# Set the working directory to the folder holding the CSV
setwd("~/Desktop/gas-prices")

gas <- read_csv("md_gas_prices.csv", show_col_types = FALSE)

monthly_avg_by_location <- gas %>%
  mutate(month = format(as.Date(scraped_date), "%Y-%m")) %>%
  group_by(location, month) %>%
  summarise(
    across(c(regular, mid_grade, premium, diesel),
           ~ round(mean(.x, na.rm = TRUE), 3)),
    .groups = "drop"
  ) %>%
  arrange(location, month)

print(monthly_avg_by_location, n = Inf)

# Optional: save the result
write_csv(monthly_avg_by_location, "monthly_gas_averages_by_location.csv")
