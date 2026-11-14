# AtmoSync: Micro-Climate Arbitrage Analytics

**Infotact Data Analytics Internship Project**

## 1. Project Overview

AtmoSync is a data analytics project designed to monitor container-level environmental conditions during the transportation of perishable commodities.

The system aims to analyze IoT sensor data, commodity market prices, and transportation routes to identify potential spoilage risks and profitable alternative markets.

## 2. Problem Statement

Traditional supply-chain analytics often rely on standard transit times and general weather forecasts. These methods may overlook the actual environmental conditions inside individual shipping containers.

Temperature, humidity, and vibration variations can affect the quality of perishable commodities during transportation.

AtmoSync aims to address this challenge through micro-climate monitoring and data-driven arbitrage analysis.

## 3. Project Objectives

- Simulate IoT sensor data for transportation containers.
- Stream sensor data using Apache Kafka.
- Store raw sensor data and historical commodity prices in Snowflake.
- Transform and analyze data using dbt.
- Identify containers with potential spoilage risks.
- Compare commodity prices across alternative markets.
- Calculate potential rerouting opportunities.
- Visualize insights through Apache Superset dashboards.

## 4. Technology Stack

| Technology | Purpose |
|---|---|
| Python | IoT data simulation |
| Apache Kafka | Real-time data streaming |
| Snowflake | Cloud data warehouse |
| dbt | Data transformation and modeling |
| Apache Superset | Data visualization and dashboards |
| SQL | Data querying and analysis |

## 5. Project Workflow

1. Generate simulated IoT sensor readings.
2. Stream sensor events through Kafka.
3. Store raw data in Snowflake.
4. Clean and transform data using dbt.
5. Analyze container conditions and commodity prices.
6. Calculate spoilage risk and potential arbitrage margins.
7. Display insights using Apache Superset.

## 6. Initial Commodity

**Avocado**

The initial analysis will focus on avocado transportation, environmental conditions, quality risk, and market price differences.

## 7. Expected Outcomes

- Container-level environmental monitoring.
- Identification of potentially at-risk shipments.
- Data-driven alternative market recommendations.
- Estimated financial benefits of rerouting.
- An interactive analytics dashboard.

## 8. Project Status

**Status:** In Progress

This repository is being developed as part of the Infotact Data Analytics Internship.

---

*Developed by Shweta Jathar*
