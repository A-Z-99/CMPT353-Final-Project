import subprocess

# List of scripts to be executed in order
scripts = [
    'extract_santa_data.py',
    'condensed_santa.py',
    'compute_santa_peak.py',
    'generic_two_week.py',
    'statistical_comparison.py',
    'visualize.py'
]

def run_script(script_name):
    print(f"Running {script_name}...")
    subprocess.run(['python', script_name], check=True)

def main():
    for script in scripts:
        run_script(script)

if __name__ == "__main__":
    main()
