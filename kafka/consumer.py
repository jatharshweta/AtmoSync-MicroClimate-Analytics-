
import json
from kafka import KafkaConsumer

# Connect to Kafka and subscribe to the topic
consumer = KafkaConsumer(
    "sensor_readings",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

print("AtmoSync Kafka Consumer Started!")
print("Waiting for sensor readings...\n")

try:
    for message in consumer:
        reading = message.value

        print("Received Sensor Reading:")
        print(f"Container ID: {reading['container_id']}")
        print(f"Temperature: {reading['temperature_c']} °C")
        print(f"Humidity: {reading['humidity_percent']} %")
        print(f"Vibration: {reading['vibration_mm_s']} mm/s")
        print(f"Sensor Status: {reading.get('sensor_status', 'Not provided')}")        
        print("-" * 40)

except KeyboardInterrupt:
    print("\nConsumer stopped.")

finally:
    consumer.close()
