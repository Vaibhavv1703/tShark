import subprocess
import sys

def run_script(script_name):
    print(f"\n--- Running {script_name} ---")
    result = subprocess.run([sys.executable, script_name], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f"Error running {script_name}:")
        print(result.stderr)
        sys.exit(1)

def main():
    print("Welcome to the automated web domain analysis pipeline!\n")

    run_script("capture.py")

    run_script("scrape.py")

    run_script("categorize.py")

    run_script("clean.py")

    print("\nFinal cleaned and merged data:\n")
    
    run_script("tab.py")

if __name__ == "__main__":
    main()
