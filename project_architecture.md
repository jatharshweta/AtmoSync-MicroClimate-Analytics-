# AtmoSync – Micro-Climate Arbitrage Analytics

## 1. Project Overview

AtmoSync is a data analytics prototype designed to monitor simulated micro-climate conditions during the transportation of perishable agricultural products and explore agricultural market-price opportunities.

The system focuses on sensor parameters such as temperature, humidity, and vibration. It combines Python-based sensor simulation, Apache Kafka event streaming, Snowflake cloud data warehousing, dbt-based data transformation, and Apache Superset for business intelligence visualization.

The prototype demonstrates how transportation sensor information can be generated, streamed, stored, transformed, and prepared for analytics through a data engineering and business intelligence workflow.

## 2. Project Objectives

- Simulate IoT sensor readings for multiple transportation containers.
- Validate sensor readings against configured prototype ranges.
- Stream sensor data using Apache Kafka.
- Store sensor readings in Snowflake.
- Transform raw sensor data into analytics-ready datasets using dbt.
- Perform container-level sensor analytics.
- Analyze temperature, humidity, and vibration patterns.
- Prepare datasets for Apache Superset dashboards.
- Explore agricultural commodity market-price information.
- Prepare data for future transportation decision-support applications.

## 3. Technology Stack

| Technology | Responsibility |
|---|---|
| Python | Sensor data simulation and validation |
| Apache Kafka 4.4.0 | Sensor event streaming |
| Snowflake | Cloud data warehouse |
| dbt Core | SQL-based data transformation and testing |
| SQL | Data querying and analytics |
| Apache Superset | Planned BI dashboard and visualization layer |
| CSV | Data storage, transfer, and seed files |
| Git and GitHub | Version control and project documentation |

## 4. System Architecture

AtmoSync currently uses separate sensor-streaming and data-warehousing workflows.

### 4.1 Sensor Event Streaming Workflow

**Python IoT Simulator → CSV → Kafka Producer → Kafka Topic → Python Kafka Consumer**

The Python simulator generates synthetic sensor readings and stores them in a CSV file.

The Kafka Producer reads the generated CSV records and publishes them as JSON messages to the `sensor_readings` Kafka topic.

The Kafka Consumer receives messages from the topic and displays the sensor events.

**Current limitation:** Kafka streaming and Snowflake data loading have been tested as separate workflows. Automatic Kafka-to-Snowflake integration is not yet verified.

### 4.2 Data Warehousing and Analytics Workflow

**Sensor CSV → Snowflake RAW Table → dbt Staging Model → dbt Analytics Models → Analytics-ready Tables**

The generated sensor CSV file is uploaded manually to Snowflake.

dbt reads the raw sensor data, applies transformations, calculates container-level metrics, and prepares analytics-ready tables.

Apache Superset is planned as the BI visualization layer. Its deployment, Snowflake connection, and dashboard development are pending.

### 4.3 Market and Route Analytics Workflow

**Mock Market Price CSV + Container Route CSV → dbt Seeds → dbt Models → Analytics-ready Data**

Synthetic market-price and container-route datasets are loaded through dbt seeds.

These datasets are used to demonstrate market comparison and route analytics within the prototype. They are not verified real-time market prices or actual transportation records.

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

**Simulation details:**

- Records per simulation run: 20
- Number of containers: 2
- Readings per container per run: 10
- Container IDs: `CONT_001` and `CONT_002`

The generated readings are stored in `sensor_readings.csv`.

**Configured prototype validation ranges:**

| Parameter | Prototype Range |
|---|---|
| Temperature | 2–8 °C |
| Humidity | 80–95% |
| Vibration | 0.1–0.8 mm/s |

These are configurable prototype assumptions, not verified tomato transportation standards.

A reading outside the configured ranges receives the status `CHECK_REQUIRED`. A reading within the configured ranges receives `VALID`.

The dbt staging model also identifies invalid or missing values using the `INVALID` classification.

### 5.2 Apache Kafka

Apache Kafka is used as the event-streaming layer.

- **Version:** Apache Kafka 4.4.0
- **Mode:** KRaft
- **Topic:** `sensor_readings`
- **Producer:** Python Kafka Producer reads sensor records from CSV and publishes JSON messages.
- **Consumer:** Python Kafka Consumer receives and displays messages.

