import pandas as pd
import sys
from scipy import stats
import matplotlib.pyplot as plt

def main():

    """
    Doing Statistical Tests on the data
    """
    
    input_filename = "../datasets/month-start/monthEvalSnpDataPercent.csv"
    output_filename = "Results.txt"
    
    # Load the dataset
    data = pd.read_csv(input_filename, parse_dates=['Date'])

    # running to test if the data is normally distributed
    normal_test_first_day_data = stats.normaltest(data['First Day Percent change'])
    normal_test_other_days_data = stats.normaltest(data['Month Avg Percent change'])
    
    # print(normal_test_first_day_data.pvalue)
    # print(normal_test_other_days_data.pvalue)
    
    # running to test if the data has equal variance
    equal_variance_test = stats.levene(data['First Day Percent change'], data['Month Avg Percent change'])
    # print(equal_variance_test.pvalue)
    
    # CONCLUSION: the data isn't normally distributed neither does it have equal variance
    
    # we can run Mann-Whitney U-test to check if the samples from one group are larger/smaller than another
    mann_whitney_test = stats.mannwhitneyu(data['First Day Percent change'], data['Month Avg Percent change'])
    # print(mann_whitney_test.pvalue)

    # CONCLUSION: pvalue > 0.05, we FAIL to reject our null hypothesis (H0 = the two means are same)

    # we can also run wilcoxon test to check if we can conclude something from pairs' difference 
    wilcoxon_test = stats.wilcoxon(data['Difference'], zero_method='wilcox')
    # print(wilcoxon_test.pvalue)

    # CONCLUSION: pvalue > 0.05, we FAIL to reject our null hypothesis (H0 = the two means are same)

    total_months = data['Date'].size

    # write the results to a file
    with open(output_filename, 'w') as file:
        file.write(f"Mann-Whitney U-Test p-value:      {mann_whitney_test.pvalue}\n")
        file.write(f"Wilcoxon Test p-value:            {wilcoxon_test.pvalue}\n")
        file.write(f"Number of months of data:         {total_months}\n")
        file.write(f"Average First Day change percent: {data['First Day Percent change'].mean()}\n")
        file.write(f"Average Other Days change percent:{data['Month Avg Percent change'].mean()}\n")

if __name__=='__main__':
    main()