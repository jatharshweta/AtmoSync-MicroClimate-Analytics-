# AtmoSync – Micro-Climate Arbitrage Analytics

**An IoT Data Streaming and Analytics Prototype for Perishable Agricultural Transportation**

## About the Project

AtmoSync is a data analytics prototype designed to monitor simulated micro-climate conditions during the transportation of perishable agricultural products and explore agricultural market-price opportunities.

The project combines Python-based sensor simulation, Apache Kafka event streaming, Snowflake cloud data warehousing, and dbt-based data transformation.

It demonstrates how transportation sensor readings can be collected, streamed, stored, transformed, and prepared for analytical applications.

## Project Objectives

- Simulate sensor readings for multiple transportation containers.
- Validate temperature, humidity, and vibration readings.
- Stream sensor events using Apache Kafka.
- Store sensor readings in Snowflake.
- Transform raw sensor data using dbt.
- Perform container-level analytics.
- Explore agricultural commodity market-price information.
- Prepare analytics-ready data for future visualization.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Sensor simulation and validation |
| Apache Kafka 4.4.0 | Event streaming |
| Snowflake | Cloud data warehouse |
| dbt | Data transformation and testing |
| SQL | Data querying and analytics |
| Apache Superset | Planned visualization |

## System Architecture

```text
Python IoT Simulator
        |
        v
sensor_readings.csv
        |
        v
Kafka Producer
        |
        v
Kafka Topic
(sensor_readings)
        |
        v
Python Kafka Consumer
        |
        v
Snowflake RAW Table
        |
        v
dbt Staging Model
        |
        v
dbt Container Analytics
        |
        v
Future Dashboard
(Apache Superset)
```

Market-price information is researched separately and is intended for future integration.

## Implemented Features

### 1. Sensor Data Simulation

- Generates 20 synthetic sensor readings.
- Simulates two transportation containers.
- Generates temperature, humidity, and vibration values.
- Saves readings in CSV format.
- Performs basic validation using configured prototype ranges.

### 2. Apache Kafka Integration

- Kafka 4.4.0 configured in KRaft mode.
- Created the `sensor_readings` topic.
- Implemented Python Kafka Producer.
- Implemented Python Kafka Consumer.
- Successfully published and received 20 sensor messages.

### 3. Snowflake Data Warehouse

Created the following database objects:

- Database: `ATMOSYNC_DB`
- Schema: `RAW`
- Table: `SENSOR_READINGS`

Successfully loaded and verified 20 sensor records.

### 4. dbt Data Transformation

Implemented two dbt models:

**stg_sensor_readings**
- Structures raw sensor readings.
- Calculates prototype condition.
- Classifies readings as `VALID` or `CHECK_REQUIRED`.

**container_analytics
