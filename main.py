import subprocess
import sys

def run_script(script):
    print(f"Executing {script}...")
    result = subprocess.run([sys.executable, f"scripts/{script}"], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error executing {script}: {result.stderr}")
        return False
    print(f"Successfully executed {script}")
    return True

def main():
    scripts = [
        "prepare_data.py",
        "forecast_data.py",
        "generate_visualizations.py",
        "generate_site.py",
        "update_metadata.py",
        "lint_data.py"
    ]

    for script in scripts:
        if not run_script(script):
            sys.exit(1)

    print("\nFull pipeline v3 executed successfully!")

if __name__ == "__main__":
    main()
