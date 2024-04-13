import pandas as pd
from scipy.stats import mannwhitneyu

def load_data(rally_path, generic_path):
    """Load the rally and generic period data from the specified paths."""
    rally_data = pd.read_csv(rally_path)
    generic_data = pd.read_csv(generic_path)
    return rally_data, generic_data

def perform_statistical_tests(rally_data, generic_data):
    """Perform Mann-Whitney U-tests to compare the rally and generic period data."""
    # 'start to peak percent change' comparison
    u_stat_start_peak, p_value_start_peak = mannwhitneyu(
        rally_data['start to peak percent change'], 
        generic_data['start to peak percent change'],
        alternative='two-sided'
    )

    # 'peak to end percent change' comparison
    u_stat_peak_end, p_value_peak_end = mannwhitneyu(
        rally_data['peak to end percent change'], 
        generic_data['peak to end percent change'],
        alternative='two-sided'
    )

    return (u_stat_start_peak, p_value_start_peak, u_stat_peak_end, p_value_peak_end)

def main():
    rally_data_path = '../datasets/santa-claus/SCR_snp_data_percent.csv'
    generic_data_path = '../datasets/santa-claus/generic2week_snp_data_percent.csv'

    rally_data, generic_data = load_data(rally_data_path, generic_data_path)

    # Perform the statistical tests (u-tests)
    results = perform_statistical_tests(rally_data, generic_data)
    with open("summary.txt", 'w') as f:
        import sys
        sys.stdout = f
        print("Mann-Whitney U-tests comparing the Santa Claus Rally data to the generic two-week periods:")
        print(f"Start to peak percent change: U-statistic = {results[0]}, P-value = {results[1]}")
        print(f"Peak to end percent change: U-statistic = {results[2]}, P-value = {results[3]}")

if __name__ == '__main__':
    main()
