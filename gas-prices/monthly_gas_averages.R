# Monthly average gas prices from md_gas_prices.csv
# Groups by the month of scraped_date (column A) and averages
# regular, mid_grade, premium and diesel (columns C-F).

# install.packages(c("dplyr", "readr"))  # run once if needed
library(dplyr)
library(readr)

# Set the working directory to the folder holding the CSV
# (or use Session > Set Working Directory > To Source File Location in RStudio)
setwd("~/Desktop/gas-prices")

gas <- read_csv("md_gas_prices.csv", show_col_types = FALSE)

monthly_avg <- gas %>%
  mutate(month = format(as.Date(scraped_date), "%Y-%m")) %>%
  group_by(month) %>%
  summarise(
    across(c(regular, mid_grade, premium, diesel),
           ~ round(mean(.x, na.rm = TRUE), 3)),
    .groups = "drop"
  ) %>%
  arrange(month)

print(monthly_avg)

# Optional: save the result
write_csv(monthly_avg, "monthly_gas_averages.csv")
