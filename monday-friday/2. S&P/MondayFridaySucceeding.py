# Pairs Mondays with the Friday on the same week

import pandas as pd
import sys
import matplotlib.pyplot as plt
from scipy.stats import wilcoxon
from scipy.stats import mannwhitneyu

input_file = sys.argv[1]

# Read CSV files into pandas DataFrame
data = pd.read_csv(input_file)

# Get rid of weekends 
data = data[data['Day of week'] <= 4]

# Convert the date column to datetime type
data['Date'] = pd.to_datetime(data['Date'])

# Get Monday-Friday pairs (Pair each Monday with the Friday that Succeeded it)
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

# Check for missing values in the 'change percent' column
missing_values = pairs['change percent'].isnull().any()

if missing_values:
    print("Missing values detected. Handling missing values...")
    
    # Drop rows with missing values
    pairs.dropna(subset=['change percent'], inplace=True)

"""
Generate plots
"""

# Plot date on the x-axis and value on the y-axis
pairs.plot(x='Monday', y='change percent', kind='scatter', color='green')
plt.axhline(y=0, color='black', linestyle='--')

# Add labels and title
plt.xlabel('Date')
plt.ylabel('Change')
plt.title('Percent change from Monday to Friday')
plt.grid(True)

plt.savefig("Percent change Succeed.png")

# Plot histogram of percent changes

plt.figure(figsize=(10, 6))

plt.hist(pairs['change percent'], bins=20, color='green', alpha=0.7)

# Add vertical line at mean
mean_percent_change = pairs['change percent'].mean()
plt.axvline(x=mean_percent_change, color='red', linestyle='--', label=f'Mean: {mean_percent_change:.2f}')  


# Add labels and title
plt.xlabel('Percent Change')
plt.ylabel('Frequency')
plt.title('Histogram of Percent Changes from Monday to Friday')
plt.legend()
plt.savefig("Percent Changes Histogram Succeed.png")

"""
Perform statistical tests
"""
# Perform the MannWhitneyU test
mwu = mannwhitneyu(pairs['Monday_value'], pairs['Friday_value'])

# Perform the Wilcoxon signed-rank test
wilcoxon_test = wilcoxon(pairs['change percent'], zero_method='wilcox')

# Calculate the number of negative changes
negative_changes = (pairs['change percent'] < 0).sum()

# Total number of changes
total_changes = len(pairs)


with open('summary Succeed.txt', 'w') as f:
    # Redirect stdout to the file
    import sys
    sys.stdout = f
    print("u-test p-value:", mwu.pvalue)
    print("Wilcoxon p-value:", wilcoxon_test.pvalue)
    print("Number of Negative Changes:", negative_changes)
    print("Total Changes:", total_changes)
    print("Average monday value:", pairs['Monday_value'].mean())
    print("Average friday value:", pairs['Friday_value'].mean())


"""
Plot values
"""
plt.clf()
plt.grid(True)
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

plt.savefig("Values.png")
