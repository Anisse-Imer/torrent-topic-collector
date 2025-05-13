import subprocess
import os
from dotenv import load_dotenv

# Load .env file to read the worker IDs
load_dotenv()

# Read worker IDs from .env
worker_ids = os.getenv("WORKER_IDS", "").split(",")

# Function to stop the workers by name
def stop_containers():
    print("Stopping workers...")
    for wid in worker_ids:
        container_name = f"worker_{wid}"
        print(f"Stopping container {container_name}...")
        subprocess.run(["docker", "stop", container_name])

if __name__ == "__main__":
    stop_containers()
