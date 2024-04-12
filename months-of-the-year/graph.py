import sys
import pandas as pd
import matplotlib.pyplot as plt
import calendar

input_filename = sys.argv[1]

# Read data from CSV file
months = pd.read_csv(input_filename)

# # Convert 'Date' column to datetime type
# months['Date'] = pd.to_datetime(months['Date'])

# # Extract month from 'Date' column and map to month names
# months['Month'] = months['Date'].dt.month.map(lambda x: calendar.month_name[x])

# Plot histograms for each month on the same plot
plt.figure(figsize=(10, 6))

for month_num in range(1, 13):
    month_name = calendar.month_name[month_num]
    month_data = months[months['Month'] == month_name]['Percent change']
    plt.hist(month_data, bins=10, alpha=0.35, edgecolor='black', label=month_name)

plt.axhline(y=0, color='black', linewidth=0.5)  # Add a horizontal line at y=0
plt.legend()
plt.title('Histogram of Daily Percent Growths for Each Month')
plt.xlabel('Daily Percent Growth')
plt.ylabel('Frequency')
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig("months.png")