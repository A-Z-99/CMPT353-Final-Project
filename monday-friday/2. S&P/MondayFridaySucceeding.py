import pandas as pd
import sys
import matplotlib.pyplot as plt
from scipy.stats import wilcoxon
from scipy.stats import binom

input_file = sys.argv[1]

# Read CSV files into pandas DataFrame
data = pd.read_csv(input_file)

# print(data_2006_df.head())
# print(data_2016_df.head())

# Get rid of weekends 
data = data[data['Day of week'] <= 4]

# Convert the date column to datetime type
data['Date'] = pd.to_datetime(data['Date'])

# Get Monday-Friday pairs (Pair each Monday with the Friday that PROCEEDED it)
mondays = data[data['Day of week'] == 0]
fridays = data[data['Day of week'] == 4]

# Group Mondays and Fridays by week
mondays['Week'] = mondays['Date'].dt.isocalendar().week
fridays['Week'] = fridays['Date'].dt.isocalendar().week

# Rename columns to avoid conflicts after merge
mondays = mondays.rename(columns={'Date': 'Monday', 'Value': 'Monday_value'})
fridays= fridays.rename(columns={'Date': 'Friday', 'Value': 'Friday_value'})

# Merge Mondays with their respective preceding Fridays based on the date difference of 4 days
pairs = pd.merge_asof(mondays.sort_values('Monday'), fridays.sort_values('Friday'), 
                            left_on='Monday', right_on='Friday', direction='forward', tolerance=pd.Timedelta(days=4))

# Change indicates the change between the value on Monday and that of Friday
pairs['change'] = pairs['Friday_value'] - pairs['Monday_value'] 
pairs['change percent'] = pairs['change']/pairs['Monday_value']*100

""""""""

# Plot date on the x-axis and value on the y-axis for 2006 data
pairs.plot(x='Monday', y='change percent', kind='scatter')

# Add labels and title
plt.xlabel('Date')
plt.ylabel('Change')
plt.title('Percent change from Monday to Friday')

# Show the plot
plt.show()


# Check for missing values in the 'change percent' column
missing_values_2006 = pairs['change percent'].isnull().any()
missing_values_2016 = pairs['change percent'].isnull().any()

if missing_values_2006 or missing_values_2016:
    print("Missing values detected. Handling missing values...")
    
    # Drop rows with missing values
    pairs.dropna(subset=['change percent'], inplace=True)
    pairs.dropna(subset=['change percent'], inplace=True)

# Perform the Wilcoxon signed-rank test
statistic, p_value = wilcoxon(pairs['change percent'], zero_method='wilcox')

print("Wilcoxon Statistic:", statistic)
print("p-value:", p_value)


"""
Perform Binomial test
"""
# Calculate the number of negative changes
negative_changes = (pairs['change percent'] < 0).sum()

# Total number of changes
total_changes = len(pairs)

# Perform the sign test
p_value = binom.cdf(negative_changes, total_changes, 0.5)

print("Number of Negative Changes:", negative_changes)
print("Total Changes:", total_changes)
print("Probability of Negative Change:", p_value)

print("Average monday value:", pairs['Monday_value'].mean())
print("Average friday value:", pairs['Friday_value'].mean())
print("Average percent change:", pairs['change percent'].mean())


# Plot all Monday values in blue
plt.plot(pairs['Monday'], pairs['Monday_value'], color='blue', label='Monday')

# Plot all Friday values in red
plt.plot(pairs['Friday'], pairs['Friday_value'], color='red', label='Friday')

# Add labels and title
plt.xlabel('Date')
plt.ylabel('Value')
plt.title('Monday and Friday Values')

# Show legend
plt.legend()

# Show the plot
plt.show()

# anomalies = pairs[pairs['change percent'].abs() > 3 ]
# print(anomalies)

# # Plot date on the x-axis and value on the y-axis for 2006 data
# data_2006_df.plot(x='Date', y='Value', kind='line')

# # Add labels and title
# plt.xlabel('Date')
# plt.ylabel('Value')
# plt.title('Plot of Value over Time (2006)')

# # Show the plot
# plt.show()

# # Plot date on the x-axis and value on the y-axis for 2016 data
# data_2016_df.plot(x='Date', y='Value', kind='line')

# # Add labels and title
# plt.xlabel('Date')
# plt.ylabel('Value')
# plt.title('Plot of Value over Time (2016)')

# # Show the plot
# plt.show()
