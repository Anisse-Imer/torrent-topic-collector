import os
import time
import logging
import sys

worker_id = os.getenv("WORKER_ID", "default")

# Configure logging to stdout with proper formatting
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - Worker %(worker_id)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

# Use LoggerAdapter to add worker_id to log records
logger = logging.getLogger(__name__)
logger = logging.LoggerAdapter(logger, {"worker_id": worker_id})

# Worker loop
while True:
    logger.info("Doing work...")
    time.sleep(2)
