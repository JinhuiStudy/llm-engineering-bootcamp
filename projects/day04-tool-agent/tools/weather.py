"""Open-Meteo 무료 API로 현재 날씨. API 키 불필요."""

from __future__ import annotations

import httpx


def _geocode(city: str) -> tuple[float, float, str]:
    r = httpx.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": city, "count": 1, "language": "ko"},
        timeout=10,
    )
    r.raise_for_status()
    results = r.json().get("results") or []
    if not results:
        raise ValueError(f"도시 못 찾음: {city}")
    top = results[0]
    return top["latitude"], top["longitude"], top.get("name", city)


def get_weather(city: str) -> dict:
    lat, lon, resolved = _geocode(city)
    r = httpx.get(
        "https://api.open-meteo.com/v1/forecast",
        params={"latitude": lat, "longitude": lon, "current_weather": True},
        timeout=10,
    )
    r.raise_for_status()
    cw = r.json()["current_weather"]
    return {
        "city": resolved,
        "temperature_celsius": cw["temperature"],
        "windspeed": cw["windspeed"],
        "weather_code": cw["weathercode"],
    }
