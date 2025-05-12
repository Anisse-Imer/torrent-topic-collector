from kafka import KafkaConsumer

bootstrap_servers = 'localhost:9092'
topic = 'magnets'

consumer = KafkaConsumer(
    topic,
    bootstrap_servers=[bootstrap_servers],
    auto_offset_reset='earliest',
    value_deserializer=lambda x: x.decode('utf-8')
)

print(f"Consuming from topic: {topic}")
print("Press Ctrl+C to stop")

try:
    for message in consumer:
        print(f"Received: {message.value}")
except KeyboardInterrupt:
    print("\nConsumer stopped")
