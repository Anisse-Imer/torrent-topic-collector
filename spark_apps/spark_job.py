from dotenv import load_dotenv

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Load .env variables
load_dotenv()
# Kafka connection details
bootstrap_servers:str = os.getenv("BOOTSTRAP_SERVER", "default")
topic:str = os.getenv("KAFKA_TOPIC", "default")

# Create a SparkSession
spark = SparkSession.builder \
    .appName("KafkaSparkStreaming") \
    .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1') \
    .getOrCreate()

# Define the Kafka source
df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", bootstrap_servers) \
  .option("subscribe", topic) \
  .load()

# Select the value from the Kafka message and cast it to a string
value_df = df.select(col("value").cast("string").alias("message"))

# Write the stream to the console
query = value_df \
    .writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()
