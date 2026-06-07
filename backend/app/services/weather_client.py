"""OpenWeatherMap forecast client with in-memory cache (EC-W-07)."""

from __future__ import annotations

import logging
import os
import time
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from typing import Dict, List, Optional, Tuple
from zoneinfo import ZoneInfo

import httpx

from app.config import (
    WEATHER_FORECAST_MAX_DAYS,
    WEATHER_HEAT_THRESHOLD_C,
    WEATHER_PLANNING_TZ,
    WEATHER_RAIN_CONDITIONS,
)
from app.settings import get_settings

logger = logging.getLogger(__name__)

_PLACEHOLDER_KEYS = frozenset(
    {
        "",
        "your_openweather_key",
        "changeme",
        "replace_me",
        "xxx",
    }
)

_CACHE: Dict[str, Tuple[float, "WeatherForecast"]] = {}
_PLANNING_TZ = ZoneInfo(WEATHER_PLANNING_TZ)


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
        self._timeout = 12.0
        self.last_error: Optional[str] = None

    def _resolve_api_key(self) -> str:
        settings = get_settings()
        key = (settings.openweather_api_key or os.environ.get("OPENWEATHER_API_KEY") or "").strip()
        return key

    def is_configured(self) -> bool:
        key = self._resolve_api_key().lower()
        return bool(key) and key not in _PLACEHOLDER_KEYS

    def fetch_forecast(self, *, lat: float, lon: float, plan_date: str) -> Optional[WeatherForecast]:
        self.last_error = None
        api_key = self._resolve_api_key()
        if not api_key or api_key.lower() in _PLACEHOLDER_KEYS:
            return None

        try:
            target = date.fromisoformat(plan_date)
        except ValueError:
            self.last_error = "invalid plan date"
            return None

        today = planning_today()
        if target < today or target > today + timedelta(days=WEATHER_FORECAST_MAX_DAYS):
            self.last_error = "plan date outside forecast window"
            return None

        cache_key = f"{lat:.3f},{lon:.3f},{plan_date}"
        from app.config import WEATHER_CACHE_TTL_SEC

        cached = _CACHE.get(cache_key)
        if cached and time.time() - cached[0] < WEATHER_CACHE_TTL_SEC:
            return cached[1]

        settings = get_settings()
        base_url = settings.openweather_base_url.rstrip("/")

        try:
            forecast = self._request_forecast(
                base_url=base_url,
                api_key=api_key,
                lat=lat,
                lon=lon,
                target=target,
            )
        except WeatherClientError as exc:
            self.last_error = str(exc)
            logger.warning("OpenWeatherMap forecast failed: %s", exc)
            if target == today:
                try:
                    forecast = self._request_current(
                        base_url=base_url,
                        api_key=api_key,
                        lat=lat,
                        lon=lon,
                        target=target,
                    )
                except WeatherClientError as current_exc:
                    self.last_error = str(current_exc)
                    logger.warning("OpenWeatherMap current weather failed: %s", current_exc)
                    return None
            else:
                return None

        _CACHE[cache_key] = (time.time(), forecast)
        return forecast

    def _request_forecast(
        self,
        *,
        base_url: str,
        api_key: str,
        lat: float,
        lon: float,
        target: date,
    ) -> WeatherForecast:
        url = f"{base_url}/forecast"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": api_key,
            "units": "metric",
        }
        payload = self._get_json(url, params)
        entries = payload.get("list") or []
        day_entries = _entries_for_date(entries, target)
        if not day_entries:
            raise WeatherClientError("no forecast entries for plan date in Delhi NCR")

        condition, description, temp_c, bias = _summarize_day(day_entries)
        return WeatherForecast(
            plan_date=target.isoformat(),
            condition=condition,
            description=description,
            temp_c=temp_c,
            bias=bias,
        )

    def _request_current(
        self,
        *,
        base_url: str,
        api_key: str,
        lat: float,
        lon: float,
        target: date,
    ) -> WeatherForecast:
        url = f"{base_url}/weather"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": api_key,
            "units": "metric",
        }
        payload = self._get_json(url, params)
        weather = (payload.get("weather") or [{}])[0]
        main = payload.get("main") or {}
        condition = str(weather.get("main", "Clear"))
        description = str(weather.get("description", "clear sky"))
        temp_c = float(main.get("temp", 28.0))
        rain_like = condition in WEATHER_RAIN_CONDITIONS
        if rain_like:
            bias = "rain"
        elif temp_c >= WEATHER_HEAT_THRESHOLD_C:
            bias = "heat"
        else:
            bias = "clear"
        return WeatherForecast(
            plan_date=target.isoformat(),
            condition=condition,
            description=description,
            temp_c=round(temp_c, 1),
            bias=bias,
        )

    def _get_json(self, url: str, params: dict) -> dict:
        try:
            with httpx.Client(timeout=self._timeout) as client:
                response = client.get(url, params=params)
        except httpx.HTTPError as exc:
            raise WeatherClientError(f"network error: {exc}") from exc

        if response.status_code == 401:
            raise WeatherClientError("invalid OpenWeatherMap API key")
        if response.status_code != 200:
            raise WeatherClientError(f"HTTP {response.status_code}")
        payload = response.json()
        if not isinstance(payload, dict):
            raise WeatherClientError("unexpected API response")
        return payload


def planning_today() -> date:
    """Calendar today in Delhi NCR — matches how travellers pick trip dates."""
    return datetime.now(_PLANNING_TZ).date()


def _entries_for_date(entries: List[dict], target: date) -> List[dict]:
    matched: List[dict] = []
    for entry in entries:
        local_date = _entry_local_date(entry)
        if local_date == target:
            matched.append(entry)
    return matched


def _entry_local_date(entry: dict) -> Optional[date]:
    dt_unix = entry.get("dt")
    if isinstance(dt_unix, int):
        return datetime.fromtimestamp(dt_unix, tz=timezone.utc).astimezone(_PLANNING_TZ).date()

    dt_txt = entry.get("dt_txt")
    if not dt_txt:
        return None
    try:
        utc_naive = datetime.strptime(dt_txt, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None
    return utc_naive.replace(tzinfo=timezone.utc).astimezone(_PLANNING_TZ).date()


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
