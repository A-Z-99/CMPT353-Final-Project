import subprocess

def run_spark_submit():
    try:
        subprocess.run(["spark-submit", "stocksETL.py", "../../datasets/monday-friday/Data/Stocks", "stocksData"], check=True)
    except subprocess.CalledProcessError as e:
        print("Error running spark-submit:", e)

def run_python_script():
    try:
        subprocess.run(["python3", "MondayFriday.py"], check=True)
    except subprocess.CalledProcessError as e:
        print("Error running python3:", e)

def main():
    run_spark_submit()
    run_python_script()

if __name__ == "__main__":
    main()