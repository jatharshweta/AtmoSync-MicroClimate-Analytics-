# AtmoSync – Micro-Climate Arbitrage Analytics

## 1. Project Overview

AtmoSync is a data analytics prototype designed to monitor simulated micro-climate conditions during the transportation of perishable agricultural products and analyze them alongside agricultural market-price information.

The system focuses on sensor parameters such as temperature, humidity, and vibration. It combines Python-based sensor simulation, Apache Kafka event streaming, Snowflake cloud data warehousing, and dbt-based data transformation.

The prototype aims to organize transportation sensor information into analytics-ready datasets that can support monitoring and future market-opportunity analysis.

## 2. Project Objectives

- Simulate IoT sensor readings for multiple transportation containers.
- Validate sensor readings against configured prototype ranges.
- Stream sensor data using Apache Kafka.
- Store sensor readings in Snowflake.
- Transform raw sensor data into analytics-ready datasets using dbt.
- Explore agricultural commodity market-price information.
- Prepare data for future visualization using Apache Superset.
- Explore how environmental conditions and market prices can support transportation decisions.

## 3. Technology Stack

| Technology | Responsibility |
|---|---|
| Python | Sensor data simulation and validation |
| Apache Kafka 4.4.0 | Sensor event streaming |
| Snowflake | Cloud data warehouse |
| dbt | SQL-based data transformation and testing |
| Apache Superset | Planned dashboard and visualization |
| CSV | Sensor data storage and transfer |

## 4. System Architecture

The implemented sensor-data workflow is:

**Python IoT Simulator → CSV → Kafka Producer → Kafka Topic → Python Kafka Consumer**

The sensor data is also loaded into Snowflake for analytical processing:

**Sensor CSV → Snowflake RAW Table → dbt Staging Model → dbt Container Analytics Model**

The planned visualization layer is:

**dbt Analytics Models → Apache Superset Dashboard**

Agricultural market-price data is a separate input source intended for future integration and analysis.

## 5. Component Description

### 5.1 Python IoT Simulator

The Python simulator generates synthetic sensor readings for multiple transportation containers.

The current prototype generates:
- Temperature readings
- Humidity readings
- Vibration readings
- Timestamps
- Container identifiers
- Sensor validation status

The simulator currently generates 20 readings for two containers, with 10 readings per container.

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

The producer successfully published 20 sensor readings. The Python consumer was tested and successfully received the messages.

### 5.3 Snowflake

Snowflake is implemented as the cloud data warehouse.

The following database objects were created:

- Database: `ATMOSYNC_DB`
- Schema: `RAW`
- Table: `SENSOR_READINGS`

The table contains six columns:

- TIMESTAMP
- CONTAINER_ID
- TEMPERATURE_C
- HUMIDITY_PERCENT
- VIBRATION_MM_S
- SENSOR_STATUS

The generated `sensor_readings.csv` file was loaded into the Snowflake RAW table.

The record count was verified using SQL, and 20 sensor records were successfully loaded.

### 5.4 dbt

dbt is implemented for SQL-based data transformation and data quality testing.

The dbt project contains two main transformation models.

**A. stg_sensor_readings**

This staging model:
- Reads data from the Snowflake RAW sensor table.
- Structures sensor readings into a consistent format.
- Calculates `prototype_condition` using the configured prototype ranges.
- Classifies readings as `VALID` or `CHECK_REQUIRED`.

**B. container_analytics**

This model performs container-level aggregation and calculates:
- Total readings
- Average temperature
- Average humidity
- Average vibration
- Number of readings requiring checks

Both models were successfully executed in Snowflake through dbt.

The dbt data quality tests were also executed successfully:
- Not-null tests for required columns.
- Accepted-values test for `prototype_condition`.

**Testing result: 7 tests passed, 0 warnings, 0 errors.**

### 5.5 Apache Superset

Apache Superset is the planned visualization layer.

Potential dashboard elements include:
- Container-wise temperature monitoring.
- Humidity and vibration trends.
- Sensor validation status.
- Container-level summary metrics.
- Market-wise commodity price comparisons.

The dashboard has not yet been implemented.

## 6. Data Sources

AtmoSync uses the following data categories:

1. **Synthetic sensor data:** Generated by the Python simulator for prototype testing.
2. **Agricultural market-price data:** Commodity and market-price records researched for price analysis.
3. **Reference fault datasets:** Public industrial sensor and fault datasets used for understanding sensor behaviour and fault-analysis concepts.

The reference fault datasets are not treated as actual refrigerated-container telemetry.

Tomato in Maharashtra, particularly the Kolhapur market context, was selected for further market-price research.

## 7. Data Flow

1. Python simulator generates synthetic sensor readings for two containers.
2. The validation function checks readings against configured prototype ranges.
3. The readings are saved in `sensor_readings.csv`.
4. Python Kafka Producer reads the CSV records.
5. Producer publishes 20 JSON messages to the `sensor_readings` topic.
6. Python Kafka Consumer receives and displays the published messages.
7. The sensor CSV is loaded into the Snowflake RAW table.
8. dbt staging model transforms the raw sensor readings.
9. dbt container analytics model calculates container-level metrics.
10. dbt tests validate required columns and allowed prototype status values.
11. The prepared analytics models can be used for future dashboard development.

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
| Publishing 20 sensor readings | Successfully tested |
| Snowflake database and RAW schema | Created |
| Snowflake sensor table | Created |
| Loading 20 sensor records into Snowflake | Successfully tested |
| dbt-Snowflake connection | Successfully tested |
| `stg_sensor_readings` model | Implemented and tested |
| `container_analytics` model | Implemented and tested |
| dbt data quality tests | 7 tests passed |
| Apache Superset dashboard | Planned |
| Market-price integration with analytics pipeline | Pending |

## 9. Assumptions and Limitations

- Sensor readings are synthetic and generated for prototype testing.
- Temperature, humidity, and vibration thresholds are configurable assumptions, not verified storage or transportation standards for tomatoes.
- `VALID` means a reading falls within the configured prototype ranges. It does not confirm that the transported product is safe or free from spoilage.
- The current sensor dataset contains 20 readings across two containers.
- The market-price dataset requires verification of date coverage, units, and source metadata before detailed price comparisons.
- Reference industrial and sensor fault datasets do not represent actual refrigerated-container conditions.
- No validated spoilage prediction model has been developed.
- Reliable destination recommendations require verified market data, transportation costs, defined business rules, and further validation.
- Apache Superset visualization is planned but not yet implemented.

## 10. Expected Outcome

The expected outcome is an integrated data analytics prototype that combines simulated transportation sensor readings with agricultural market-price information.

The implemented pipeline demonstrates sensor simulation, event streaming, cloud data storage, SQL-based transformation, and data quality testing.

Future development can extend the prototype with verified market-price integration, interactive dashboards, and validated transportation decision-support logic.
