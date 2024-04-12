import sys
import pandas as pd

input_filename = "../../datasets/monday-friday/snpData.csv"
output_filename = "../../datasets/monday-friday/snpDataPercent.csv"

# expect around 10 * 365 * 5/7 rows corresponding to trading days in 10 years
data = pd.read_csv(input_filename)

# store average of high and low as value
data['Value'] = (data['High'] + data['Low'])/2
data['Value'] = data['Value'].round(2)

# # Replace 0 values in 'Value' column with corresponding values from 'Close/Last' column
# zero_mask = data['Value'] == 0
# data.loc[zero_mask, 'Value'] = data.loc[zero_mask, 'Close/Last']

# Filter out non-trading days (holidays)
data = data[data['Value'] != 0]

# Get Day of week (0=Monday, 4=Friday, 6=Sunday)
data['Date'] = pd.to_datetime(data['Date'])
data['Day of week'] = data['Date'].dt.day_of_week

# Sort values by ascending date
data.sort_values(by='Date', inplace=True)

# Calculate percent change from previous trading day
data['Previous'] = data['Value'].shift(periods=1)
data['Percent change'] = (data['Value']-data['Previous'])/data['Previous']
data['Percent change'] = (data['Percent change']*100).round(2)

# remove unneeded columns
data = data.drop(columns=['Close/Last', 'Open', 'High', 'Low', 'Previous']).set_index(['Date'])

data.to_csv(output_filename)
