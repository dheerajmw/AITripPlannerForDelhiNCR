"""Itinerary generate API tests."""

from datetime import date
from unittest.mock import patch

from app.services.weather_client import WeatherForecast


def _mock_matrix(coordinates):
    n = len(coordinates)
    matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            if i == j:
                row.append(0.0)
            else:
                row.append(300.0)  # 5 min
        matrix.append(row)
    return matrix, "osrm", []


@patch(
    "app.services.route_service.build_matrix_chunked",
    side_effect=lambda client, coords, chunk: _mock_matrix(coords),
)
def test_generate_itinerary_success(mock_matrix, api_client, sample_pois) -> None:
    body = {
        "budget": "medium",
        "interests": ["history", "nature"],
        "duration": "8h",
    }
    response = api_client.post("/api/v1/itinerary/generate?mode=rule", json=body)
    assert response.status_code == 200
    data = response.json()
    assert data["meta"]["schema_version"] == "1.0"
    assert data["meta"]["planner_mode"] == "rule"
    assert data["meta"]["budget_tier"] == "medium"
    assert data["meta"]["duration_minutes"] == 480
    assert len(data["stops"]) >= 2
    assert data["summary"]["total_stops"] == len(data["stops"])
    assert data["summary"]["total_cost_inr"]["low"] >= 0
    for stop in data["stops"]:
        assert "arrive_at" in stop
        assert "cost_estimate_inr" in stop


@patch(
    "app.services.route_service.build_matrix_chunked",
    side_effect=lambda client, coords, chunk: _mock_matrix(coords),
)
def test_generate_is_deterministic(mock_matrix, api_client, sample_pois) -> None:
    body = {
        "budget": "medium",
        "interests": ["history", "nature"],
        "duration": "8h",
    }
    r1 = api_client.post("/api/v1/itinerary/generate", json=body)
    r2 = api_client.post("/api/v1/itinerary/generate", json=body)
    assert r1.status_code == 200
    assert r2.status_code == 200
    r1 = r1.json()
    r2 = r2.json()
    ids1 = [s["poi_id"] for s in r1["stops"]]
    ids2 = [s["poi_id"] for s in r2["stops"]]
    assert ids1 == ids2


@patch(
    "app.services.route_service.build_matrix_chunked",
    side_effect=lambda client, coords, chunk: _mock_matrix(coords),
)
@patch("app.services.weather_service.WeatherClient")
def test_generate_with_weather_plan_date(mock_client_cls, mock_matrix, api_client, sample_pois) -> None:
    mock_client = mock_client_cls.return_value
    mock_client.is_configured.return_value = True
    mock_client.fetch_forecast.return_value = WeatherForecast(
        plan_date=date.today().isoformat(),
        condition="Rain",
        description="light rain",
        temp_c=27.0,
        bias="rain",
    )
    body = {
        "budget": "medium",
        "interests": ["history", "nature"],
        "duration": "8h",
        "plan_date": date.today().isoformat(),
    }
    response = api_client.post("/api/v1/itinerary/generate?mode=rule", json=body)
    assert response.status_code == 200
    data = response.json()
    assert data["meta"]["weather"] is not None
    assert data["meta"]["weather"]["bias"] == "rain"
    assert any("Rain expected" in w for w in data["meta"]["warnings"])


def test_invalid_interest_returns_400(api_client, sample_pois) -> None:
    body = {
        "budget": "medium",
        "interests": ["invalid"],
        "duration": "8h",
    }
    response = api_client.post("/api/v1/itinerary/generate", json=body)
    assert response.status_code == 400


@patch(
    "app.services.route_service.build_matrix_chunked",
    side_effect=lambda client, coords, chunk: _mock_matrix(coords),
)
def test_tight_budget_trims_stops(mock_matrix, api_client, sample_pois) -> None:
    body = {
        "budget": "medium",
        "interests": ["history", "nature", "food"],
        "duration": "4h",
    }
    response = api_client.post("/api/v1/itinerary/generate", json=body)
    assert response.status_code == 200
    data = response.json()
    total_visit = sum(s["visit_minutes"] for s in data["stops"])
    total_travel = data["summary"]["total_travel_min"]
    assert total_visit + total_travel <= 240


def test_no_matching_interests_returns_422(db_session) -> None:
    from fastapi.testclient import TestClient

    from app.db.session import get_db
    from app.main import app

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        body = {
            "budget": "medium",
            "interests": ["history"],
            "duration": "8h",
        }
        response = client.post("/api/v1/itinerary/generate", json=body)
        assert response.status_code == 422
        assert response.json()["error"]["code"] == "UNPROCESSABLE_PLAN"
    app.dependency_overrides.clear()