The Producer and Consumer were tested separately. During testing, the Producer successfully published 20 sensor messages and the Consumer successfully received messages.

**Limitation:** Live Kafka broker operation and end-to-end Kafka-to-Snowflake ingestion are not currently verified.

### 5.3 Snowflake

Snowflake is implemented as the cloud data warehouse.

**Database objects:**

- Database: `ATMOSYNC_DB`
- Raw Schema: `RAW`
- Table: `SENSOR_READINGS`
- Stage: `ATMOSYNC_CSV_STAGE`

The raw sensor table contains six columns:

- `TIMESTAMP`
- `CONTAINER_ID`
- `TEMPERATURE_C`
- `HUMIDITY_PERCENT`
- `VIBRATION_MM_S`
- `SENSOR_STATUS`

The generated `sensor_readings.csv` file was uploaded manually to Snowflake.

**Latest verified database status:**

| Metric | Value |
|---|---:|
| Total sensor records | 40 |
| CONT_001 records | 20 |
| CONT_002 records | 20 |

The 40 records include previously loaded data and the latest simulation data.

### 5.4 dbt Core

dbt Core is implemented for SQL-based data transformation and data quality testing.

The dbt project uses Snowflake as its data warehouse.

**Configured dbt seeds:**

1. `market_prices.csv` – mock commodity market-price information.
2. `container_routes.csv` – synthetic container route information.

**Main transformation models:**

**A. `stg_sensor_readings`**

This staging model:

- Reads data from the Snowflake RAW sensor table.
- Structures raw sensor readings.
- Converts numeric sensor values into appropriate data types.
- Applies configured prototype condition checks.
- Classifies readings as `VALID`, `CHECK_REQUIRED`, or `INVALID`.

**B. `container_analytics`**

This model performs container-level aggregation and calculates:

- Total readings
- Average temperature
- Average humidity
- Average vibration
- Number of readings requiring checks
- Market-wise reference information

**C. `spoilage_arbitrage`**

This model prepares exploratory risk classifications and recommendations based on configured sensor conditions.

It classifies records into:

- HIGH
- MEDIUM
- LOW

These are prototype risk categories, not scientifically validated spoilage predictions.

**D. `container_routes_analysis`**

This model:

- Reads synthetic route information.
- Converts departure and arrival timestamps.
- Calculates transportation duration.
- Prepares route-level analytics.

**E. `temperature_analysis`**

This model:

- Analyzes temperature readings.
- Calculates rolling average temperature.
- Classifies temperature status as HIGH, LOW, or NORMAL.

**Latest dbt execution results:**

| Operation | Result |
|---|---|
| dbt debug | Connection successful |
| dbt seed | 2 seeds loaded |
| dbt run | 7 table models built successfully |
| dbt test | 33 tests passed |
| Failed tests | 0 |

All 33 configured dbt data quality tests passed successfully.

### 5.5 Apache Superset

Apache Superset is selected as the business intelligence and visualization layer.

The planned implementation includes:

- Self-hosted Apache Superset deployment.
- Snowflake database connection.
- Dataset configuration using analytics-ready dbt tables.
- User access and role configuration.
- Temperature monitoring charts.
- Humidity monitoring charts.
- Vibration monitoring charts.
- Container-wise average temperature comparison.
- Total sensor readings KPI.
- Average temperature KPI.
- Average humidity KPI.
- Average vibration KPI.
- Container ID filter.

**Current status:** Superset deployment, Snowflake connection, role configuration, and dashboard development are pending.

## 6. Data Sources

AtmoSync uses the following data categories:

1. **Synthetic sensor data:** Generated by the Python simulator for prototype testing.
2. **Mock market-price data:** Created for demonstrating market comparison through dbt.
3. **Synthetic route data:** Created for route analysis.
4. **Agricultural market-price reference data:** Public market-price datasets researched for future integration.
5. **Reference fault datasets:** Public industrial sensor and fault datasets used for understanding sensor behaviour and fault-analysis concepts.

The industrial reference datasets are not treated as actual refrigerated-container telemetry.

Tomato in Maharashtra, particularly the Kolhapur market context, was selected for further market-price research.

