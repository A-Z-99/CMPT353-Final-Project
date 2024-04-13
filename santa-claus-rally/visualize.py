import pandas as pd
import matplotlib.pyplot as plt

def load_data():
    rally_data_path = '../datasets/santa-claus/SCR_snp_data_percent.csv'
    generic_data_path = '../datasets/santa-claus/generic2week_snp_data_percent.csv'
    rally_data = pd.read_csv(rally_data_path)
    generic_data = pd.read_csv(generic_data_path)
    return rally_data, generic_data

def plot_price_movements(rally_data):
    plt.figure(figsize=(12, 6))
    for year in rally_data['start date'].apply(lambda x: pd.to_datetime(x).year).unique():
        year_data = rally_data[rally_data['start date'].apply(lambda x: pd.to_datetime(x).year) == year]
        plt.plot(pd.to_datetime(year_data[['start date', 'peak date', 'end date']].values.flatten()),
                 year_data[['start value', 'peak value', 'end value']].values.flatten(), marker='o', label=f'Year {year}')
    plt.title('Santa Claus Rally Price Movements')
    plt.xlabel('Date')
    plt.ylabel('S&P 500 Index Value')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('../datasets/santa-claus/SC_price_movements.png')

def plot_histograms(rally_data, generic_data, column_name, title, color1, color2):
    plt.figure(figsize=(12, 6))
    n, bins, patches = plt.hist(rally_data[column_name], bins=20, alpha=0.5, label=f'Santa Claus Rally {title}', color=color1, density=True, edgecolor='black')
    n, bins, patches = plt.hist(generic_data[column_name], bins=bins, alpha=0.5, label=f'Generic 2-Week {title}', color=color2, density=True, edgecolor='black')
    plt.title(f'Comparison of {title}: Santa Claus Rally vs. Generic 2-Week Periods')
    plt.xlabel(f'{title} (%)')
    plt.ylabel('Density')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'../datasets/santa-claus/SC_{title.replace(" ", "_").lower()}.png')

def main():
    rally_data, generic_data = load_data()
    plot_price_movements(rally_data)
    plot_histograms(rally_data, generic_data, 'start to peak percent change', 'Start to Peak Percent Changes', 'green', 'blue')
    plot_histograms(rally_data, generic_data, 'peak to end percent change', 'Peak to End Percent Changes', 'green', 'blue')

if __name__ == '__main__':
    main()
