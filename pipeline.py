import os
import yaml
import subprocess
from pathlib import Path
import sys

def load_config(config_path="config.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def run_step(script_path, description):
    print(f"\n--- Running Step: {description} ---")
    result = subprocess.run([sys.executable, script_path], check=True)
    if result.returncode != 0:
        print(f"Error in {description}, stopping pipeline")
        sys.exit(1)

def main():
    config = load_config()
    
    # Step 1: Ingestion
    run_step("src/ingestion.py", "Data Ingestion")
    
    # Step 2: Feature Engineering
    run_step("src/features.py", "Feature Engineering")
    
    # Step 3: Training
    run_step("src/train.py", "Model Training")
    
    # Step 4: Evaluation
    run_step("src/evaluate.py", "Model Evaluation")
    
    print("\n--- Pipeline Completed Successfully ---")

if __name__ == "__main__":
    main()
