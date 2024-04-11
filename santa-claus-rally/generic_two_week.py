import pandas as pd
import numpy as np

def identify_generic_two_week_peaks(df):
    """Identify peak values within each generic two-week period for the available years in the dataset."""
    rally_data_frames = []
    unique_years = df['Date'].dt.year.unique()

    for year in unique_years:
        # For each year, randomly select a two-week period
        year_data = df[df['Date'].dt.year == year]
        
        if len(year_data) >= 14:
            for month in range(1, 12):  # Exclude December to avoid Santa Claus Rally overlap
                month_data = year_data[year_data['Date'].dt.month == month]
                if len(month_data) >= 14:
                    random_start_index = np.random.randint(0, len(month_data) - 14)
                    two_week_period_df = month_data.iloc[random_start_index:random_start_index + 10] # Exclude weekends where trading does not occur 
                    
                    peak_value = two_week_period_df['Value'].max()
                    peak_date = two_week_period_df[two_week_period_df['Value'] == peak_value]['Date'].iloc[0]

                    temp_rally_data = pd.DataFrame({
                        'start date': [two_week_period_df['Date'].iloc[-1]],
                        'start value': [two_week_period_df['Value'].iloc[-1]],
                        'peak date': [peak_date],
                        'peak value': [peak_value],
                        'end date': [two_week_period_df['Date'].iloc[0]],
                        'end value': [two_week_period_df['Value'].iloc[0]]
                    })

                    rally_data_frames.append(temp_rally_data)

    # Concatenate all DataFrame slices into one DataFrame
    rally_data = pd.concat(rally_data_frames, ignore_index=True)
    return rally_data

def main():
    # Define the path to the CSV file with condensed S&P data
    data_path = '../datasets/monday-friday/snpDataCondensed.csv'

    # Read the condensed S&P data
    snp_data_condensed = pd.read_csv(data_path, parse_dates=['Date'])

    # Identify the peak values within each generic two-week period
    generic_rally_data = identify_generic_two_week_peaks(snp_data_condensed)

    # Calculate 'start to peak' and 'peak to end' percent changes
    generic_rally_data['start to peak percent change'] = (((generic_rally_data['peak value'] - generic_rally_data['start value']) / generic_rally_data['start value']) * 100).round(2)
    generic_rally_data['peak to end percent change'] = (((generic_rally_data['end value'] - generic_rally_data['peak value']) / generic_rally_data['peak value']) * 100).round(2)

    # Save the rally data with peak values and percent changes to a new CSV file
    generic_rally_data.to_csv('../datasets/santa-claus/generic2week_snp_data_percent.csv', index=False)

if __name__ == '__main__':
    main()
