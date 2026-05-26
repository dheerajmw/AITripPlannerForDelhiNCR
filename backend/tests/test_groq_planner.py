"""Groq AI planner tests (mocked — no live API)."""

from unittest.mock import MagicMock, patch

import pytest

from app.services.ai.ai_planner import AIPlannerService
from app.services.ai.groq_client import GroqTimeoutError
from app.services.ai.itinerary_validator import ItineraryValidationError
from app.services.ai.itinerary_validator import ItineraryValidator


def _mock_matrix(coordinates):
    n = len(coordinates)
    matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            if i == j:
                row.append(0.0)
            else:
                row.append(300.0)
        matrix.append(row)
    return matrix, "osrm", []


def _valid_groq_notes(poi_ids):
    return {
        "stops": [{"poi_id": pid, "notes": f"Tip for {pid}"} for pid in poi_ids]
    }


@patch(
    "app.services.route_service.build_matrix_chunked",
    side_effect=lambda client, coords, chunk: _mock_matrix(coords),
)
@patch("app.services.ai.ai_planner.get_settings")
def test_ai_mode_enriches_notes(
    mock_settings, mock_matrix, api_client, sample_pois
) -> None:
    settings = MagicMock()
    settings.groq_api_key = "test-key"
    settings.groq_model = "llama-3.3-70b-versatile"
    settings.groq_timeout_sec = 25
    mock_settings.return_value = settings

    body = {
        "budget": "medium",
        "interests": ["history", "nature"],
        "duration": "8h",
    }
    rule = api_client.post("/api/v1/itinerary/generate?mode=rule", json=body).json()
    rule_ids = [s["poi_id"] for s in rule["stops"]]

    mock_result = MagicMock()
    mock_result.data = _valid_groq_notes(rule_ids)
    mock_result.prompt_tokens = 100
    mock_result.completion_tokens = 50
    mock_result.total_tokens = 150

    with patch("app.services.ai.ai_planner.GroqClient") as mock_client_cls:
        mock_client_cls.return_value.complete_json.return_value = mock_result
        response = api_client.post("/api/v1/itinerary/generate?mode=ai", json=body)

    assert response.status_code == 200
    data = response.json()
    assert data["meta"]["planner_mode"] == "ai"
    assert data["meta"]["ai_status"] == "success"
    assert [s["poi_id"] for s in data["stops"]] == rule_ids
    assert all(s["notes"] for s in data["stops"])


@patch(
    "app.services.route_service.build_matrix_chunked",
    side_effect=lambda client, coords, chunk: _mock_matrix(coords),
)
@patch("app.services.ai.ai_planner.get_settings")
def test_ai_fallback_without_api_key(
    mock_settings, mock_matrix, api_client, sample_pois
) -> None:
    settings = MagicMock()
    settings.groq_api_key = None
    mock_settings.return_value = settings

    body = {
        "budget": "medium",
        "interests": ["history", "nature"],
        "duration": "8h",
    }
    response = api_client.post("/api/v1/itinerary/generate?mode=ai", json=body)
    assert response.status_code == 200
    data = response.json()
    assert data["meta"]["ai_status"] == "fallback"
    assert data["meta"]["fallback_reason"] == "no_api_key"


@patch(
    "app.services.route_service.build_matrix_chunked",
    side_effect=lambda client, coords, chunk: _mock_matrix(coords),
)
@patch("app.services.ai.ai_planner.get_settings")
def test_invalid_poi_id_in_groq_response_triggers_fallback(
    mock_settings, mock_matrix, api_client, sample_pois
) -> None:
    settings = MagicMock()
    settings.groq_api_key = "test-key"
    settings.groq_model = "llama-3.3-70b-versatile"
    settings.groq_timeout_sec = 25
    mock_settings.return_value = settings

    body = {
        "budget": "medium",
        "interests": ["history", "nature"],
        "duration": "8h",
    }

    mock_result = MagicMock()
    mock_result.data = {
        "stops": [{"poi_id": "osm:node/fake", "notes": "Hallucinated place"}]
    }

    with patch("app.services.ai.ai_planner.GroqClient") as mock_client_cls:
        mock_client_cls.return_value.complete_json.return_value = mock_result
        response = api_client.post("/api/v1/itinerary/generate?mode=ai", json=body)

    assert response.status_code == 200
    data = response.json()
    assert data["meta"]["ai_status"] == "fallback"
    assert data["meta"]["fallback_reason"] == "validation"


@patch(
    "app.services.route_service.build_matrix_chunked",
    side_effect=lambda client, coords, chunk: _mock_matrix(coords),
)
@patch("app.services.ai.ai_planner.get_settings")
def test_groq_timeout_triggers_fallback(
    mock_settings, mock_matrix, api_client, sample_pois
) -> None:
    settings = MagicMock()
    settings.groq_api_key = "test-key"
    settings.groq_model = "llama-3.3-70b-versatile"
    settings.groq_timeout_sec = 25
    mock_settings.return_value = settings

    body = {
        "budget": "medium",
        "interests": ["history", "nature"],
        "duration": "8h",
    }

    with patch("app.services.ai.ai_planner.GroqClient") as mock_client_cls:
        mock_client_cls.return_value.complete_json.side_effect = GroqTimeoutError("timed out")
        response = api_client.post("/api/v1/itinerary/generate?mode=ai", json=body)

    assert response.status_code == 200
    data = response.json()
    assert data["meta"]["ai_status"] == "fallback"
    assert data["meta"]["fallback_reason"] == "timeout"


def test_validator_rejects_unknown_poi_id() -> None:
    with pytest.raises(ItineraryValidationError):
        ItineraryValidator().extract_notes(
            {"stops": [{"poi_id": "bad", "notes": "x"}]},
            allowed_ids={"a", "b"},
            required_ids={"a", "b"},
        )


def test_validator_accepts_valid_notes() -> None:
    notes = ItineraryValidator().extract_notes(
        {"stops": [{"poi_id": "a", "notes": "Hi"}, {"poi_id": "b", "notes": "Bye"}]},
        allowed_ids={"a", "b", "c"},
        required_ids={"a", "b"},
    )
    assert notes["a"] == "Hi"
    assert notes["b"] == "Bye"
