from kafka import KafkaConsumer
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("BasicTest").getOrCreate()

# Simplest possible operation
rdd = spark.sparkContext.parallelize([1, 2, 3, 4])
print(rdd.collect())

spark.stop()
