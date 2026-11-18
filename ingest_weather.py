
import os
from pathlib import Path
import requests
import dlt

# GCP credentials file location
BASE_DIR = Path(__file__).resolve().parent
credentials_path = BASE_DIR / "gcp-credentials.json"

if credentials_path.exists() and not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(credentials_path)

@dlt.resource(
    table_name="raw_weather_daily",
    write_disposition="merge",
    primary_key="time"
)
def fetch_weather():

    # Open-Meteo Forecast API
    url = "https://api.open-meteo.com/v1/forecast"

    # Halifax, Nova Scotia coordinates
    params = {
        "latitude": 44.6488,
        "longitude": -63.5752,
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum"
        ],
        "timezone": "America/Halifax",
        "forecast_days": 7
    }

    # Fetch weather data
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()["daily"]

    # Convert JSON into daily records
    for i in range(len(data["time"])):
        yield {
            "time": data["time"][i],
            "temp_max_c": data["temperature_2m_max"][i],
            "temp_min_c": data["temperature_2m_min"][i],
            "precipitation_mm": data["precipitation_sum"][i]
        }


if __name__ == "__main__":

    pipeline = dlt.pipeline(
        pipeline_name="weather_pipeline",
        destination="bigquery",
        dataset_name="raw_weather"
    )

    load_info = pipeline.run(fetch_weather())

    print(load_info)
