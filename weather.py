# weather.py (using free API)
import requests
import pandas as pd
from datetime import datetime, timedelta
import creds

OPENWEATHER_API_KEY = creds.OPENWEATHER_API_KEY

def fetch_weather_data(lat, lon):
    records = []

    # --- Current weather ---
    current_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
    resp = requests.get(current_url)
    current_data = resp.json()

    if "main" not in current_data:
        print("Error fetching current weather:", current_data)
        return pd.DataFrame()

    records.append({
        "type": "current",
        "forecast_time": datetime.utcfromtimestamp(current_data["dt"]),
        "temp": current_data["main"]["temp"],
        "min_temp": current_data["main"]["temp"],
        "max_temp": current_data["main"]["temp"],
        "humidity": current_data["main"]["humidity"],
        "weather_code": current_data["weather"][0]["id"],
        "weather_main": current_data["weather"][0]["main"],
        "weather_desc": current_data["weather"][0]["description"],
        "cloudiness": current_data["clouds"]["all"],
        "wind_speed": current_data["wind"]["speed"],
        "precip_prob": None,
        "rain_volume": current_data.get("rain", {}).get("1h", 0.0),
        "snow_volume": current_data.get("snow", {}).get("1h", 0.0),
        "uvi": 0,  # placeholder, since free API doesn’t provide UV
        "part_of_day": "d" if current_data["weather"][0]["icon"].endswith("d") else "n"
    })

    # --- Forecast (5-day, 3-hour intervals) ---
    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
    resp = requests.get(forecast_url)
    forecast_data = resp.json()

    if "list" not in forecast_data:
        print("Error fetching forecast:", forecast_data)
        return pd.DataFrame(records)

    cutoff_time = datetime.utcnow() + timedelta(hours=48)  # next 48h only
    for entry in forecast_data["list"]:
        ts = datetime.utcfromtimestamp(entry["dt"])
        if ts > cutoff_time:
            break
        records.append({
            "type": "forecast",
            "forecast_time": ts,
            "temp": entry["main"]["temp"],
            "min_temp": entry["main"]["temp_min"],
            "max_temp": entry["main"]["temp_max"],
            "humidity": entry["main"]["humidity"],
            "weather_code": entry["weather"][0]["id"],
            "weather_main": entry["weather"][0]["main"],
            "weather_desc": entry["weather"][0]["description"],
            "cloudiness": entry["clouds"]["all"],
            "wind_speed": entry["wind"]["speed"],
            "precip_prob": entry.get("pop", 0),
            "rain_volume": entry.get("rain", {}).get("3h", 0.0),
            "snow_volume": entry.get("snow", {}).get("3h", 0.0),
            "uvi": 0,  # placeholder
            "part_of_day": entry["sys"]["pod"]
        })

    df = pd.DataFrame(records)
    return df

def summarize_daily_weather(df):
    """
    Aggregate weather data by day to compute min/max temperature,
    average humidity, cloudiness, wind speed, and total rain/snow.
    """
    if df.empty:
        return df  # return empty DataFrame if no data

    df["date"] = df["forecast_time"].dt.date

    summary = df.groupby("date").agg(
        min_temp=("min_temp", "min"),
        max_temp=("max_temp", "max"),
        avg_humidity=("humidity", "mean"),
        avg_cloudiness=("cloudiness", "mean"),
        avg_wind_speed=("wind_speed", "mean"),
        avg_precip_prob=("precip_prob", "mean"),
        total_rain=("rain_volume", "sum"),
        total_snow=("snow_volume", "sum")
    ).reset_index()

    return summary
