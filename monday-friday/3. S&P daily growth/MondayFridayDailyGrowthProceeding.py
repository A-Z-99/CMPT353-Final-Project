# Pairs Mondays with the Friday of the previous week

import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
from scipy.stats import wilcoxon
from scipy.stats import mannwhitneyu

input_file = sys.argv[1]
if len(sys.argv) == 3:
    suffix = sys.argv[2]
else:
    suffix = ""

# Read CSV files into pandas DataFrame
data = pd.read_csv(input_file)

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
mondays = mondays.rename(columns={'Date': 'Monday', 'Value': 'Monday_value', 'Percent change': 'Monday_growth'})
fridays= fridays.rename(columns={'Date': 'Friday', 'Value': 'Friday_value', 'Percent change': 'Friday_growth'})

# Merge Mondays with their respective preceding Fridays based on the date difference of 3 days
pairs = pd.merge_asof(mondays.sort_values('Monday'), fridays.sort_values('Friday'), 
                            left_on='Monday', right_on='Friday', direction='backward', tolerance=pd.Timedelta(days=3))

# Change indicates the change between the value on Friday and the value on Monday
pairs['change percent'] = pairs['Monday_growth'] - pairs['Friday_growth'] 

# Check for missing values in the 'change percent' column
missing_values = pairs['change percent'].isnull().any()

if missing_values:
    print("Missing values detected. Handling missing values...")
    
    # Drop rows with missing values
    pairs.dropna(subset=['change percent'], inplace=True)

pairs['Growth difference'] = pairs['change percent'].round(2)

# Save DataFrame to CSV file using the temporary alias
pairs.to_csv("proceeding" + suffix + ".csv", index=False, columns=['Monday', 'Friday', 'Monday_growth', 'Friday_growth', 'Growth difference'])

# Drop the temporary alias after saving
pairs.drop(columns=['Growth difference'], inplace=True)

"""
Generate plots
"""

# Plot date on the x-axis and value on the y-axis
pairs.plot(x='Monday', y='change percent', kind='scatter')
plt.axhline(y=0, color='black', linestyle='--')

# Add labels and title
plt.xlabel('Date')
plt.ylabel('Change in growth percent')
plt.title('Difference in growth percent between Friday and Monday')
plt.grid(True)

plt.savefig("Growth percent Procede" + suffix + ".png")

# Plot histogram of percent changes

plt.figure(figsize=(10, 6))

plt.hist(pairs['change percent'], bins=20, color='blue', alpha=0.7)

# Add vertical line at mean
mean_percent_change = pairs['change percent'].mean()
plt.axvline(x=mean_percent_change, color='red', linestyle='--', label=f'Mean: {mean_percent_change:.2f}')  


# Add labels and title
plt.xlabel('Difference in growth percent')
plt.ylabel('Frequency')
plt.title('Histogram of Difference in growth percent between Friday and Monday')
plt.legend()
plt.savefig("Growth percent Histogram Procede" + suffix + ".png")


# Plot growths in a histogram together
# Create histogram for Monday percent changes
# Define bin edges for equal bin size
mondays.dropna(subset=['Monday_growth'], inplace=True)
fridays.dropna(subset=['Friday_growth'], inplace=True)
plt.clf()
bin_edges = np.linspace(min(min(mondays['Monday_growth']), min(fridays['Friday_growth'])),
                        max(max(mondays['Monday_growth']), max(fridays['Friday_growth'])), 31)

# Create histogram for Monday percent changes
plt.hist(mondays['Monday_growth'], bins=bin_edges, color='skyblue', alpha=0.7, label='Monday')

# Create histogram for Friday percent changes
plt.hist(fridays['Friday_growth'], bins=bin_edges, color='lightgreen', alpha=0.4, label='Friday')

# Calculate and plot mean lines
mean_monday = mondays['Monday_growth'].mean()
mean_friday = fridays['Friday_growth'].mean()
plt.axvline(x=mean_monday, color='blue', linestyle='--', label=f'Monday mean: {mean_monday:.2f}')
plt.axvline(x=mean_friday, color='green', linestyle='--', label=f'Friday mean: {mean_friday:.2f}')

# Add labels and title
plt.xlabel('Daily growths')
plt.ylabel('Frequency')
plt.title('Distribution of Daily Growth for Mondays and Fridays')

# Add a legend
plt.legend()
plt.savefig("Daily growth comparison" + suffix + ".png")

"""
Perform statistical tests
"""
# Perform the MannWhitneyU test
mwu = mannwhitneyu(pairs['Monday_growth'], pairs['Friday_growth'])

# Perform the Wilcoxon signed-rank test
wilcoxon_test = wilcoxon(pairs['change percent'], zero_method='wilcox')

# Calculate the number of negative changes
negative_changes = (pairs['change percent'] < 0).sum()

# Total number of changes
total_changes = len(pairs)


with open("summary growths Procede" + suffix + ".txt", 'w') as f:
    # Redirect stdout to the file
    import sys
    sys.stdout = f
    print("u-test p-value:", mwu.pvalue)
    print("Wilcoxon p-value:", wilcoxon_test.pvalue)
    print("Number of decreased growths:", negative_changes)
    print("Total pairs:", total_changes)
    print("Average monday growth percent:", pairs['Monday_growth'].mean())
    print("Average friday growth percent:", pairs['Friday_growth'].mean())

