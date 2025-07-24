import os
import time
import logging
import sys
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

from dotenv import load_dotenv

from includes.singleton_torrent import singletonTorrent

# Load .env variables
load_dotenv()
worker_id = os.getenv("WORKER_ID", "default")
# Kafka connection details
bootstrap_servers:str = os.getenv("BOOTSTRAP_SERVER", "default")
topic:str = os.getenv("KAFKA_TOPIC", "default")

# Configure logging to stdout with proper formatting
logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.StreamHandler(sys.stdout)]
)

# Use LoggerAdapter to add worker_id to log records
logger = logging.getLogger(__name__)
logger = logging.LoggerAdapter(logger, {"worker_id": worker_id})

# Retry logic for Kafka connection
retries = 5
delay = 1  # Start with 1 second

while retries > 0:
    try:
        # Try to create the Kafka producer
        producer = KafkaProducer(
            bootstrap_servers=[bootstrap_servers],
            value_serializer=lambda x: x.encode('utf-8')
        )
        logger.info("Connected to Kafka successfully")
        break  # Exit the loop if connection is successful
    except NoBrokersAvailable:
        logger.error(f"No brokers available, retrying in {delay} seconds...")
        time.sleep(delay)
        retries -= 1
        delay *= 2  # Exponential backoff: double the delay each time

if retries == 0:
    logger.error("Failed to connect to Kafka after several attempts")
    exit(1)

# Worker loop - sending messages to Kafka
magnets_sent:list[str] = []
_instance:singletonTorrent = singletonTorrent()

while True:
    try:
        for magnet in _instance.search(query=worker_id, retries=100):
            if magnet in magnets_sent:
                pass
            else:
                producer.send(topic, value=magnet)
                logger.info(f"Sent: {magnet}")
                magnets_sent.append(magnet)
    except Exception as e:
        logger.error(e)
