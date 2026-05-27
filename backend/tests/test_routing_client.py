"""Routing client tests."""

from unittest.mock import MagicMock, patch

import httpx

from app.services.routing_client import RoutingClient, _http_fallback_url, haversine_duration_sec


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


def test_http_fallback_url() -> None:
    assert _http_fallback_url(
        "https://router.project-osrm.org/table/v1/walking/1,2"
    ).startswith("http://")


@patch("app.services.routing_client.httpx.Client")
def test_get_json_retries_http_after_ssl_failure(mock_client_cls: MagicMock) -> None:
    client = RoutingClient()
    mock_client = mock_client_cls.return_value.__enter__.return_value
    ok_response = MagicMock()
    ok_response.raise_for_status = MagicMock()
    ok_response.json.return_value = {"code": "Ok", "durations": [[0.0, 60.0], [60.0, 0.0]]}

    mock_client.get.side_effect = [
        httpx.ConnectError("SSL handshake failure"),
        ok_response,
    ]

    data = client._get_json(
        "https://router.project-osrm.org/table/v1/walking/77.2,28.6",
        {"annotations": "duration"},
    )
    assert data["code"] == "Ok"
    assert mock_client.get.call_count == 2
    assert mock_client.get.call_args_list[1][0][0].startswith("http://")
