
{{ config(materialized='table') }}

SELECT
    CAST(time AS DATE) AS forecast_date,
    temp_max_c,
    temp_min_c,

    ROUND(
        temp_max_c - temp_min_c, 1
    ) AS temp_swing_c,

    precipitation_mm,

    CASE
        WHEN precipitation_mm > 5.0
        THEN TRUE
        ELSE FALSE
    END AS is_heavy_rain

FROM {{ source('raw_weather', 'raw_weather_daily') }}
