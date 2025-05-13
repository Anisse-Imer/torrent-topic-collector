from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Create a SparkSession
spark = SparkSession.builder \
    .appName("KafkaSparkStreaming") \
    .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1') \
    .getOrCreate()

# Define the Kafka source
df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "kafka:9092") \
  .option("subscribe", "magnets") \
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
