"""OpenWeatherMap forecast client with in-memory cache (EC-W-07)."""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Dict, List, Optional, Tuple

import httpx

from app.config import (
    WEATHER_FORECAST_MAX_DAYS,
    WEATHER_HEAT_THRESHOLD_C,
    WEATHER_RAIN_CONDITIONS,
)
from app.settings import get_settings

logger = logging.getLogger(__name__)

_CACHE: Dict[str, Tuple[float, "WeatherForecast"]] = {}


@dataclass(frozen=True)
class WeatherForecast:
    plan_date: str
    condition: str
    description: str
    temp_c: float
    bias: str  # rain | heat | clear


class WeatherClientError(Exception):
    pass


class WeatherClient:
    def __init__(self) -> None:
        settings = get_settings()
        self._api_key = settings.openweather_api_key
        self._base_url = settings.openweather_base_url.rstrip("/")
        self._timeout = 12.0

    def is_configured(self) -> bool:
        return bool(self._api_key and self._api_key.strip())

    def fetch_forecast(self, *, lat: float, lon: float, plan_date: str) -> Optional[WeatherForecast]:
        if not self.is_configured():
            return None

        try:
            target = date.fromisoformat(plan_date)
        except ValueError:
            return None

        today = date.today()
        if target < today or target > today + timedelta(days=WEATHER_FORECAST_MAX_DAYS):
            return None

        cache_key = f"{lat:.3f},{lon:.3f},{plan_date}"
        from app.config import WEATHER_CACHE_TTL_SEC

        cached = _CACHE.get(cache_key)
        if cached and time.time() - cached[0] < WEATHER_CACHE_TTL_SEC:
            return cached[1]

        try:
            forecast = self._request_forecast(lat=lat, lon=lon, target=target)
        except WeatherClientError as exc:
            logger.warning("OpenWeatherMap request failed: %s", exc)
            return None

        _CACHE[cache_key] = (time.time(), forecast)
        return forecast

    def _request_forecast(self, *, lat: float, lon: float, target: date) -> WeatherForecast:
        url = f"{self._base_url}/forecast"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self._api_key,
            "units": "metric",
        }
        with httpx.Client(timeout=self._timeout) as client:
            response = client.get(url, params=params)
            if response.status_code != 200:
                raise WeatherClientError(f"HTTP {response.status_code}")
            payload = response.json()

        entries = payload.get("list") or []
        day_entries = _entries_for_date(entries, target)
        if not day_entries:
            raise WeatherClientError("No forecast entries for plan date")

        condition, description, temp_c, bias = _summarize_day(day_entries)
        return WeatherForecast(
            plan_date=target.isoformat(),
            condition=condition,
            description=description,
            temp_c=temp_c,
            bias=bias,
        )


def _entries_for_date(entries: List[dict], target: date) -> List[dict]:
    matched: List[dict] = []
    for entry in entries:
        dt_txt = entry.get("dt_txt")
        if not dt_txt:
            continue
        try:
            entry_dt = datetime.strptime(dt_txt, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            continue
        if entry_dt.date() == target:
            matched.append(entry)
    return matched


def _summarize_day(entries: List[dict]) -> Tuple[str, str, float, str]:
    conditions: List[str] = []
    descriptions: List[str] = []
    temps: List[float] = []

    for entry in entries:
        weather = (entry.get("weather") or [{}])[0]
        main = entry.get("main") or {}
        conditions.append(str(weather.get("main", "Clear")))
        descriptions.append(str(weather.get("description", "clear sky")))
        temp = main.get("temp")
        if isinstance(temp, (int, float)):
            temps.append(float(temp))

    rain_like = any(c in WEATHER_RAIN_CONDITIONS for c in conditions)
    max_temp = max(temps) if temps else 28.0
    dominant = _dominant_condition(conditions)
    description = _dominant_description(descriptions)

    if rain_like:
        bias = "rain"
        dominant = next((c for c in conditions if c in WEATHER_RAIN_CONDITIONS), dominant)
    elif max_temp >= WEATHER_HEAT_THRESHOLD_C:
        bias = "heat"
    else:
        bias = "clear"

    return dominant, description, round(max_temp, 1), bias


def _dominant_condition(conditions: List[str]) -> str:
    counts: Dict[str, int] = {}
    for cond in conditions:
        counts[cond] = counts.get(cond, 0) + 1
    return max(counts, key=counts.get)


def _dominant_description(descriptions: List[str]) -> str:
    if not descriptions:
        return "clear sky"
    counts: Dict[str, int] = {}
    for desc in descriptions:
        counts[desc] = counts.get(desc, 0) + 1
    return max(counts, key=counts.get)
