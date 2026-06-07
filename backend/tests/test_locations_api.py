"""Location search API tests."""


def test_search_landmark(api_client) -> None:
    response = api_client.get("/api/v1/locations/search", params={"q": "India"})
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "India"
    assert len(data["items"]) >= 1
    labels = [item["label"] for item in data["items"]]
    assert "India Gate" in labels
    item = data["items"][0]
    assert item["id"]
    assert item["lat"]
    assert item["lon"]
    assert item["source"] in ("landmark", "poi")


def test_search_poi_name(api_client) -> None:
    response = api_client.get("/api/v1/locations/search", params={"q": "Red"})
    assert response.status_code == 200
    data = response.json()
    assert any(
        "Red" in item["label"] or item["source"] == "poi" for item in data["items"]
    )


def test_search_too_short_returns_400(api_client) -> None:
    response = api_client.get("/api/v1/locations/search", params={"q": "a"})
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"


def test_search_no_match_returns_empty(api_client) -> None:
    response = api_client.get("/api/v1/locations/search", params={"q": "zzzznotaplace"})
    assert response.status_code == 200
    assert response.json()["items"] == []
