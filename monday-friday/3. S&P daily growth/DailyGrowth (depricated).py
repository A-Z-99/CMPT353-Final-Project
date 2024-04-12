import pandas as pd
import sys
import matplotlib.pyplot as plt
import statsmodels as stats

OUTPUT_TEMPLATE = (
    "Original data normality p-values: {monday_normality_p:.3g} {friday_normality_p:.3g}\n"
    "Original data equal-variance p-value: {initial_levene_p:.3g}\n"
    "Initial T-test p-value: {initial_ttest_p:.3g}\n"
    "u-test p-value: {mannwhitneyu_p:.3g}\n"
)

input_file = sys.argv[1]

# Read CSV files into pandas DataFrame
data = pd.read_csv(input_file)

# Convert the date column to datetime type
data['Date'] = pd.to_datetime(data['Date'])

""""""""

mondays = data[data['Day of week'] == 0]
fridays = data[data['Day of week'] == 4]

# Calculate the number of negative changes
negative_changes_mondays = (mondays['Percent change'] < 0).sum()
negative_changes_fridays = (fridays['Percent change'] < 0).sum()

# Total number of changes
total_changes_mondays = len(mondays)
total_changes_fridays = len(fridays)

print(f"Monday negative changes: {negative_changes_mondays}/{total_changes_mondays}")
print(f"Friday negative changes: {negative_changes_fridays}/{total_changes_fridays}")

# # Perform the sign test
# p_value = binom.cdf(negative_changes, total_changes, 0.5)

# print("Number of Negative Changes:", negative_changes)
# print("Total Changes:", total_changes)
# print("Probability of Negative Change:", p_value)

print("Average monday percent change:", mondays['Percent change'].mean())
print("Average friday percent change:", fridays['Percent change'].mean())


# # Plot all Monday values in blue
# plt.plot(mondays['Date'], mondays['Percent change'], color='blue', label='Monday', marker='o', linestyle='None', markersize=2)

# # Plot all Friday values in red
# plt.plot(fridays['Date'], fridays['Percent change'], color='red', label='Friday', marker='o', linestyle='None', markersize=2)

# Plot all Monday values in blue
plt.plot(mondays['Date'], mondays['Percent change'], color='blue', label='Monday')

# Plot all Friday values in red
plt.plot(fridays['Date'], fridays['Percent change'], color='red', label='Friday')

plt.axhline(y=0, color='black', linestyle='--')

# Add labels and title
plt.xlabel('Date')
plt.ylabel('Value')
plt.title('Monday and Friday percent changes')

# Show legend
plt.legend()

# Show the plot
plt.show()

# Create histogram to show percent change distributions for Mondays and Fridays

# Create histogram for Monday percent changes
plt.hist(mondays['Percent change'], bins=30, color='blue', alpha=0.5, label='Monday')

# Create histogram for Friday percent changes
plt.hist(fridays['Percent change'], bins=30, color='red', alpha=0.5, label='Friday')

# Add labels and title
plt.xlabel('Percent Change')
plt.ylabel('Frequency')
plt.title('Percent Change Distribution for Mondays and Fridays')

# Add a legend
plt.legend()

# Show the plot
plt.show()


normaltest_mondays = stats.normaltest(mondays['Percent change'])
normaltest_fridays = stats.normaltest(fridays['Percent change'])
levene_test = stats.levene(mondays['Percent change'], fridays['Percent change'])
ttest_result = stats.ttest_ind(mondays['Percent change'], fridays['Percent change'], equal_var=True)
mannwhitneyu = stats.mannwhitneyu(mondays['Percent change'], fridays['Percent change'])

print(OUTPUT_TEMPLATE.format(
        initial_ttest_p=ttest_result.pvalue,
        monday_normality_p=normaltest_mondays.pvalue,
        friday_normality_p=normaltest_fridays.pvalue,
        initial_levene_p=levene_test.pvalue,
        mannwhitneyu_p=mannwhitneyu.pvalue
    ))
