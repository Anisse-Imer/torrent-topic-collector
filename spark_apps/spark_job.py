import os
import logging
import concurrent.futures
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from includes.singleton_torrent import singletonTorrent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('/opt/spark/logs/app.log')
    ]
)
logger = logging.getLogger(__name__)

bootstrap_servers: str = os.getenv("BOOTSTRAP_SERVER", "default")
topic: str = os.getenv("KAFKA_TOPIC", "default")

logger.info(f"Starting Kafka Spark Streaming application")
logger.info(f"Bootstrap servers: {bootstrap_servers}")
logger.info(f"Kafka topic: {topic}")

# Create SparkSession
spark = SparkSession.builder \
    .appName("KafkaSparkStreaming") \
    .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1') \
    .getOrCreate()

logger.info("SparkSession created successfully")

# Define Kafka source
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", bootstrap_servers) \
    .option("subscribe", topic) \
    .option("startingOffsets", "earliest") \
    .load()

logger.info("Kafka stream configured")

def process_batch(magnet: str):
    try:
        logger.info(f"Processing magnet: {magnet[:50]}...")
        _instance = singletonTorrent()
        save_path = f"/opt/spark/logs/{magnet}"
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(_instance.download, save_path=save_path, magnet_url=magnet)
            logger.info(f"Torrent download initiated for: {magnet[:50]}...")
            
    except Exception as e:
        logger.error(f"Error processing magnet {magnet[:50]}...: {str(e)}")

def process_kafka_batch(batch_df, batch_id):
    try:
        messages = batch_df.select(col("value").cast("string").alias("message")).collect()
        message_count = len(messages)
        
        for i, row in enumerate(messages):
            magnet = row["message"]
            logger.info(f"Processing message {i+1}/{message_count} in batch {batch_id}")
            process_batch(magnet)
            
        logger.info(f"Completed processing batch {batch_id}")
        
    except Exception as e:
        logger.error(f"Error processing batch {batch_id}: {str(e)}")

logger.info("Starting stream processing...")

query = df \
    .writeStream \
    .foreachBatch(process_kafka_batch) \
    .outputMode("update") \
    .option("checkpointLocation", "/opt/spark/checkpoints") \
    .start()

logger.info("Stream started, waiting for termination...")
query.awaitTermination()
