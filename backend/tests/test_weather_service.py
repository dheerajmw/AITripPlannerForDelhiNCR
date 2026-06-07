"""Weather bias and forecast parsing tests."""

from datetime import date

from app.db.models import POIRecord
from app.models.itinerary import ItineraryGenerateRequest
from app.models.weather import WeatherSummary
from app.services.weather_client import WeatherClient, _summarize_day
from app.services.weather_service import WeatherService


def _poi(poi_id: str, category: str) -> POIRecord:
    return POIRecord(
        id=poi_id,
        name=poi_id,
        category=category,
        lat=28.61,
        lon=77.22,
        estimated_visit_minutes=60,
        source="test",
    )


def test_summarize_day_rain_bias() -> None:
    entries = [
        {
            "dt_txt": "2026-06-10 09:00:00",
            "weather": [{"main": "Rain", "description": "light rain"}],
            "main": {"temp": 28.0},
        },
        {
            "dt_txt": "2026-06-10 12:00:00",
            "weather": [{"main": "Rain", "description": "moderate rain"}],
            "main": {"temp": 27.5},
        },
    ]
    condition, description, temp_c, bias = _summarize_day(entries)
    assert condition == "Rain"
    assert bias == "rain"
    assert temp_c == 28.0
    assert "rain" in description


def test_summarize_day_heat_bias() -> None:
    entries = [
        {
            "dt_txt": "2026-06-10 12:00:00",
            "weather": [{"main": "Clear", "description": "clear sky"}],
            "main": {"temp": 41.2},
        }
    ]
    _, _, _, bias = _summarize_day(entries)
    assert bias == "heat"


def test_rank_candidates_prefers_indoor_in_rain() -> None:
    service = WeatherService()
    weather = WeatherSummary(
        plan_date="2026-06-10",
        condition="Rain",
        description="light rain",
        temp_c=28.0,
        bias="rain",
        applied=True,
    )
    ranked = service.rank_candidates(
        [_poi("park", "park"), _poi("museum", "museum"), _poi("cafe", "cafe")],
        weather,
    )
    assert ranked[0].category in {"museum", "cafe"}
    assert ranked[-1].category == "park"


def test_resolve_skips_without_plan_date() -> None:
    service = WeatherService(client=WeatherClient())
    request = ItineraryGenerateRequest(
        budget="medium",
        interests=["history"],
        duration="8h",
    )
    summary, warnings = service.resolve(request, lat=28.61, lon=77.22)
    assert summary is None
    assert warnings == []


def test_resolve_warns_when_api_key_missing() -> None:
    service = WeatherService(client=WeatherClient())
    request = ItineraryGenerateRequest(
        budget="medium",
        interests=["history"],
        duration="8h",
        plan_date=date.today().isoformat(),
    )
    summary, warnings = service.resolve(request, lat=28.61, lon=77.22)
    assert summary is None
    assert any("API key" in w for w in warnings)


def test_outdoor_visit_minutes_shortened_in_heat() -> None:
    weather = WeatherSummary(
        plan_date="2026-06-10",
        condition="Clear",
        description="clear sky",
        temp_c=42.0,
        bias="heat",
        applied=True,
    )
    assert WeatherService.outdoor_visit_minutes(60, weather) == 45
    assert WeatherService.outdoor_visit_minutes(20, weather) == 20
