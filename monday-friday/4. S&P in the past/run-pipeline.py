import subprocess

def run_ETL(name):
    try:
        subprocess.run(["python3", "pastS&P_ETL.py", "../../datasets/monday-friday/" + name, "../../datasets/monday-friday/processed_" + name], check=True)
    except subprocess.CalledProcessError as e:
        print("Error running python3:", e)

def run_python_script_Procede(name):
    try:
        subprocess.run(["python3", "../2. S&P/MondayFridayProceding.py", "../../datasets/monday-friday/processed_" + name], check=True)
    except subprocess.CalledProcessError as e:
        print("Error running python3:", e)

def run_python_script_Succeed(name):
    try:
        subprocess.run(["python3", "../2. S&P/MondayFridaySucceeding.py", "../../datasets/monday-friday/processed_" + name], check=True)
    except subprocess.CalledProcessError as e:
        print("Error running python3:", e)

def run_python_script_Percent(name):
    try:
        subprocess.run(["python3", "../3. S&P daily growth/MondayFridayPercent.py", "../../datasets/monday-friday/processed_" + name], check=True)
    except subprocess.CalledProcessError as e:
        print("Error running python3:", e)

def main():
    datasets = ['snp1990.csv', 'snp1997.csv']
    for dataset in datasets:
        run_ETL(dataset)
        run_python_script_Procede(dataset)
        run_python_script_Succeed(dataset)
        run_python_script_Percent(dataset)

if __name__ == "__main__":
    main()