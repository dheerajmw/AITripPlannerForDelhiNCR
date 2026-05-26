"""PreferenceFilter unit tests."""

from app.db.models import POIRecord
from app.services.planner.filter import PreferenceFilter


def _poi(pid: str, category: str) -> POIRecord:
    return POIRecord(
        id=pid,
        name=pid,
        category=category,
        lat=28.61,
        lon=77.23,
        estimated_visit_minutes=60,
        source="osm",
    )


def test_low_budget_excludes_restaurants() -> None:
    candidates = [
        _poi("a", "cafe"),
        _poi("b", "restaurant"),
        _poi("c", "park"),
    ]
    result = PreferenceFilter().apply(
        candidates, interests=["food"], budget="low"
    )
    categories = {p.category for p in result}
    assert "restaurant" not in categories
    assert "cafe" in categories


def test_interest_filter_limits_categories() -> None:
    candidates = [
        _poi("a", "park"),
        _poi("b", "bar"),
    ]
    result = PreferenceFilter().apply(
        candidates, interests=["nature"], budget="high"
    )
    assert len(result) == 1
    assert result[0].category == "park"
