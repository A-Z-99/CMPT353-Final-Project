import pandas as pd
import sys
import matplotlib.pyplot as plt

input_file = sys.argv[1]
if len(sys.argv) == 3:
    suffix = sys.argv[2]
else:
    suffix = ""

# Read CSV files into pandas DataFrame
data = pd.read_csv(input_file)

data.dropna(subset=['Percent change'], inplace=True)

# Convert the date column to datetime type
data['Date'] = pd.to_datetime(data['Date'])

mondays = data[data['Day of week'] == 0]
fridays = data[data['Day of week'] == 4]

plt.clf()
plt.grid(True)
# Plot all Monday values in blue
plt.plot(mondays['Date'], mondays['Percent change'], color='blue', label='Monday')

# Plot all Friday values in red
plt.plot(fridays['Date'], fridays['Percent change'], color='red', label='Friday')

# Add labels and title
plt.xlabel('Date')
plt.ylabel('Daily Percent Growth')
plt.title('Monday and Friday Daily Growth Percents')
plt.axhline(y=0, color='black', linestyle='--')

# Show legend
plt.legend()

plt.savefig("LinePercents" + suffix + ".png")