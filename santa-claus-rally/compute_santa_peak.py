import pandas as pd

def get_rally_period_dates(year):
    """Return the start and end dates of the rally period for a given year."""
    rally_start_date = pd.Timestamp(year=year, month=12, day=18)
    rally_end_date = pd.Timestamp(year=year, month=12, day=31)
    return rally_start_date, rally_end_date

def identify_rally_peaks(df):
    """Identify peak values within each rally period for the available years in the dataset."""
    unique_years = df['Date'].dt.year.unique()
    rally_data_frames = []  # List to store DataFrame slices to concatenate later

    for year in unique_years:
        rally_start, rally_end = get_rally_period_dates(year)
        rally_period_df = df[(df['Date'] >= rally_start) & (df['Date'] <= rally_end)]
        
        if not rally_period_df.empty:
            peak_value = rally_period_df['value'].max()
            peak_date = rally_period_df[rally_period_df['value'] == peak_value]['Date'].iloc[0]

            # Create a temporary DataFrame slice
            temp_rally_data = pd.DataFrame({
                'start date': [rally_period_df['Date'].iloc[-1]],
                'start value': [rally_period_df['value'].iloc[-1]],
                'peak date': [peak_date],
                'peak value': [peak_value],
                'end date': [rally_period_df['Date'].iloc[0]],
                'end value': [rally_period_df['value'].iloc[0]]
            })

            # Add the temporary DataFrame to the list
            rally_data_frames.append(temp_rally_data)
    
    # Concatenate all DataFrame slices into one DataFrame
    rally_data = pd.concat(rally_data_frames, ignore_index=True)
    
    # Calculate 'start to peak' and 'peak to end' percent changes
    rally_data['start to peak percent change'] = (((rally_data['peak value'] - rally_data['start value']) / rally_data['start value']) * 100).round(2)
    rally_data['peak to end percent change'] = (((rally_data['end value'] - rally_data['peak value']) / rally_data['peak value']) * 100).round(2)
    
    return rally_data

def main():
    data_path = '../datasets/santa-claus/SCR_snp_data_condensed.csv'

    # Read the condensed Santa Claus Rally data
    santa_claus_data_condensed = pd.read_csv(data_path, parse_dates=['Date'])

    # Identify the rally peaks and calculate percent changes
    rally_data = identify_rally_peaks(santa_claus_data_condensed)

    # Save the rally data with peak values and percent changes to a new CSV file
    rally_data.to_csv('../datasets/santa-claus/SCR_snp_data_percent.csv', index=False)

if __name__ == '__main__':
    main()
