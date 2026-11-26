# AtmoSync – Data Sources and Dataset Documentation

## 1. Project Overview

AtmoSync uses synthetic sensor data, agricultural market-price information, and reference fault datasets to develop a micro-climate monitoring and analytics prototype.

The datasets are used for research, reference analysis, and prototype development. Not all datasets directly represent refrigerated transportation conditions.

The project currently implements sensor simulation, Kafka event streaming, Snowflake data storage, dbt transformations, and Power BI dashboard visualization.

## 2. Synthetic Sensor Dataset

**File:** `sensor_readings.csv`  
**Source:** Generated using the AtmoSync Python simulator.

**Columns:**
- timestamp
- container_id
- temperature_c
- humidity_percent
- vibration_mm_s
- sensor_status

**Generated details:**
- Records per simulation run: 20
- Containers: 2
- Readings per container per run: 10
- Container IDs: CONT_001 and CONT_002

**Latest Snowflake storage details:**
- Total verified records: 40
- CONT_001: 20 records
- CONT_002: 20 records

The Snowflake records include previously loaded data and the latest simulation data.

**Purpose in AtmoSync:**
- Simulate transportation sensor readings.
- Test prototype validation logic.
- Demonstrate Kafka event streaming.
- Load sensor records into Snowflake.
- Perform transformations and analytics using dbt.
- Visualize sensor metrics using Power BI.

**Limitation:**

The readings are synthetic and do not represent measurements from physical transportation containers.

## 3. Agricultural Market Price Dataset – Kaggle

**File:** `daily_price.csv`  
**Source:** [Agricultural Commodity Prices in India – Kaggle](https://www.kaggle.com/code/arvindkhoda/price-of-agricultural-commodities-data/input)

**Columns:**
- State
- District
- Market
- Commodity
- Variety
- Grade
- Min Price
- Max Price
- Modal Price

**Inspected details:**
- Records: 5,557
- Columns: 9
- States: 23
- Districts: 245
- Markets: 531
- Commodities: 186
- Tomato records: 225
- Arrival Date column: Not available
- Price unit: Not independently verified

**Purpose in AtmoSync:**

This dataset provides a reference for comparing agricultural commodity prices across markets.

**Limitation:**

The dataset does not contain an arrival-date column. Therefore, it cannot independently support historical price trend analysis or time-series forecasting.

The dataset has not yet been integrated into the current Snowflake analytics pipeline.

## 4. Tomato Market Price Research – AGMARKNET

**Source:** AGMARKNET / Ministry of Agriculture and Farmers Welfare, Government of India.

**Research selection:**
- Commodity: Tomato
- State: Maharashtra
- District: Kolhapur
- Research period: 1 October 2026 – 16 November 2026

**Observed research details:**
- The portal displayed 74 matching records.
- 10 records were visible in the inspected result.
- Sample modal price values included 1000, 800, and 900.
- Price units and complete dataset metadata still require verification.
- Full dataset download was not completed.

**Purpose in AtmoSync:**

The research explores the availability of dated tomato market-price information for future market comparison and price analysis.

**Limitation:**

This is preliminary source research. The complete dataset has not been downloaded or integrated into Snowflake.

## 5. Industrial Fault Detection Dataset

**File:** `industrial_fault_detection_data_1000.csv`  
**Source:** [Industrial IoT Fault Detection – Kaggle](https://www.kaggle.com/code/amandaillona/shapelet-propo/input)

**Columns:**
- Timestamp
- Vibration (mm/s)
- Temperature (°C)
- Pressure (bar)
- RMS Vibration
- Mean Temp
- Fault Label

**Inspected details:**
- Records: 1,000
- Columns: 7
- Time interval: One minute between records
- Fault Label 0: 609 records
- Fault Label 1: 303 records
- Fault Label 2: 88 records
- Missing values: None observed during inspection

**Purpose in AtmoSync:**

Reference for understanding industrial sensor readings, vibration analysis, and fault-detection concepts.

**Limitation:**

This dataset represents industrial machinery, not refrigerated transport containers. Its fault labels are not used as verified food-spoilage labels.

## 6. Sensor Fault Detection Dataset

**File:** `sensor-fault-detection.csv`  
**Source:** [Sensor Fault Detection Data – Kaggle](https://www.kaggle.com/code/kerneler/starter-sensor-fault-detection-data-5681d09f-8/input)

**Columns:**
- Timestamp
- SensorId
- Value

**Inspected details:**
- Records: 62,629
- Columns: 3
- Separator: Semicolon (;)
- Sensor ID: 1
- Date range: 1 August 2016 – 1 September 2017
- Sensor description: PT100 temperature sensor in an industrial environment

**Purpose in AtmoSync:**

Reference for timestamp-based sensor readings and sensor-event analysis.

**Limitation:**

The source describes an industrial PT100 sensor. Its readings are not assumed to represent refrigerated-container conditions.

## 7. Dataset Selection and Usage

| Dataset | Purpose | Current Status |
|---|---|---|
| Synthetic Sensor Data | Container monitoring prototype | Generated and tested |
| Kaggle Market Prices | Commodity price reference | Inspected |
| AGMARKNET Tomato Prices | Dated market-price research | Preliminary research |
| Industrial Fault Detection | Fault-analysis reference | Inspected |
| Sensor Fault Detection | Sensor-event reference | Inspected |

## 8. Data Quality and Verification

- The three downloaded reference CSV datasets were inspected.
- Dataset structures and column names were recorded.
- Missing-value checks were performed during dataset inspection.
- Unknown units and unverified meanings are not assumed.
- Original downloaded datasets are preserved unchanged.
- Synthetic sensor data was generated and validated through the Python simulator.
- Kafka Producer and Consumer were successfully tested.
- A total of 40 sensor records were verified in Snowflake.
- dbt staging and container analytics models were successfully executed.
- Eleven dbt data quality tests passed successfully (PASS=11, WARN=0, ERROR=0).
- Snowflake sensor data was imported into Power BI.
- Dashboard charts, KPI cards, and a container slicer were implemented.
- Market-price integration into the current Snowflake analytics pipeline is still pending.

## 9. Pending Data Requirements

1. Complete and verified dated tomato market-price data.
2. Verification of market-price units and source metadata.
3. Integration of market-price records into Snowflake.
4. Market-wise price comparison and analytics.
5. Verification of dataset licensing before redistribution.
6. Additional validated cold-chain sensor data for more realistic analysis.

## 10. Research Status

Initial reference dataset inspection has been completed.

Synthetic sensor data generation, Kafka Producer and Consumer testing, Snowflake sensor-data loading, dbt transformations, and Power BI dashboard development have been implemented and tested.

Tomato market-price research using AGMARKNET has been initiated, but complete data acquisition and integration remain pending.

The project continues to distinguish synthetic prototype data, reference datasets, and verified market-price information.

---

**Project:** AtmoSync – Micro-Climate Arbitrage Analytics  
**Developer:** Shweta Jathar  
**Repository:** [AtmoSync on GitHub](https://github.com/jatharshweta/AtmoSync-MicroClimate-Analytics-)
