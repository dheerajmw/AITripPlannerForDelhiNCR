"""Health endpoint integration tests."""

from fastapi.testclient import TestClient

from app.db.session import get_db
from app.main import app


def test_health_returns_ok(db_session) -> None:
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(app) as client:
            response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["city"] == "Delhi NCR"
        assert data["poi_count"] == 0
    finally:
        app.dependency_overrides.clear()
