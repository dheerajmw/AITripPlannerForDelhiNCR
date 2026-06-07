"""Google Maps eligibility filter tests."""

from app.db.models import POIRecord
from app.services.planner.maps_filter import MapsEligibilityFilter, is_named_maps_poi


def _poi(name: str, pid: str = "osm:node/1") -> POIRecord:
    return POIRecord(
        id=pid,
        name=name,
        category="monument",
        lat=28.6129,
        lon=77.2295,
        estimated_visit_minutes=60,
        source="osm",
    )


def test_is_named_maps_poi_rejects_unnamed() -> None:
    assert not is_named_maps_poi(_poi("Unnamed monument"))
    assert is_named_maps_poi(_poi("India Gate"))


def test_apply_skips_unnamed_places() -> None:
    candidates = [
        _poi("India Gate", "a"),
        _poi("Unnamed cafe", "b"),
        _poi("Red Fort", "c"),
    ]
    result, warnings = MapsEligibilityFilter().apply(candidates)
    assert len(result) == 2
    assert any("Skipped" in w for w in warnings)


class _StubPlaces:
    def is_configured(self) -> bool:
        return True

    def verify_poi(self, poi: POIRecord) -> bool:
        return poi.name == "India Gate"


class _RejectAllPlaces:
    def is_configured(self) -> bool:
        return True

    last_error = "ZERO_RESULTS"

    def verify_poi(self, poi: POIRecord) -> bool:
        return False


def test_ensure_shortlist_falls_back_to_named_when_api_rejects_all() -> None:
    pool = [
        _poi("India Gate", "a"),
        _poi("Red Fort", "b"),
    ]
    chosen, warnings = MapsEligibilityFilter(places_client=_RejectAllPlaces()).ensure_shortlist(
        pool, pool, max_stops=2
    )
    assert len(chosen) == 2
    assert any("named landmarks" in w for w in warnings)


def test_ensure_shortlist_replaces_unverified_from_pool() -> None:
    pool = [
        _poi("India Gate", "a"),
        _poi("Red Fort", "b"),
        _poi("Qutub Minar", "c"),
    ]
    shortlist = [_poi("Red Fort", "b")]
    chosen, _ = MapsEligibilityFilter(places_client=_StubPlaces()).ensure_shortlist(
        shortlist, pool, max_stops=2
    )
    assert chosen[0].name == "Red Fort"
    assert any(p.name == "India Gate" for p in chosen)
