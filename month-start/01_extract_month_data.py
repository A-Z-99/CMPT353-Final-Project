import pandas as pd
import sys
import matplotlib.pyplot as plt

def main():

    input_filename = "../datasets/month-start/snpDataPercent.csv"
    output_filename = "../datasets/month-start/monthEvalSnpDataPercent.csv"
    
    # Get data from csv to pandas dataframe(df)
    data = pd.read_csv(input_filename, parse_dates=['Date']).drop(columns=['Day of week','Value'])
    
    # Remove the month of April 2014, because we don't have the percent change for 1st April, 2014
    data = data[~((data['Date'].dt.month == 4) & (data['Date'].dt.year == 2014))]
    
    # Get the first day of the trading month of all the data we have in a pandas series
    first_days_list = data.groupby([data['Date'].dt.year, data['Date'].dt.month])['Date'].min().reset_index(drop=True)
    
    # Keep only first days data from the original dataset
    first_days = data[data['Date'].isin(first_days_list)]
    first_days.loc[:, 'Date'] = first_days['Date'].dt.to_period('M')
    first_days = first_days.rename(columns={'Percent change': 'First Day Percent change'})
    
    # Keep all the data except the first days of the trading month
    other_days = data[~data['Date'].isin(first_days_list)]
    
    # Get the average of the trading month of all the data we have
    other_days_avg = other_days.groupby(other_days['Date'].dt.to_period("M"))['Percent change'].mean().reset_index()    
    other_days_avg = other_days_avg.rename(columns={'Percent change': 'Month Avg Percent change'})

    # merge the two datasets so we have both the data in the same df based on the month
    month_data = pd.merge(first_days, other_days_avg, on='Date')
    month_data['Difference'] = month_data['First Day Percent change'] - month_data['Month Avg Percent change']
    
    month_data.to_csv(output_filename, index=False)
    
    # print(data, first_days_list, first_days, other_days, other_days_avg, month_data);return #.dtypes)


if __name__=='__main__':
    main()