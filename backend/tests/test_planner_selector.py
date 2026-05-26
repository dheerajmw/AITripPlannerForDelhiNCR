"""CandidateSelector unit tests."""

from app.db.models import POIRecord
from app.services.planner.selector import CandidateSelector


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


def test_selector_prefers_category_diversity() -> None:
    candidates = [
        _poi("1", "park"),
        _poi("2", "park"),
        _poi("3", "museum"),
        _poi("4", "museum"),
    ]
    selected = CandidateSelector().select(candidates, max_stops=3)
    categories = [p.category for p in selected]
    assert len(selected) == 3
    assert "park" in categories
    assert "museum" in categories
