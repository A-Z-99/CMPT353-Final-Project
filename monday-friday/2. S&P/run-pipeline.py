import subprocess

def run_ETL():
    try:
        subprocess.run(["python3", "snpETL.py"], check=True)
    except subprocess.CalledProcessError as e:
        print("Error running python3:", e)

def run_python_script1():
    try:
        subprocess.run(["python3", "MondayFridayProceding.py", "../../datasets/monday-friday/snpDataCondensed.csv"], check=True)
    except subprocess.CalledProcessError as e:
        print("Error running python3:", e)

def run_python_script2():
    try:
        subprocess.run(["python3", "MondayFridaySucceeding.py", "../../datasets/monday-friday/snpDataCondensed.csv"], check=True)
    except subprocess.CalledProcessError as e:
        print("Error running python3:", e)

def main():
    run_ETL()
    run_python_script1()
    run_python_script2()

if __name__ == "__main__":
    main()