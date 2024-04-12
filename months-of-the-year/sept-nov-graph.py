import sys
import pandas as pd
import matplotlib.pyplot as plt

input_filename = sys.argv[1]

# Read data from CSV file
months = pd.read_csv(input_filename)

# Filter data to include only September and November
filtered_months = months[(months['Month'] == 'September') | (months['Month'] == 'November')]

# Plot histograms for September and November
plt.figure(figsize=(10, 6))

# Dictionary to store the color corresponding to each month
month_colors = {'September': 'blue', 'November': 'green'}

for month_name in ['September', 'November']:  # Only September and November
    month_data = filtered_months[filtered_months['Month'] == month_name]['Percent change']
    color = month_colors[month_name]
    
    # Plot histogram
    plt.hist(month_data, bins=10, alpha=0.35, edgecolor='black', label=month_name, color=color)
    
    # Calculate and plot mean line for each month
    month_mean = month_data.mean()
    plt.axvline(x=month_mean, color=color, linestyle='--', label=f'{month_name} Mean: {month_mean:.2f}')

plt.legend()
plt.title('Histogram of Daily Percent Growths for September and November')
plt.xlabel('Daily Percent Growth')
plt.ylabel('Frequency')
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig("sept-nov.png")