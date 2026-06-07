"""Resolve weather context and apply POI ranking for itineraries."""

from __future__ import annotations

from datetime import date, timedelta

from app.services.weather_client import planning_today
from typing import List, Optional, Sequence, Tuple

from app.config import (
    INDOOR_POI_CATEGORIES,
    OUTDOOR_POI_CATEGORIES,
    WEATHER_DISCLAIMER,
    WEATHER_FORECAST_MAX_DAYS,
)
from app.db.models import POIRecord
from app.models.itinerary import ItineraryGenerateRequest
from app.models.weather import WeatherSummary
from app.services.weather_client import WeatherClient


class WeatherService:
    def __init__(self, client: Optional[WeatherClient] = None) -> None:
        self._client = client or WeatherClient()

    def resolve(
        self,
        request: ItineraryGenerateRequest,
        *,
        lat: float,
        lon: float,
    ) -> Tuple[Optional[WeatherSummary], List[str]]:
        warnings: List[str] = []
        plan_date = request.plan_date
        if not plan_date:
            return None, warnings

        if not self._client.is_configured():
            warnings.append(
                "Weather-aware planning skipped — add OPENWEATHER_API_KEY to Streamlit secrets "
                "or backend/.env."
            )
            return None, warnings

        try:
            target = date.fromisoformat(plan_date)
        except ValueError:
            warnings.append("Invalid plan date; weather adjustments skipped.")
            return None, warnings

        today = planning_today()
        if target < today:
            warnings.append("Plan date is in the past; weather adjustments skipped.")
            return None, warnings

        if target > today + timedelta(days=WEATHER_FORECAST_MAX_DAYS):
            warnings.append(
                f"Weather forecast unavailable more than {WEATHER_FORECAST_MAX_DAYS} days ahead; "
                "adjustments skipped."
            )
            return None, warnings

        forecast = self._client.fetch_forecast(lat=lat, lon=lon, plan_date=plan_date)
        if forecast is None:
            detail = self._client.last_error or "using standard POI ranking"
            if "invalid OpenWeatherMap API key" in detail:
                warnings.append(
                    "OpenWeatherMap API key is invalid — update OPENWEATHER_API_KEY in "
                    "Streamlit secrets."
                )
            else:
                warnings.append(f"Weather forecast unavailable ({detail}).")
            return None, warnings

        summary = WeatherSummary(
            plan_date=forecast.plan_date,
            condition=forecast.condition,
            description=forecast.description,
            temp_c=forecast.temp_c,
            bias=forecast.bias,  # type: ignore[arg-type]
            applied=forecast.bias in {"rain", "heat"},
        )
        warnings.extend(self._build_warnings(summary))
        return summary, warnings

    def rank_candidates(
        self,
        candidates: Sequence[POIRecord],
        weather: WeatherSummary,
    ) -> List[POIRecord]:
        if not weather.applied:
            return list(candidates)

        scored = [(self._score(poi, weather), poi) for poi in candidates]
        scored.sort(key=lambda item: (-item[0], item[1].category, item[1].id))
        return [poi for _, poi in scored]

    @staticmethod
    def _score(poi: POIRecord, weather: WeatherSummary) -> int:
        if weather.bias == "rain":
            if poi.category in INDOOR_POI_CATEGORIES:
                return 2
            if poi.category in OUTDOOR_POI_CATEGORIES:
                return -2
            return 0
        if weather.bias == "heat":
            if poi.category in INDOOR_POI_CATEGORIES:
                return 1
            if poi.category in OUTDOOR_POI_CATEGORIES:
                return -1
            return 0
        return 0

    def _build_warnings(self, weather: WeatherSummary) -> List[str]:
        warnings: List[str] = []
        if weather.bias == "rain":
            warnings.append(
                f"Rain expected on {weather.plan_date} ({weather.description}). "
                "Indoor stops are prioritized; outdoor parks may be deprioritized."
            )
        elif weather.bias == "heat":
            warnings.append(
                f"High heat forecast (~{weather.temp_c:.0f}°C). "
                "Outdoor visit times are shortened and indoor breaks are favored."
            )
        else:
            warnings.append(
                f"Weather on {weather.plan_date}: {weather.description} (~{weather.temp_c:.0f}°C)."
            )
        warnings.append(WEATHER_DISCLAIMER)
        return warnings

    @staticmethod
    def outdoor_visit_minutes(base_minutes: int, weather: Optional[WeatherSummary]) -> int:
        if not weather or weather.bias != "heat":
            return base_minutes
        from app.config import WEATHER_MIN_OUTDOOR_VISIT_MINUTES, WEATHER_OUTDOOR_VISIT_FACTOR

        reduced = int(round(base_minutes * WEATHER_OUTDOOR_VISIT_FACTOR))
        return max(WEATHER_MIN_OUTDOOR_VISIT_MINUTES, reduced)
