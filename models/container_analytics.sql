{{ config(materialized='table') }}

SELECT
    container_id,
    COUNT(*) AS total_readings,
    ROUND(AVG(temperature_c), 2) AS avg_temperature,
    ROUND(AVG(humidity_percent), 2) AS avg_humidity,
    ROUND(AVG(vibration_mm_s), 2) AS avg_vibration,

    SUM(
        CASE
            WHEN prototype_condition = 'CHECK_REQUIRED'
            THEN 1
            ELSE 0
        END
    ) AS check_required_count

FROM {{ ref('stg_sensor_readings') }}

GROUP BY container_id
