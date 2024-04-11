import pandas as pd

def condense_price_columns(df):
    # df['value'] = df[['Open', 'High', 'Close/Last', 'Low']].max(axis=1)
    df['value'] = ((df['High'] + df['Low']) / 2).round(2)
    
    # Convert the 'Date' column to datetime for easier analysis
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Drop the unnecessary price columns
    df_condensed = df.drop(['Open', 'High', 'Close/Last', 'Low'], axis=1)
    
    return df_condensed

def main():
    # Read the santa claus rally data
    santa_claus_data_path = '../datasets/santa-claus/SCR_snp_data.csv'
    santa_claus_data_df = pd.read_csv(santa_claus_data_path)

    # Apply the condensing function to the DataFrame
    santa_claus_data_condensed = condense_price_columns(santa_claus_data_df)

    # Save the condensed data to a new CSV file
    santa_claus_data_condensed.to_csv('../datasets/santa-claus/SCR_snp_data_condensed.csv', index=False)

if __name__ == '__main__':
    main()
