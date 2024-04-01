import pandas as pd
import os
import matplotlib.pyplot as plt
from scipy.stats import wilcoxon
from scipy.stats import binom

# Path to the directory containing the CSV files
data_2006_path = "2006 data"
data_2016_path = "2016 data"

# Function to read all CSV files in a directory into a single DataFrame
def read_csv_files(directory):
    all_files = os.listdir(directory)
    df_list = []
    for filename in all_files:
        if filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            df = pd.read_csv(file_path, header=None)
            df_list.append(df)
    return pd.concat(df_list, ignore_index=True)

# Read CSV files into pandas DataFrame
data_2006_df = read_csv_files(data_2006_path)
data_2016_df = read_csv_files(data_2016_path)

column_labels = ['Date', 'Value', 'Day of week']
data_2006_df.columns = column_labels
data_2016_df.columns = column_labels

# print(data_2006_df.head())
# print(data_2016_df.head())

# Get rid of weekends
data_2006_df = data_2006_df[~data_2006_df['Day of week'].isin([1, 7])]
data_2016_df = data_2016_df[~data_2016_df['Day of week'].isin([1, 7])]

# Convert the date column to datetime type
data_2006_df['Date'] = pd.to_datetime(data_2006_df['Date'])
data_2016_df['Date'] = pd.to_datetime(data_2016_df['Date'])

# Get Monday-Friday pairs (Pair each Monday with the Friday that PROCEEDED it)
mondays_2006 = data_2006_df[data_2006_df['Day of week'] == 2]
mondays_2016 = data_2016_df[data_2016_df['Day of week'] == 2]
fridays_2006 = data_2006_df[data_2006_df['Day of week'] == 6]
fridays_2016 = data_2016_df[data_2016_df['Day of week'] == 6]

# Group Mondays and Fridays by week
mondays_2006['Week'] = mondays_2006['Date'].dt.isocalendar().week
mondays_2016['Week'] = mondays_2016['Date'].dt.isocalendar().week

# Rename columns to avoid conflicts after merge
mondays_2006 = mondays_2006.rename(columns={'Date': 'Monday', 'Value': 'Monday_value'})
fridays_2006 = fridays_2006.rename(columns={'Date': 'Friday', 'Value': 'Friday_value'})

mondays_2016 = mondays_2016.rename(columns={'Date': 'Monday', 'Value': 'Monday_value'})
fridays_2016 = fridays_2016.rename(columns={'Date': 'Friday', 'Value': 'Friday_value'})

# Merge Mondays with their respective preceding Fridays based on the date difference of 3 days
pairs_2006 = pd.merge_asof(mondays_2006.sort_values('Monday'), fridays_2006.sort_values('Friday'), 
                            left_on='Monday', right_on='Friday', direction='backward', tolerance=pd.Timedelta(days=3))

pairs_2016 = pd.merge_asof(mondays_2016.sort_values('Monday'), fridays_2016.sort_values('Friday'), 
                            left_on='Monday', right_on='Friday', direction='backward', tolerance=pd.Timedelta(days=3))

print(pairs_2006.head())
print(pairs_2016.head())

# Change indicates the change between the value on Friday and the value on Monday
pairs_2006['change'] = pairs_2006['Monday_value'] - pairs_2006['Friday_value'] 
pairs_2016['change'] = pairs_2016['Monday_value'] - pairs_2016['Friday_value']
pairs_2006['change percent'] = pairs_2006['change']/pairs_2006['Friday_value']*100
pairs_2016['change percent'] = pairs_2016['change']/pairs_2016['Friday_value']*100

""""""""

# Plot date on the x-axis and value on the y-axis for 2006 data
pairs_2006.plot(x='Monday', y='change percent', kind='scatter')

# Add labels and title
plt.xlabel('Date')
plt.ylabel('Change')
plt.title('Percent change from Friday to Monday (2006)')

# Show the plot
plt.show()

# Plot date on the x-axis and value on the y-axis for 2016 data
pairs_2016.plot(x='Monday', y='change percent', kind='scatter')

# Add labels and title
plt.xlabel('Date')
plt.ylabel('Change')
plt.title('Percent change from Friday to Monday (2016)')

# Show the plot
plt.show()

# Check for missing values in the 'change percent' column
missing_values_2006 = pairs_2006['change percent'].isnull().any()
missing_values_2016 = pairs_2016['change percent'].isnull().any()

if missing_values_2006 or missing_values_2016:
    print("Missing values detected. Handling missing values...")
    
    # Drop rows with missing values
    pairs_2006.dropna(subset=['change percent'], inplace=True)
    pairs_2016.dropna(subset=['change percent'], inplace=True)

# Perform the Wilcoxon signed-rank test
statistic_2006, p_value_2006 = wilcoxon(pairs_2006['change percent'], zero_method='wilcox')
statistic_2016, p_value_2016 = wilcoxon(pairs_2016['change percent'], zero_method='wilcox')

print("2006 - Wilcoxon Statistic:", statistic_2006)
print("2006 - p-value:", p_value_2006)

print("2016 - Wilcoxon Statistic:", statistic_2016)
print("2016 - p-value:", p_value_2016)

"""
Perform Binomial test
"""
# Calculate the number of negative changes
negative_changes_2006 = (pairs_2006['change percent'] < 0).sum()
negative_changes_2016 = (pairs_2016['change percent'] < 0).sum()

# Total number of changes
total_changes_2006 = len(pairs_2006)
total_changes_2016 = len(pairs_2016)

# Perform the sign test
p_value_2006 = binom.cdf(negative_changes_2006, total_changes_2006, 0.5)
p_value_2016 = binom.cdf(negative_changes_2016, total_changes_2016, 0.5)

print("2006 - Number of Negative Changes:", negative_changes_2006)
print("2006 - Total Changes:", total_changes_2006)
print("2006 - Probability of Negative Change:", p_value_2006)

print("2016 - Number of Negative Changes:", negative_changes_2016)
print("2016 - Total Changes:", total_changes_2016)
print("2016 - Probability of Negative Change:", p_value_2016)

print("2006 - Average monday value:", pairs_2006['Monday_value'].mean())
print("2006 - Average friday value:", pairs_2006['Friday_value'].mean())
print("2016 - Average monday value:", pairs_2016['Monday_value'].mean())
print("2016 - Average friday value:", pairs_2016['Friday_value'].mean())

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
