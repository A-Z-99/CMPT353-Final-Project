import sys
import pandas as pd
from scipy.stats import f_oneway
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import calendar
from collections import OrderedDict

input_filename = sys.argv[1]
output_filename = sys.argv[2]
months = pd.read_csv(input_filename)

# Convert 'Date' column to datetime type
months['Date'] = pd.to_datetime(months['Date'])

# Extract month from 'Date' column and map to month names
months['Month'] = months['Date'].dt.month.map(lambda x: calendar.month_name[x])

# Drop rows with missing values
months.dropna(inplace=True)

# Write data to output file
months.to_csv("../datasets/months/monthsData.csv", index=False)

# Define an ordered dictionary to maintain the order of months
month_order = OrderedDict((month, None) for month in calendar.month_name[1:])

# Calculate percent change averages for each month
month_means = months.groupby('Month')['Percent change'].mean().loc[month_order.keys()]

# Perform Tukey test
tukey_results = pairwise_tukeyhsd(months['Percent change'], months['Month'])


# Perform ANOVA test
anova = f_oneway(*[group['Percent change'] for name, group in months.groupby('Month')])

# Write ANOVA results and percent change averages to summary file
with open("summary.txt", 'w') as f:
    sys.stdout = f
    print("ANOVA p-value: {}\n".format(anova.pvalue))
    print("Percent Daily Growth Averages by Month:")
    print(month_means.to_string())
    print("\nTukey Test Results:")
    print(str(tukey_results))
