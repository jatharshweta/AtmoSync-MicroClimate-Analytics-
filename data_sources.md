# AtmoSync – Data Sources and Dataset Documentation

## 1. Project Overview

AtmoSync uses market-price data and sensor-related reference datasets to develop a simulated micro-climate monitoring and arbitrage analytics pipeline.

The selected datasets are used for research, reference analysis, and development. They are not all direct refrigerated-container datasets.

## 2. Market Price Dataset

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
- Tomato records: 225
- Arrival Date column: Not available
- Price unit: Not independently verified

**Purpose in AtmoSync:** Reference for commodity and market-price analysis.

**Limitation:** This dataset does not contain a date column, so it cannot independently support historical price trend analysis or time-series forecasting.

## 3. Industrial Fault Detection Dataset

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
- Missing values: None

**Purpose in AtmoSync:** Reference for understanding industrial sensor readings, vibration analysis, and fault-detection logic.

**Limitation:** This dataset represents industrial machinery, not refrigerated transport containers. It will not be treated as actual cold-chain telemetry.

## 4. Sensor Fault Detection Dataset

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
- Sensor description: PT100 temperature sensor in an industrial environment

**Purpose in AtmoSync:** Reference for timestamp-based sensor readings and sensor-event simulation.

**Limitation:** The source describes an industrial PT100 sensor. Its readings will not be assumed to represent refrigerated-container conditions.

## 5. Dataset Selection and Usage

| Dataset | Intended use |
|---|---|
| Market Prices | Commodity price reference |
| Industrial Fault | Vibration and fault-analysis reference |
| Sensor Fault | Timestamp and sensor-event reference |

## 6. Data Quality and Verification

- All three downloaded CSV files were inspected.
- No missing values were found in the inspected files.
- Dataset structure and column names were recorded.
- Unknown units and unverified meanings will not be assumed.
- Original downloaded datasets will be preserved unchanged.
- Dataset redistribution and usage licenses must be checked before public redistribution.

## 7. Pending Data Requirements

The project still requires:

1. A verified source or clearly labelled synthetic temperature and humidity data for refrigerated-container simulation.
2. A dated market-price dataset for historical price analysis.
3. A Python-based event simulator to publish sensor readings to Kafka.
4. Validation of dataset licensing and source metadata.

## Research Status

Initial dataset inspection completed.

Dataset selection is provisional. Further verification and simulator development are pending.
