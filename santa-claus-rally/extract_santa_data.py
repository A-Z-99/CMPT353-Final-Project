import pandas as pd
from datetime import timedelta


snp_data_path = '../datasets/monday-friday/snpData.csv'

snp_data_df = pd.read_csv(snp_data_path)

# Convert the 'Date' column to datetime for easier date manipulation
snp_data_df['Date'] = pd.to_datetime(snp_data_df['Date'])

# Define a function to extract data for the Santa Claus Rally period
def extract_santa_claus_rally(data, year):
    # Define the date range for the Santa Claus Rally: 1 week before to 1 week after Christmas
    start_date = pd.Timestamp(year=year, month=12, day=18)
    end_date = pd.Timestamp(year=year, month=12, day=31) + timedelta(days=7)
    if end_date.year != year:
        end_date = pd.Timestamp(year=year, month=12, day=31)
    
    # Filter the data for the defined date range
    rally_data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
    return rally_data

# Initialize a DataFrame to hold all Santa Claus Rally data
santa_claus_rally_all_years = pd.DataFrame()

for year in snp_data_df['Date'].dt.year.unique():
    santa_claus_rally_data = extract_santa_claus_rally(snp_data_df, year)
    santa_claus_rally_all_years = pd.concat([santa_claus_rally_all_years, santa_claus_rally_data])


output_path = '../datasets/santa-claus/SCR_snp_data.csv'  
santa_claus_rally_all_years.to_csv(output_path, index=False)
