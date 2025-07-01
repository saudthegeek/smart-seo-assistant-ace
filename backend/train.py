import os
import subprocess

def run_training(run_name: str):
    try:
        os.environ["RUN_NAME"] = run_name
        subprocess.run(["dvc", "repro"], check=True)
        return f"Training run '{run_name}' started via DVC."
    except Exception as e:
        return f"Error starting training: {str(e)}"
