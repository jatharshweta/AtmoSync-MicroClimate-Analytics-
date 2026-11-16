
import csv
import random
from datetime import datetime, timedelta

# AtmoSync - Multi-Container IoT Sensor Simulator

CONTAINERS = ["CONT_001", "CONT_002"]
READINGS_PER_CONTAINER = 10

# Sensor Data Validation Function

def validate_reading(reading):

    if not (2 <= reading["temperature_c"] <= 8):
        return "CHECK_REQUIRED"

    if not (80 <= reading["humidity_percent"] <= 95):
        return "CHECK_REQUIRED"

    if not (0.1 <= reading["vibration_mm_s"] <= 0.8):
        return "CHECK_REQUIRED"

    return "VALID"
# Test abnormal sensor reading

test_reading = {
    "temperature_c": 10,
    "humidity_percent": 85,
    "vibration_mm_s": 0.5
}

print("Validation Test:", validate_reading(test_reading))
data = []
start_time = datetime.now()

for container_id in CONTAINERS:

    for i in range(READINGS_PER_CONTAINER):

        reading = {
            "timestamp": (start_time + timedelta(minutes=i)).isoformat(),
            "container_id": container_id,
            "temperature_c": round(random.uniform(2, 8), 2),
            "humidity_percent": round(random.uniform(80, 95), 2),
            "vibration_mm_s": round(random.uniform(0.1, 0.8), 2)
        }
        reading["sensor_status"] = validate_reading(reading)
        data.append(reading)

# Save sensor readings to CSV
fieldnames = [
    "timestamp",
    "container_id",
    "temperature_c",
    "humidity_percent",
    "vibration_mm_s",
    "sensor_status"
]

with open("sensor_readings.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

print("AtmoSync Sensor Simulator Started!")
print(f"Total containers: {len(CONTAINERS)}")
print(f"Readings per container: {READINGS_PER_CONTAINER}")
print(f"Total readings generated: {len(data)}")
print("Data saved to sensor_readings.csv")
