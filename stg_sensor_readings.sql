{{ config(materialized='table') }}

SELECT
    "TIMESTAMP" AS reading_timestamp,
    CONTAINER_ID AS container_id,
    TEMPERATURE_C AS temperature_c,
    HUMIDITY_PERCENT AS humidity_percent,
    VIBRATION_MM_S AS vibration_mm_s,
    SENSOR_STATUS AS sensor_status,

    CASE
        WHEN TEMPERATURE_C NOT BETWEEN 2 AND 8
          OR HUMIDITY_PERCENT NOT BETWEEN 80 AND 95
          OR VIBRATION_MM_S NOT BETWEEN 0.1 AND 0.8
        THEN 'CHECK_REQUIRED'
        ELSE 'VALID'
    END AS prototype_condition

FROM ATMOSYNC_DB.RAW.SENSOR_READINGS