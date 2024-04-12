import subprocess

def run_spark_submit():
    try:
        subprocess.run(["spark-submit", "stocksETL.py", "Data/Stocks"], check=False)
    except subprocess.CalledProcessError as e:
        print("Error running spark-submit:", e)

def run_python_script():
    try:
        subprocess.run(["python3", "months.py", "../datasets/months/snpDataPercent.csv", "output.txt"], check=True)
    except subprocess.CalledProcessError as e:
        print("Error running python3:", e)

def run_graphs():
    try:
        subprocess.run(["python3", "graph.py", "../datasets/months/monthsData.csv"], check=True)
    except subprocess.CalledProcessError as e:
        print("Error running python3:", e)

def main():
    run_python_script()
    run_graphs()

if __name__ == "__main__":
    main()