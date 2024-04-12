import subprocess
import re

def run_ETL(name):
    try:
        subprocess.run(["python3", "pastS&P_ETL.py", "../../datasets/monday-friday/" + name, "../../datasets/monday-friday/processed_" + name], check=True)
    except subprocess.CalledProcessError as e:
        print("Error running python3:", e)

def run_python_script_Procede(name, suffix):
    try:
        subprocess.run(["python3", "../2. S&P/MondayFridayProceding.py", "../../datasets/monday-friday/processed_" + name, suffix], check=True)
    except subprocess.CalledProcessError as e:
        print("Error running python3:", e)

def run_python_script_Succeed(name, suffix):
    try:
        subprocess.run(["python3", "../2. S&P/MondayFridaySucceeding.py", "../../datasets/monday-friday/processed_" + name, suffix], check=True)
    except subprocess.CalledProcessError as e:
        print("Error running python3:", e)

def run_python_script_Percent_Procede(name, suffix):
    try:
        subprocess.run(["python3", "../3. S&P daily growth/MondayFridayDailyGrowthProceeding.py", "../../datasets/monday-friday/processed_" + name, suffix], check=True)
    except subprocess.CalledProcessError as e:
        print("Error running python3:", e)

def run_python_script_Percent_Succeed(name, suffix):
    try:
        subprocess.run(["python3", "../3. S&P daily growth/MondayFridayDailyGrowthSucceeding.py", "../../datasets/monday-friday/processed_" + name, suffix], check=True)
    except subprocess.CalledProcessError as e:
        print("Error running python3:", e)

def run_graph(name, suffix):
    try:
        subprocess.run(["python3", "../3. S&P daily growth/daily-growth-lineplot.py", name, suffix], check=True)
    except subprocess.CalledProcessError as e:
        print("Error running python3:", e)

def main():
    datasets = ['snp1979.csv', 'snp1980.csv', 'snp1981.csv','snp1990.csv', 'snp1997.csv']
    pattern = re.compile(r'\d+')
    for dataset in datasets:
        suffix = re.search(pattern, dataset).group()
        run_ETL(dataset)
        # run_python_script_Procede(dataset, suffix)
        # run_python_script_Succeed(dataset, suffix)
        run_python_script_Percent_Procede(dataset, suffix)
        # run_python_script_Percent_Succeed(dataset, suffix)
    run_graph('../../datasets/monday-friday/processed_snp1980.csv', '1980')
if __name__ == "__main__":
    main()