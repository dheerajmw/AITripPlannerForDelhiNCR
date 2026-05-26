"""Geographic utility tests (Phase 0 gate)."""

from app.utils.geo import (
    clamp_to_ncr,
    in_ncr_bounds,
    is_delhi_area_coordinate,
    is_valid_coordinate,
)


def test_india_gate_inside_ncr() -> None:
    assert in_ncr_bounds(28.6129, 77.2295) is True


def test_jaipur_outside_ncr() -> None:
    assert in_ncr_bounds(26.9124, 75.7873) is False


def test_bbox_edge_inclusive() -> None:
    assert in_ncr_bounds(28.40, 76.84) is True
    assert in_ncr_bounds(28.88, 77.45) is True


def test_clamp_to_ncr() -> None:
    lat, lon = clamp_to_ncr(30.0, 80.0)
    assert in_ncr_bounds(lat, lon) is True
    assert lat == 28.88
    assert lon == 77.45


def test_null_island_invalid_area() -> None:
    assert in_ncr_bounds(0.0, 0.0) is False
    assert is_delhi_area_coordinate(0.0, 0.0) is False


def test_valid_wgs84() -> None:
    assert is_valid_coordinate(28.6, 77.2) is True
    assert is_valid_coordinate(91.0, 77.2) is False
