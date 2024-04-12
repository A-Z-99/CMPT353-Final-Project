import subprocess

def run_ETL():
    try:
        subprocess.run(["python3", "snpETLpercentChange.py"], check=True)
    except subprocess.CalledProcessError as e:
        print("Error running python3:", e)

def run_python_script():
    try:
        subprocess.run(["python3", "MondayFridayPercent.py", "../../datasets/monday-friday/snpDataPercent.csv"], check=True)
    except subprocess.CalledProcessError as e:
        print("Error running python3:", e)

def main():
    run_ETL()
    run_python_script()

if __name__ == "__main__":
    main()