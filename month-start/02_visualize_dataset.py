import pandas as pd
import sys
import matplotlib.pyplot as plt

def main():

    """
    Visualizing the data
    """

    input_filename = "../datasets/month-start/monthEvalSnpDataPercent.csv"
    
    # Load the dataset
    data = pd.read_csv(input_filename, parse_dates=['Date'])

    # Plot the two dataset from the df
    # 1. the first day of the trading month
    # 2. the other days the month

    # plot them on different graphs
    plt.plot(data['Date'], data['First Day Percent change'], color='blue', label='First Day Percent change', marker='o', markersize=2)
    plt.xlabel('Date')
    plt.ylabel('Percent Change')
    plt.title('First Day Percent Changes')
    plt.grid(True)
    plt.legend()

    plt.savefig('First Day Percent Changes.png', format='png', dpi=300)
    plt.clf()
    # plt.show();return

    plt.plot(data['Date'], data['Month Avg Percent change'], color='red', label='Month Avg Percent change', marker='o', markersize=2)
    plt.xlabel('Date')
    plt.ylabel('Percent Change')
    plt.title('Monthly Avg. Percent Changes')
    plt.grid(True)
    plt.legend()

    plt.savefig('Monthly Avg. Percent Changes.png', format='png', dpi=300)
    plt.clf()
    # plt.show();return

    # plot them on the same graph
    plt.figure(figsize=(6,4))  # Optional: Specifies the size of the plot
    # plt.grid(True)
    plt.scatter(x=data['Date'], y=data['First Day Percent change'], color='blue', label='First Day Percent change')
    plt.scatter(x=data['Date'], y=data['Month Avg Percent change'], color='red', label='Month Avg Percent change')

    # plt.plot(data['Date'], data['First Day Percent change'], color='blue', label='First Day Percent change', marker='o')
    # plt.plot(data['Date'], data['Month Avg Percent change'], color='red', label='Month Avg Percent change', marker='o')
    
    plt.xlabel('Date')
    plt.ylabel('Percent Change')
    plt.title('Comparison of First Day and Monthly Average Percent Changes')
    plt.legend()

    plt.savefig('First Day vs Monthly Avg Percent Changes.png', format='png', dpi=300)
    plt.clf()
    # plt.show();return

    # Plot the differences (first day - monthly avg) to have a look at the distribution
    plt.hist(data['Difference'], bins=10, color='skyblue')
    # plt.grid(True)
    plt.xlabel('Difference in Percent Change')
    plt.ylabel('Frequency')
    plt.title('Histogram of Differences (First Day - Month Avg)')
    # plt.axvline(x=data['Difference'].mean(), color='blue', linestyle='--')
    plt.axvline(x=0, color='red', linestyle='--')
    
    
    plt.savefig('Histogram of Differences.png', format='png', dpi=300)
    plt.clf()
    # plt.show()

if __name__=='__main__':
    main()