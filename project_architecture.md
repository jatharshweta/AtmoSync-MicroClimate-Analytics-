# AtmoSync – Micro-Climate Arbitrage Analytics

## 1. Project Overview

AtmoSync is a data analytics prototype designed to monitor simulated micro-climate conditions during the transportation of perishable agricultural products and explore agricultural market-price opportunities.

The system focuses on sensor parameters such as temperature, humidity, and vibration. It combines Python-based sensor simulation, Apache Kafka event streaming, Snowflake cloud data warehousing, dbt-based data transformation, and Power BI visualization.

The prototype demonstrates how transportation sensor information can be generated, streamed, stored, transformed, and visualized through a data analytics workflow.

## 2. Project Objectives

- Simulate IoT sensor readings for multiple transportation containers.
- Validate sensor readings against configured prototype ranges.
- Stream sensor data using Apache Kafka.
- Store sensor readings in Snowflake.
- Transform raw sensor data into analytics-ready datasets using dbt.
- Perform container-level analytics.
- Visualize sensor metrics using Power BI.
- Explore agricultural commodity market-price information.
- Prepare data for future transportation decision-support applications.

## 3. Technology Stack

| Technology | Responsibility |
|---|---|
| Python | Sensor data simulation and validation |
| Apache Kafka 4.4.0 | Sensor event streaming |
| Snowflake | Cloud data warehouse |
| dbt | SQL-based data transformation and testing |
| SQL | Data querying and analytics |
| Power BI | Interactive dashboard and visualization |
| CSV | Sensor data storage and transfer |
| GitHub | Version control and project documentation |

## 4. System Architecture

AtmoSync uses two separate but related data workflows.

### 4.1 Sensor Event Streaming Workflow

**Python IoT Simulator → CSV → Kafka Producer → Kafka Topic → Python Kafka Consumer**

The Python simulator generates sensor readings and stores them in a CSV file. The Kafka Producer reads the CSV records and publishes them as JSON messages to the Kafka topic. The Kafka Consumer receives and displays the messages.

### 4.2 Data Warehousing and Analytics Workflow

**Sensor CSV → Snowflake Stage → Snowflake RAW Table → dbt Staging Model → dbt Container Analytics → Power BI Dashboard**

The generated CSV file is uploaded manually to Snowflake. dbt transforms the raw sensor data into analytics-ready models, which are imported into Power BI for visualization.

**Important:** Automatic Kafka-to-Snowflake integration has not been implemented. Kafka streaming and Snowflake data loading are tested as separate workflows.

Agricultural market-price information is researched separately and is intended for future integration.

## 5. Component Description

### 5.1 Python IoT Simulator

The Python simulator generates synthetic sensor readings for multiple transportation containers.

The current simulation generates:
- Temperature readings
- Humidity readings
- Vibration readings
- Timestamps
- Container identifiers
- Sensor validation status

The simulator generates 20 readings for two containers, with 10 readings per container in each simulation run.

The generated readings are stored in `sensor_readings.csv`.

Configured prototype validation ranges:

| Parameter | Prototype Range |
|---|---|
| Temperature | 2–8 °C |
| Humidity | 80–95% |
| Vibration | 0.1–0.8 mm/s |

These are configurable prototype assumptions, not verified tomato transportation standards.

A reading outside the configured ranges receives the status `CHECK_REQUIRED`. A reading within the ranges receives `VALID`.

### 5.2 Apache Kafka

Apache Kafka is implemented as the event-streaming layer.

- **Broker:** Kafka 4.4.0 running locally in KRaft mode.
- **Topic:** `sensor_readings`.
- **Producer:** Python Kafka Producer reads `sensor_readings.csv` and publishes sensor records as JSON messages.
- **Consumer:** Python Kafka Consumer receives and displays messages from the topic.

The Producer successfully published 20 sensor messages during testing. The Consumer was tested and successfully received messages from the Kafka topic.

### 5.3 Snowflake

Snowflake is implemented as the cloud data warehouse.

The following database objects were created:

- Database: `ATMOSYNC_DB`
- Schema: `RAW`
- Table: `SENSOR_READINGS`
- Stage: `ATMOSYNC_CSV_STAGE`

The table contains six columns:

- `TIMESTAMP`
- `CONTAINER_ID`
- `TEMPERATURE_C`
- `HUMIDITY_PERCENT`
- `VIBRATION_MM_S`
- `SENSOR_STATUS`

The generated `sensor_readings.csv` file was uploaded manually through Snowflake.

**Latest verified database status:**

- Total sensor records: 40
- `CONT_001`: 20 records
- `CONT_002`: 20 records

The 40 records include previously loaded data and the latest simulation data.

### 5.4 dbt

dbt is implemented for SQL-based data transformation and data quality testing.

The dbt project contains two main transformation models.

**A. stg_sensor_readings**

