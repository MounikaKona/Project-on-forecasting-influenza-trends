# Comparison of the proportion of positive cases of different variants
# (A, B, H1N1, H3N2) of influenza over the years.
library(lubridate)
library(dplyr)
library(tidyverse)
library(zoo)
library(ggplot2)
data = read.csv("influenza_Surveillance_Weekly.csv")
names(data)
colnames(data) = tolower(colnames(data))
# total missing values
sum(is.na(data))
#
data$week_start = mdy(data$week_start)
data$week_end = mdy(data$week_end)

data['lab_flu_positive']

data = data %>%
  mutate(year = year(week_start))

influenza_types = data[,c('year',
                          'lab_tot_a_positive', 
                          'lab_tot_b_positive', 
                          'lab_tot_h1n1_positive',
                        'lab_tot_h3n2_positive')]


Types_change = aggregate(influenza_types[,2:5], by = list(year =influenza_types$year), sum)


Types_change <- Types_change %>%
  mutate(total_positive = lab_tot_a_positive 
         + lab_tot_b_positive + 
           lab_tot_h1n1_positive +
           lab_tot_h3n2_positive)

Types_change$prop_a = Types_change$lab_tot_a_positive/ Types_change$total_positive*100

Types_change$prop_b = Types_change$lab_tot_b_positive/ Types_change$total_positive*100
Types_change$prop_h1n1 = Types_change$lab_tot_h1n1_positive/ Types_change$total_positive*100
Types_change$prop_h3n2 = Types_change$lab_tot_h3n2_positive/ Types_change$total_positive*100



ggplot(Types_change, aes(x = year)) +
  geom_line(aes(y = prop_a, color = "A")) +
  geom_line(aes(y = prop_b, color = "B")) +
  geom_line(aes(y = prop_h1n1, color = "H1N1")) +
  geom_line(aes(y = prop_h3n2, color = "H3N2")) +
  scale_color_manual(values = c("red", "blue", "green", "purple")) +
  labs(x = "Year", y = "Proportion of Positive Tests", color = "Influenza Type") +
  scale_x_continuous(limits = c(2015, 2023), breaks = seq(2015, 2023, by = 1)) 

# The number of hospitalizations in the ICU due to influenza over the years.

names(data)

icu =  data[,c('year', 'hosp_flu_icu_weekly')]

Yearly_icu = data %>%
  group_by(year) %>%
  summarise(total_icu = sum(hosp_flu_icu_weekly))





ggplot(Yearly_icu, aes(x=year, y=total_icu)) +
  geom_bar(stat="identity", fill="blue") +
  xlab("Year") +
  ylab("Total ICU hospitalizations") +
  ggtitle("Total ICU hospitalizations per year") +
  theme_minimal()+
  scale_x_continuous(limits = c(2015, 2023), breaks = seq(2015, 2023, by = 1)) 


###############################################################################

# Monthly Time series of total influenza-positive cases and total samples tested over the years.
monthly_cases = read.csv("monthly_cases.csv")

# not enough data points in 2015, removing first three rows.

monthly_cases = monthly_cases %>% slice(4:n())


head(monthly_cases)
monthly_cases$month_year <- as.Date(paste0(monthly_cases$month_year, "-01"), format = "%Y-%m-%d")


monthly_cases <- monthly_cases %>%
  mutate(year = year(month_year))
str(monthly_cases)



ggplot(monthly_cases, aes(x = month_year, y = total_sample_tested, group = year, color = factor(year))) +
  geom_line(aes(linetype = "Total Sample Tested", size = 1)) +
  geom_line(aes(y = total_flu_positive, linetype = "Total Flu Positive", size = 1.5)) +
  labs(x = "Date", y = "Total Sample Tested", color = "Year", linetype = "") +
  ggtitle("Total Sample Tested and Total Flu Positive by Month and Year") +
  scale_x_date(date_breaks = "6 month", date_labels = "%b %Y") +
  scale_linetype_manual(name = "", values = c("Total Sample Tested" = "solid", "Total Flu Positive" = "dashed")) +
  scale_size(range = c(1, 1.5), guide = FALSE)









