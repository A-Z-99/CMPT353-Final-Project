import sys
import pandas as pd

input_filename = "snpData.csv"
output_filename = "snpDataCondensed.csv"

data = pd.read_csv(input_filename)

# store average of high and low as value
data['value'] = (data['High'] + data['Low'])/2

# Get day of week (0=Monday, 5=Friday)
data['Date'] = pd.to_datetime(data['Date'])
data['day of week'] = data['Date'].dt.day_of_week

# remove unneeded columns
data = data.drop(columns=['Close/Last', 'Open', 'High', 'Low'])

print(data)
