import sys
import pandas as pd

input_filename = "snpData.csv"
output_filename = "snpDataCondensed.csv"

# expect around 10 * 365 * 5/7 rows corresponding to trading days in 10 years
data = pd.read_csv(input_filename)

# store average of high and low as value
data['Value'] = (data['High'] + data['Low'])/2
data['Value'] = data['Value'].round(2)

# Get day of week (0=Monday, 4=Friday, 6=Sunday)
data['Date'] = pd.to_datetime(data['Date'])
data['day of week'] = data['Date'].dt.day_of_week

# remove unneeded columns
data = data.drop(columns=['Close/Last', 'Open', 'High', 'Low']).set_index(['Date'])

data.to_csv(output_filename)
