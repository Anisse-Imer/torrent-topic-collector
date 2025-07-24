import subprocess
import os
import logging
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Read worker IDs from .env
worker_ids = os.getenv("WORKER_IDS", "").split(",")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

containers = []
for idx, wid in enumerate(worker_ids):
    container_name = f"worker_{idx}"
    port = 5000 + idx
    
    logger.info(f"Starting worker {wid}...")
    
    container = subprocess.Popen([
        "docker", "run", "--rm", "-d",
        "--name", container_name,
        "--network", "data_lakehouse_net",  
        "-e", f"WORKER_ID={wid}", 
        "-p", f"{port}:8080",
        "worker-magnet"
    ])

    containers.append(container)

    logger.info(f"Worker {wid} started with container name {container_name} and mapped to port {port}.")
