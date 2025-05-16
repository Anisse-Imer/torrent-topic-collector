import os

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

bootstrap_servers: str = os.getenv("BOOTSTRAP_SERVER", "default")
topic: str = os.getenv("KAFKA_TOPIC", "default")

# Create SparkSession
spark = SparkSession.builder \
    .appName("KafkaSparkStreaming") \
    .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1') \
    .getOrCreate()

# Define Kafka source
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", bootstrap_servers) \
    .option("subscribe", topic) \
    .load()

# Process each batch and print the topic
def process_batch(batch_df, batch_id):
    print(f"Processing batch {batch_id} from topic: {topic}")  # Continuously prints
    batch_df.select(col("value").cast("string").alias("message")).show(truncate=False)

# Write stream with foreachBatch
query = df \
    .writeStream \
    .foreachBatch(process_batch) \
    .outputMode("update") \
    .start()

query.awaitTermination()