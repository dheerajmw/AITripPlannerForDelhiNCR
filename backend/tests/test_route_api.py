"""Route API integration tests."""

from unittest.mock import patch


def _mock_matrix(coordinates):
    n = len(coordinates)
    matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            if i == j:
                row.append(0.0)
            else:
                row.append(600.0)  # 10 min
        matrix.append(row)
    return matrix, "osrm", []


@patch("app.services.route_service.build_matrix_chunked", side_effect=lambda client, coords, chunk: _mock_matrix(coords))
def test_optimize_route_returns_order_and_legs(mock_matrix, api_client, sample_pois) -> None:
    poi_ids = ["osm:node/1", "osm:node/2", "osm:node/3"]
    body = {
        "poi_ids": poi_ids,
        "start_lat": 28.6129,
        "start_lon": 77.2295,
        "mode": "walking",
        "max_total_minutes": 480,
    }
    response = api_client.post("/api/v1/route/optimize", json=body)
    assert response.status_code == 200
    data = response.json()
    assert len(data["ordered_poi_ids"]) == 3
    assert set(data["ordered_poi_ids"]) == set(poi_ids)
    assert len(data["legs"]) == 3
    assert data["legs"][0]["from"] == "start"
    assert data["total_travel_minutes"] > 0
    assert data["total_visit_minutes"] > 0


@patch("app.services.route_service.build_matrix_chunked", side_effect=lambda client, coords, chunk: _mock_matrix(coords))
def test_unknown_poi_id_returns_400(mock_matrix, api_client, sample_pois) -> None:
    body = {
        "poi_ids": ["osm:node/1", "osm:does-not-exist"],
        "start_lat": 28.6129,
        "start_lon": 77.2295,
    }
    response = api_client.post("/api/v1/route/optimize", json=body)
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"


@patch("app.services.route_service.build_matrix_chunked", side_effect=lambda client, coords, chunk: _mock_matrix(coords))
def test_exceeds_time_budget_returns_422(mock_matrix, api_client, sample_pois) -> None:
    body = {
        "poi_ids": ["osm:node/1", "osm:node/2", "osm:node/3"],
        "start_lat": 28.6129,
        "start_lon": 77.2295,
        "max_total_minutes": 5,
    }
    response = api_client.post("/api/v1/route/optimize", json=body)
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "UNPROCESSABLE_PLAN"


@patch("app.services.routing_client.RoutingClient._fetch_osrm_table")
def test_osrm_failure_uses_fallback(mock_fetch, api_client, sample_pois) -> None:
    mock_fetch.side_effect = RuntimeError("OSRM down")

    body = {
        "poi_ids": ["osm:node/1", "osm:node/2"],
        "start_lat": 28.6129,
        "start_lon": 77.2295,
    }
    response = api_client.post("/api/v1/route/optimize", json=body)
    assert response.status_code == 200
    data = response.json()
    assert data["routing_source"] == "haversine"
    assert any("OSRM" in w for w in data["warnings"])
