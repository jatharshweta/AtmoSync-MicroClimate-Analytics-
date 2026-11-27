# AtmoSync – Data Sources and Dataset Documentation

## 1. Project Overview

AtmoSync uses synthetic sensor data, agricultural market-price reference information, and industrial fault datasets to develop a micro-climate monitoring and analytics prototype.

The project implements Python sensor simulation, Apache Kafka event streaming, Snowflake data storage, dbt transformations, and analytics-ready datasets.

The project distinguishes between synthetic prototype data, external reference datasets, and mock market-price data.

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

**Latest verified Snowflake storage details:**
- Total records: 40
- CONT_001: 20 records
- CONT_002: 20 records

**Purpose in AtmoSync:**
- Simulate transportation sensor readings.
- Test prototype validation logic.
- Demonstrate Kafka event streaming.
- Load sensor records into Snowflake.
- Perform transformations and analytics using dbt.
- Prepare data for business intelligence dashboards.

**Limitation:**

The readings are synthetic and do not represent measurements from physical transportation containers.

## 3. Agricultural Market Price Reference Dataset – Kaggle

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

**Purpose:**

Reference for understanding agricultural commodity prices and market-wise price comparisons.

**Limitation:**

This dataset has not been integrated into the current Snowflake analytics pipeline. It does not contain an arrival-date column, so it cannot independently support historical price trends or time-series forecasting.

## 4. Tomato Market Price Research – AGMARKNET

**Source:** AGMARKNET / Ministry of Agriculture and Farmers Welfare, Government of India.

**Research selection:**
- Commodity: Tomato
- State: Maharashtra
- District: Kolhapur
- Research period: 1 October 2026 – 16 November 2026

**Observed research details:**
- Portal displayed 74 matching records.
- 10 records were visible in the inspected result.
- Sample modal price values included 1000, 800, and 900.
- Price units and complete metadata require verification.
- Full dataset download was not completed.

**Purpose:**

Explore dated tomato market-price information for future market comparison.

**Limitation:**

This is preliminary research. The complete dataset has not been downloaded or integrated into Snowflake.

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

**Purpose:**

Reference for understanding industrial sensor readings, vibration analysis, and fault-detection concepts.

**Limitation:**

This dataset represents industrial machinery, not refrigerated transport containers. Its fault labels are not treated as verified food-spoilage labels.

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

**Purpose:**

Reference for timestamp-based sensor readings and sensor-event analysis.

**Limitation:**

The source describes an industrial PT100 sensor. Its readings are not assumed to represent refrigerated-container conditions.

## 7. AtmoSync Mock Market Price Seed

**File:** `market_prices.csv`  
**Location:** `atmosync_dbt/seeds/market_prices.csv`  
**Source:** Synthetic mock reference data prepared for the project prototype.

**Sample market information:**

| Market | Commodity | Price per kg | Distance (km) |
|---|---|---:|---:|
| Kolhapur Market | Tomato | 30 | 40 |
| Pune Market | Tomato | 42 | 230 |
| Mumbai Market | Tomato | 50 | 375 |
| Sangli Market | Tomato | 35 | 50 |

**Purpose:**
- Demonstrate market-wise price comparisons.
- Join market information with container analytics.
- Prepare exploratory market recommendation outputs.

**Limitation:**

These values are mock demonstration data, not verified current market prices.

## 8. Container Route Dataset

**File:** `container_routes.csv`  
**Location:** `atmosync_dbt/seeds/container_routes.csv`  
**Source:** Synthetic route data created for the project prototype.

**Columns:**
- container_id
- origin
- destination
- departure_timestamp
- arrival_timestamp
- distance_km

**Purpose:**
- Analyze historical route records.
- Calculate travel duration.
- Prepare route-based analytics.

**Limitation:**

The route records are synthetic and do not represent verified GPS tracking or actual transportation journeys.

## 9. Dataset Selection and Usage

| Dataset | Purpose | Current Status |
|---|---|---|
| Synthetic Sensor Data | Container monitoring | Generated and loaded |
| Kaggle Market Prices | Commodity price reference | Inspected |
| AGMARKNET Tomato Prices | Dated market-price research | Preliminary research |
| Industrial Fault Detection | Fault-analysis reference | Inspected |
| Sensor Fault Detection | Sensor-event reference | Inspected |
| Mock Market Prices | Market comparison prototype | Loaded as dbt seed |
| Container Routes | Route analysis prototype | Loaded as dbt seed |

## 10. Data Quality and Verification

- Three downloaded reference CSV datasets were inspected.
- Dataset structures and column names were recorded.
- Missing-value checks were performed during dataset inspection.
- Unknown units and unverified meanings are not assumed.
- Original downloaded datasets are preserved unchanged.
- Synthetic sensor data was generated using the Python simulator.
- Kafka Producer and Consumer were tested separately.
- Snowflake raw table contains 40 verified sensor records.
- dbt Snowflake connection test completed successfully.
- Two seed datasets were successfully loaded.
- Seven dbt table models were built successfully.
- All 33 dbt data quality tests passed (PASS=33, WARN=0, ERROR=0).
- Automatic Kafka-to-Snowflake streaming remains unverified.
- Apache Superset deployment and dashboard development remain pending.

## 11. Pending Data Requirements

1. Complete and verified dated tomato market-price data.
2. Verification of market-price units and source metadata.
3. Integration of verified market-price records into Snowflake.
4. Validation of market-wise price comparison logic.
5. Verification of dataset licensing before redistribution.
6. Additional validated cold-chain sensor data.
7. Live Kafka-to-Snowflake ingestion verification.

## 12. Research Status

Initial reference dataset inspection has been completed.

Synthetic sensor data generation, Kafka Producer and Consumer testing, Snowflake sensor-data loading, dbt transformations, seed loading, and dbt data quality testing have been implemented and tested.

Tomato market-price research using AGMARKNET has been initiated, but complete data acquisition and integration remain pending.

The project continues to distinguish synthetic prototype data, reference datasets, and verified market-price information.

---

**Project:** AtmoSync – Micro-Climate Arbitrage Analytics  
**Developer:** Shweta Jathar  
**Repository:** [AtmoSync on GitHub](https://github.com/jatharshweta/AtmoSync-MicroClimate-Analytics-)
