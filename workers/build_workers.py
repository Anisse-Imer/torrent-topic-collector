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
    container_name = f"worker_{wid}"  # Naming the container with worker_id
    port = 5000 + idx  # Example: dynamically assigning a port starting from 5000
    
    logger.info(f"Starting worker {wid}...")
    
    container = subprocess.Popen([
        "docker", "run", "--rm", "-e", f"WORKER_ID={wid}", 
        "--name", container_name,  # Name the container
        "-p", f"{port}:8080",       # Map port 8080 inside the container to a dynamic port on the host
        "worker-magnet"
    ])
    containers.append(container)

    logger.info(f"Worker {wid} started with container name {container_name} and mapped to port {port}.")
