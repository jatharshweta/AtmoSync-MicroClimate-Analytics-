# AtmoSync – Micro-Climate Arbitrage Analytics

**An IoT Data Streaming and Analytics Prototype for Perishable Agricultural Transportation**

## About the Project

AtmoSync is a data analytics prototype designed to monitor simulated micro-climate conditions during the transportation of perishable agricultural products and explore agricultural market-price opportunities.

The project combines Python-based sensor simulation, Apache Kafka event streaming, Snowflake cloud data warehousing, dbt-based data transformation, and business intelligence visualization.

It demonstrates how transportation sensor readings can be generated, streamed, stored, transformed, analyzed, and prepared for visualization through a data analytics workflow.

## Project Objectives

- Simulate sensor readings for multiple transportation containers.
- Validate temperature, humidity, and vibration readings.
- Stream sensor events using Apache Kafka.
- Store sensor readings in Snowflake.
- Transform raw sensor data using dbt.
- Perform container-level analytics.
- Analyze historical container routes.
- Analyze temperature fluctuations.
- Explore agricultural commodity market prices.
- Build interactive dashboards using Apache Superset.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Sensor simulation and data processing |
| Apache Kafka 4.4.0 | Event streaming |
| Snowflake | Cloud data warehouse |
| dbt Core | Data transformation and testing |
| SQL | Data querying and analytics |
| Apache Superset | Business intelligence and visualization |
| GitHub | Version control and documentation |

## System Architecture

### 1. Sensor Event Streaming

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
Snowflake (Integration Pending)
```

### 2. Data Warehousing and Analytics

```text
sensor_readings.csv
        |
        v
Manual CSV Upload
        |
        v
Snowflake RAW Table
        |
        v
dbt Staging Model
        |
        v
dbt Analytics Models
        |
        v
Snowflake ANALYTICS Schema
        |
        v
Apache Superset (Pending)
```

**Note:** Kafka Producer and Consumer have been implemented and tested separately. The current Snowflake raw data was loaded through manual CSV upload. Automatic Kafka-to-Snowflake streaming is still pending verification.

## Implemented Features

### 1. Python IoT Sensor Simulation

- Generates synthetic sensor readings.
- Simulates two transportation containers.
- Generates temperature, humidity, and vibration values.
- Saves sensor readings in CSV format.
- Applies configurable prototype validation ranges.

### 2. Apache Kafka Integration

- Configured Kafka in KRaft mode.
- Created the `sensor_readings` topic.
- Implemented Python Kafka Producer.
- Implemented Python Kafka Consumer.
- Successfully published and received 20 sensor messages during previous testing.
- Live broker connectivity and Kafka-to-Snowflake integration require final verification.

### 3. Snowflake Data Warehouse

Created the following database objects:

- Database: `ATMOSYNC_DB`
- Raw Schema: `RAW`
- Raw Table: `SENSOR_READINGS`
- Analytics Schema: `ANALYTICS`
- Stage: `ATMOSYNC_CSV_STAGE`

**Latest verified database status:**

- Total sensor records: 40
- Container 1: 20 records
- Container 2: 20 records

### 4. dbt Data Transformation

Configured dbt Core with the Snowflake adapter.

Implemented the following models:

1. `stg_sensor_readings` – Cleans and classifies raw sensor readings.
2. `container_analytics` – Calculates container metrics and joins market-price information.
3. `spoilage_arbitrage` – Performs prototype risk classification and generates market-wise recommendations.
4. `container_routes_analysis` – Analyzes historical container routes and travel duration.
5. `temperature_analysis` – Calculates rolling average temperature and temperature status.

Additional seed datasets:

- `market_prices.csv`
- `container_routes.csv`

### 5. dbt Data Quality Testing

Implemented data quality tests for required columns and accepted values.

**Latest verified results:**

| Metric | Result |
|---|---:|
| Models built | 7 |
| Tests executed | 33 |
| Tests passed | 33 |
| Tests failed | 0 |
| Warnings | 0 |

Snowflake connection and dbt project configuration were also successfully verified using `dbt debug`.

### 6. Business Intelligence Dashboard

Apache Superset is the planned BI platform for this project.

Planned visualizations:

- Raw sensor readings table.
- Temperature fluctuation line chart.
- Humidity monitoring chart.
- Vibration monitoring chart.
- Historical container route analysis.
- Container-wise analytics.
- Market-price comparison.

**Status:** Superset deployment, Snowflake connection, user roles, and dashboard development are pending.

## Project Structure

```text
AtmoSync/
│
├── main.py
├── sensor_readings.csv
├── requirements.txt
├── project_architecture.md
├── data_sources.md
│
├── kafka/
│   ├── producer.py
│   ├── consumer.py
│   └── consumer_backup_before_snowflake.py
│
├── atmosync_dbt/
│   ├── dbt_project.yml
│   ├── seeds/
│   │   ├── market_prices.csv
│   │   └── container_routes.csv
│   │
│   └── models/
│       ├── stg_sensor_readings.sql
│       ├── container_analytics.sql
│       ├── spoilage_arbitrage.sql
│       ├── container_routes_analysis.sql
│       ├── temperature_analysis.sql
│       └── schema.yml
│
└── README.md
```

## Assumptions and Limitations

- Sensor readings are synthetic and generated for prototype testing.
- Configured sensor ranges are prototype assumptions, not verified agricultural transportation standards.
- `VALID` indicates compliance with configured prototype ranges only; it does not confirm food safety or absence of spoilage.
- Automatic Kafka-to-Snowflake integration is not yet verified.
- Current Snowflake raw data was loaded through manual CSV upload.
- Market prices are mock reference data and require validation against dated market sources.
- Risk classifications are rule-based prototype logic, not a validated spoilage prediction model.
- Market recommendations are exploratory and not production-ready decisions.

## Future Scope

- Automate Kafka-to-Snowflake ingestion.
- Integrate verified agricultural market-price data.
- Develop advanced market-wise price comparisons.
- Deploy Apache Superset dashboards.
- Explore anomaly detection and predictive analytics.
- Develop improved transportation decision-support methods.

## Documentation

- [Project Architecture](project_architecture.md)
- [Data Sources and Dataset Documentation](data_sources.md)

---

**Project:** AtmoSync – Micro-Climate Arbitrage Analytics  
**Developer:** Shweta Jathar  
**Repository:** [AtmoSync on GitHub](https://github.com/jatharshweta/AtmoSync-MicroClimate-Analytics-)
