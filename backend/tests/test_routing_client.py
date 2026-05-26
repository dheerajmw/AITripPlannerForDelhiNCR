"""Routing client tests."""

from app.services.routing_client import RoutingClient, haversine_duration_sec


def test_haversine_duration_positive() -> None:
    sec = haversine_duration_sec(28.6129, 77.2295, 28.5931, 77.2190)
    assert sec > 0


def test_fix_zero_duration_legs() -> None:
    client = RoutingClient()
    coords = [(28.6129, 77.2295), (28.65, 77.23)]
    matrix = [[0.0, 0.0], [0.0, 0.0]]
    fixed, warnings = client._fix_zero_duration_legs(coords, matrix)
    assert fixed[0][1] is not None
    assert fixed[0][1] > 0
    assert warnings
