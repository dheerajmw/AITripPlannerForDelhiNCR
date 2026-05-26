"""POI normalizer unit tests."""

from app.db.models import POIRecord
from app.services.poi_normalizer import (
    classify_category,
    dedupe_pois,
    display_name,
    normalize_element,
)


def test_classify_cafe() -> None:
    category, tags = classify_category({"amenity": "cafe"})
    assert category == "cafe"
    assert "food" in tags


def test_classify_monument_via_tourism() -> None:
    category, tags = classify_category({"tourism": "museum", "name": "National Museum"})
    assert category == "museum"
    assert "history" in tags


def test_display_name_fallback() -> None:
    name = display_name({}, "cafe")
    assert name == "Unnamed cafe"


def test_normalize_node_element() -> None:
    element = {
        "type": "node",
        "id": 12345,
        "lat": 28.6129,
        "lon": 77.2295,
        "tags": {"amenity": "restaurant", "name": "Test Restaurant"},
    }
    record = normalize_element(element)
    assert record is not None
    assert record.id == "osm:node/12345"
    assert record.category == "restaurant"
    assert record.name == "Test Restaurant"


def test_normalize_rejects_outside_ncr() -> None:
    element = {
        "type": "node",
        "id": 99,
        "lat": 26.9,
        "lon": 75.7,
        "tags": {"amenity": "cafe", "name": "Jaipur Cafe"},
    }
    assert normalize_element(element) is None


def test_dedupe_similar_nearby() -> None:
    a = POIRecord(
        id="osm:node/1",
        name="India Gate",
        category="monument",
        lat=28.6129,
        lon=77.2295,
        estimated_visit_minutes=60,
        source="osm",
    )
    b = POIRecord(
        id="osm:node/2",
        name="India Gate",
        category="monument",
        lat=28.6130,
        lon=77.2296,
        estimated_visit_minutes=60,
        source="osm",
    )
    a.set_tags_list(["history"])
    b.set_tags_list(["history"])
    result = dedupe_pois([a, b])
    assert len(result) == 1
