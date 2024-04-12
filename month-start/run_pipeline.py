import subprocess

# List of scripts to be executed in order
scripts = [
    '01_extract_month_data.py',
    '02_visualize_dataset.py',
    '03_statistical_conclusion.py',
]

def run_script(script_name):
    print(f"Running {script_name}...")
    subprocess.run(['python', script_name], check=True)

def main():
    for script in scripts:
        run_script(script)

if __name__ == "__main__":
    main()