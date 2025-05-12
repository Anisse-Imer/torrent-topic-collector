from kafka import KafkaProducer
import time

bootstrap_servers = 'localhost:9092'
topic = 'magnets'

producer = KafkaProducer(
    bootstrap_servers=[bootstrap_servers],
    value_serializer=lambda x: x.encode('utf-8')
)

print(f"Producing to topic: {topic}")
print("Press Ctrl+C to stop")

try:
    count = 0
    while True:
        message = f"Message {count}"
        producer.send(topic, value=message)
        print(f"Sent: {message}")
        count += 1
        time.sleep(1)
except KeyboardInterrupt:
    print("\nProducer stopped")