Refer to `data_sources.md` for dataset details, sources, and limitations.

## 7. Data Flow

### 7.1 Sensor Simulation and Streaming

1. Python simulator generates synthetic sensor readings for two containers.
2. The validation function checks readings against configured prototype ranges.
3. The readings are saved in `sensor_readings.csv`.
4. Python Kafka Producer reads the CSV records.
5. Producer publishes JSON messages to the `sensor_readings` topic.
6. Python Kafka Consumer receives and displays messages.

### 7.2 Data Warehousing and Analytics

1. Sensor CSV file is uploaded manually to Snowflake.
2. Sensor data is loaded into the Snowflake RAW table.
3. The latest verified Snowflake table contains 40 records.
4. dbt staging model transforms the raw sensor readings.
5. dbt analytics models calculate container-level metrics and prepare route and temperature analysis.
6. dbt seeds load mock market-price and route datasets.
7. dbt tests validate required fields and configured data quality rules.
8. Analytics-ready tables are prepared for future Apache Superset dashboards.

### 7.3 Planned BI Workflow

1. Deploy self-hosted Apache Superset.
2. Configure Snowflake database connectivity.
3. Register analytics-ready dbt tables as datasets.
4. Configure user access roles.
5. Create sensor monitoring charts and KPI cards.
6. Build an interactive AtmoSync dashboard.

## 8. Current Implementation Status

| Component | Current Status |
|---|---|
| Python sensor simulator | Implemented and tested |
| Multi-container data generation | Implemented |
| Basic sensor validation | Implemented and tested |
| CSV output generation | Implemented and tested |
| Kafka 4.4.0 setup | Configured |
| Kafka KRaft configuration | Configured |
| `sensor_readings` topic | Created |
| Python Kafka Producer | Implemented and tested |
| Python Kafka Consumer | Implemented and tested |
| Publishing 20 sensor messages | Successfully tested |
| Snowflake database and RAW schema | Created |
| Snowflake sensor table | Created |
| Snowflake sensor records | 40 records verified |
| dbt-Snowflake connection | Successfully tested |
| dbt seeds | 2 loaded successfully |
| dbt table models | 7 built successfully |
| dbt data quality tests | 33 passed |
| Automatic Kafka-to-Snowflake integration | Pending verification |
| Apache Superset deployment | Pending |
| Superset-Snowflake connection | Pending |
| Superset user roles | Pending |
| Superset dashboard | Pending |
| Verified market-price integration | Pending |

## 9. Assumptions and Limitations

- Sensor readings are synthetic and generated for prototype testing.
- Temperature, humidity, and vibration thresholds are configurable assumptions, not verified storage or transportation standards for tomatoes.
- `VALID` means a reading falls within configured prototype ranges. It does not confirm that the transported product is safe or free from spoilage.
- Kafka Producer and Consumer have been tested separately; automatic Kafka-to-Snowflake streaming is not yet verified.
- CSV sensor data is manually uploaded to Snowflake.
- Mock market-price values are for demonstration only and are not verified current market prices.
- External market-price datasets require verification of date coverage, units, and source metadata before detailed price comparisons.
- Reference industrial and sensor fault datasets do not represent actual refrigerated-container conditions.
- No validated spoilage prediction model has been developed.
- Reliable destination recommendations require verified market data, transportation costs, defined business rules, and further validation.
- Apache Superset dashboard implementation is pending.

## 10. Expected Outcome

The implemented AtmoSync prototype demonstrates sensor simulation, Kafka event-streaming development, cloud data storage, SQL-based transformations, seed loading, and automated data quality testing.

The dbt analytics models prepare sensor, route, and mock market-price data for business intelligence analysis.

The planned Apache Superset dashboard will provide visual summaries of temperature, humidity, vibration, and container-level sensor metrics.

Future development can extend the prototype with verified market-price integration, automated data ingestion, advanced analytics, and validated transportation decision-support logic.

---

**Project:** AtmoSync – Micro-Climate Arbitrage Analytics  
**Developer:** Shweta Jathar  
**Repository:** [AtmoSync on GitHub](https://github.com/jatharshweta/AtmoSync-MicroClimate-Analytics-)
