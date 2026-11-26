# AtmoSync – Micro-Climate Arbitrage Analytics

**An IoT Data Streaming and Analytics Prototype for Perishable Agricultural Transportation**

## About the Project

AtmoSync is a data analytics prototype designed to monitor simulated micro-climate conditions during the transportation of perishable agricultural products and explore agricultural market-price opportunities.

The project combines Python-based sensor simulation, Apache Kafka event streaming, Snowflake cloud data warehousing, dbt-based data transformation, and Power BI visualization.

It demonstrates how transportation sensor readings can be generated, streamed, stored, transformed, analyzed, and visualized through a data analytics workflow.

## Project Objectives

- Simulate sensor readings for multiple transportation containers.
- Validate temperature, humidity, and vibration readings.
- Stream sensor events using Apache Kafka.
- Store sensor readings in Snowflake.
- Transform raw sensor data using dbt.
- Perform container-level analytics.
- Visualize sensor metrics through Power BI.
- Explore agricultural commodity market-price information.
- Prepare analytics-ready data for future decision-support applications.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Sensor simulation and validation |
| Apache Kafka 4.4.0 | Event streaming |
| Snowflake | Cloud data warehouse |
| dbt | Data transformation and testing |
| SQL | Data querying and analytics |
| Power BI | Interactive analytics dashboard |
| GitHub | Version control and project documentation |

## System Architecture

AtmoSync uses two connected but separate data paths.

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
```

### 2. Data Warehousing and Analytics

```text
sensor_readings.csv
        |
        | Manual CSV Upload
        v
Snowflake Stage
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
Power BI Dashboard
```

**Note:** Kafka Producer and Consumer are implemented and tested separately. Sensor data is uploaded to Snowflake through a manual CSV upload process. Automatic Kafka-to-Snowflake integration is not implemented.

Market-price information is researched separately and is intended for future integration.

## Implemented Features

### 1. Sensor Data Simulation

- Generates 20 synthetic sensor readings per simulation run.
- Simulates two transportation containers.
- Generates temperature, humidity, and vibration values.
- Saves readings in CSV format.
- Performs basic validation using configured prototype ranges.

### 2. Apache Kafka Integration

- Kafka 4.4.0 configured in KRaft mode.
- Created the `sensor_readings` topic.
- Implemented Python Kafka Producer.
- Implemented Python Kafka Consumer.
- Successfully published 20 sensor messages during testing.
- Verified message reception through the Consumer.

### 3. Snowflake Data Warehouse

Created the following database objects:

- Database: `ATMOSYNC_DB`
- Schema: `RAW`
- Table: `SENSOR_READINGS`
- Stage: `ATMOSYNC_CSV_STAGE`

The CSV data was uploaded manually through Snowflake.

**Latest verified database status:**

- Total sensor records: 40
- Container 1: 20 records
- Container 2: 20 records

The 40 records include previously loaded data and the latest simulation data.

### 4. dbt Data Transformation

Implemented two dbt models:

**stg_sensor_readings**

- Structures raw sensor readings.
- Applies prototype condition checks.
- Classifies readings as `VALID` or `CHECK_REQUIRED`.

**container_analytics**

- Calculates total readings per container.
- Computes average temperature.
- Computes average humidity.
- Computes average vibration.
- Counts readings requiring checks.

### 5. dbt Data Quality Testing

Implemented tests for required columns and accepted status values.

**Latest recorded test result:**

- Total tests: 11
- Passed: 11
- Failed: 0
- Warnings: 0

Both dbt models were successfully executed.

### 6. Power BI Dashboard

Connected Power BI Desktop to Snowflake and imported the `SENSOR_READINGS` table.

The dashboard includes:

- Temperature Monitoring – Line Chart
- Humidity Monitoring – Line Chart
- Vibration Monitoring – Line Chart
- Container-wise Average Temperature – Clustered Column Chart
- Total Sensor Readings – KPI Card
- Average Temperature – KPI Card
- Average Humidity – KPI Card
- Average Vibration – KPI Card
- Container ID – Interactive Slicer

**Verified dashboard metrics:**

| Metric | Value |
|---|---:|
| Total Sensor Readings | 40 |
| Average Temperature | 5.49 °C |
| Average Vibration | 0.46 mm/s |

Humidity is displayed in the dashboard; its exact average is not included here.

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
│   └── consumer.py
│
├── atmosync_dbt/
│   ├── dbt_project.yml
│   ├── models/
│   │   ├── stg_sensor_readings.sql
│   │   ├── container_analytics.sql
│   │   └── example/
│   │       ├── my_first_dbt_model.sql
│   │       ├── my_second_dbt_model.sql
│   │       └── schema.yml
│   ├── analyses/
│   ├── macros/
│   ├── seeds/
│   ├── snapshots/
│   └── tests/
│
└── AtmoSync_MicroClimate_Dashboard.pbix
```

## Data Sources

The project uses:

- Synthetic sensor readings generated by the Python simulator.
- Agricultural commodity market-price reference data.
- Public industrial sensor and fault datasets for reference research.
- Preliminary AGMARKNET research for tomato prices in Maharashtra.

Refer to [data_sources.md](data_sources.md) for dataset details, sources, and limitations.

## Current Project Status

| Component | Status |
|---|---|
| Python Sensor Simulator | Implemented |
| Kafka Producer and Consumer | Tested |
| Snowflake Sensor Data Loading | Tested |
| Snowflake Data Records | 40 Verified |
| dbt Staging Model | Tested |
| dbt Container Analytics | Tested |
|dbt data quality tests | 18 tests passed |
| Power BI Dashboard | Implemented |
| GitHub Documentation | Maintained |
| Market Price Integration | Pending |
| Automatic Kafka-to-Snowflake Integration | Pending |

## Assumptions and Limitations

- Sensor readings are synthetic and generated for prototype testing.
- Configured sensor ranges are prototype assumptions, not verified tomato transportation standards.
- `VALID` indicates compliance with configured prototype ranges only; it does not confirm food safety or absence of spoilage.
- Kafka-to-Snowflake automatic streaming has not been implemented.
- CSV data is manually uploaded to Snowflake.
- Market-price units and complete date coverage require further verification.
- No validated spoilage prediction model or destination recommendation engine has been implemented.
- Agricultural market-price integration remains future work.

## Future Scope

- Integrate verified, dated agricultural market-price data.
- Develop market-wise commodity price comparisons.
- Automate Kafka-to-Snowflake data ingestion.
- Develop interactive monitoring dashboards and advanced analytics.
- Explore validated anomaly detection and transportation decision-support methods.

## Documentation

- [Project Architecture](project_architecture.md)
- [Data Sources and Dataset Documentation](data_sources.md)

---

**Project:** AtmoSync – Micro-Climate Arbitrage Analytics  
**Developer:** Shweta Jathar  
**Repository:** [AtmoSync on GitHub](https://github.com/jatharshweta/AtmoSync-MicroClimate-Analytics-)
