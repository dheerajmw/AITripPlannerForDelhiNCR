"""POI API integration tests."""


def test_list_pois_by_category(api_client) -> None:
    response = api_client.get("/api/v1/pois", params={"category": "monument"})
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert len(data["items"]) >= 1
    item = data["items"][0]
    assert item["id"]
    assert item["name"]
    assert item["lat"]
    assert item["lon"]
    assert item["category"] == "monument"


def test_list_pois_by_interest_food(api_client) -> None:
    response = api_client.get("/api/v1/pois", params={"interest": "food"})
    assert response.status_code == 200
    data = response.json()
    assert any(i["category"] in ("restaurant", "cafe") for i in data["items"])


def test_unknown_category_returns_400(api_client) -> None:
    response = api_client.get("/api/v1/pois", params={"category": "invalid"})
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"


def test_health_includes_poi_count(api_client) -> None:
    response = api_client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["poi_count"] == 3