This staging model:
- Reads data from the Snowflake RAW sensor table.
- Structures raw sensor readings.
- Applies configured prototype condition checks.
- Classifies readings as `VALID` or `CHECK_REQUIRED`.

**B. container_analytics**

This model performs container-level aggregation and calculates:
- Total readings
- Average temperature
- Average humidity
- Average vibration
- Number of readings requiring checks

Both models were successfully executed in Snowflake through dbt.

The dbt data quality tests were also executed successfully.

**Latest recorded testing result:**
- Total tests: 7
- Passed: 7
- Failed: 0

### 5.5 Power BI

Power BI Desktop is implemented as the visualization layer.

Power BI was successfully connected to Snowflake, and the `SENSOR_READINGS` table was imported for dashboard development.

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

The dashboard is saved as `AtmoSync_MicroClimate_Dashboard.pbix`.

## 6. Data Sources

AtmoSync uses the following data categories:

1. **Synthetic sensor data:** Generated by the Python simulator for prototype testing.
2. **Agricultural market-price data:** Commodity and market-price records researched for price analysis.
3. **Reference fault datasets:** Public industrial sensor and fault datasets used for understanding sensor behaviour and fault-analysis concepts.

The reference fault datasets are not treated as actual refrigerated-container telemetry.

Tomato in Maharashtra, particularly the Kolhapur market context, was selected for further market-price research.

Refer to `data_sources.md` for dataset details, sources, and limitations.

## 7. Data Flow

### 7.1 Sensor Simulation and Streaming

1. Python simulator generates synthetic sensor readings for two containers.
2. The validation function checks readings against configured prototype ranges.
3. The readings are saved in `sensor_readings.csv`.
4. Python Kafka Producer reads the CSV records.
5. Producer publishes 20 JSON messages to the `sensor_readings` topic.
6. Python Kafka Consumer receives and displays messages.

### 7.2 Data Warehousing and Analytics

1. The sensor CSV file is uploaded manually to the Snowflake stage.
2. The sensor data is loaded into the Snowflake RAW table.
3. The latest verified Snowflake table contains 40 records.
4. dbt staging model transforms the raw sensor readings.
5. dbt container analytics model calculates container-level metrics.
6. dbt tests validate required columns and allowed prototype status values.
7. Power BI imports the Snowflake sensor table.
8. Dashboard charts, KPI cards, and a container slicer visualize the sensor data.

## 8. Current Implementation Status

| Component | Status |
|---|---|
| Python sensor simulator | Implemented and tested |
| Multi-container data generation | Implemented |
| Basic sensor validation | Implemented and tested |
| CSV output generation | Implemented and tested |
| Kafka 4.4.0 broker setup | Implemented and tested |
| Kafka KRaft configuration | Implemented |
| `sensor_readings` topic | Created and verified |
| Python Kafka Producer | Implemented and tested |
| Python Kafka Consumer | Implemented and tested |
| Publishing 20 sensor messages | Successfully tested |
| Snowflake database and RAW schema | Created |
| Snowflake sensor table | Created |
| Snowflake sensor records | 40 records verified |
| dbt-Snowflake connection | Successfully tested |
| `stg_sensor_readings` model | Implemented and tested |
| `container_analytics` model | Implemented and tested |
| dbt data quality tests | 7 tests passed |
| Power BI Snowflake connection | Successfully tested |
| Power BI dashboard | Implemented |
| Automatic Kafka-to-Snowflake integration | Pending |
| Market-price integration with analytics pipeline | Pending |

## 9. Assumptions and Limitations

- Sensor readings are synthetic and generated for prototype testing.
- Temperature, humidity, and vibration thresholds are configurable assumptions, not verified storage or transportation standards for tomatoes.
- `VALID` means a reading falls within the configured prototype ranges. It does not confirm that the transported product is safe or free from spoilage.
- Kafka-to-Snowflake automatic streaming has not been implemented.
- CSV data is manually uploaded to Snowflake.
- The market-price dataset requires verification of date coverage, units, and source metadata before detailed price comparisons.
- Reference industrial and sensor fault datasets do not represent actual refrigerated-container conditions.
- No validated spoilage prediction model has been developed.
- Reliable destination recommendations require verified market data, transportation costs, defined business rules, and further validation.
- Market-price integration with the sensor analytics pipeline remains pending.

## 10. Expected Outcome

The implemented AtmoSync prototype demonstrates sensor simulation, event streaming, cloud data storage, SQL-based transformation, data quality testing, and interactive dashboard visualization.

The Power BI dashboard provides a visual summary of temperature, humidity, vibration, and container-level sensor metrics.

Future development can extend the prototype with verified market-price integration, automated data ingestion, advanced analytics, and validated transportation decision-support logic.

---

**Project:** AtmoSync – Micro-Climate Arbitrage Analytics  
**Developer:** Shweta Jathar  
**Repository:** [AtmoSync on GitHub](https://github.com/jatharshweta/AtmoSync-MicroClimate-Analytics-)
