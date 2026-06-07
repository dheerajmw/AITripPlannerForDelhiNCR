"""Analytics API tests."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.analytics_models import AnalyticsBase
from app.db.analytics_session import get_analytics_db
from app.settings import get_settings


@pytest.fixture
def analytics_client(db_session, sample_pois):
    from fastapi.testclient import TestClient

    from app.db.session import get_db
    from app.main import app

    analytics_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    AnalyticsBase.metadata.create_all(analytics_engine)
    AnalyticsSession = sessionmaker(bind=analytics_engine, autocommit=False, autoflush=False)

    def override_get_db():
        yield db_session

    def override_get_analytics_db():
        session = AnalyticsSession()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_analytics_db] = override_get_analytics_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


def test_record_page_view(analytics_client, monkeypatch) -> None:
    monkeypatch.setattr(
        "app.services.analytics_snapshot.refresh_analytics_snapshot",
        lambda **_: None,
    )
    response = analytics_client.post(
        "/api/v1/analytics/events",
        json={"event": "page_view", "session_id": "sess-1", "page": "explore"},
    )
    assert response.status_code == 202
    assert response.json()["ok"] is True


def test_record_itinerary_generated(analytics_client) -> None:
    response = analytics_client.post(
        "/api/v1/analytics/events",
        json={
            "event": "itinerary_generated",
            "session_id": "sess-1",
            "properties": {"mode": "rule"},
        },
    )
    assert response.status_code == 202


def test_page_view_requires_page(analytics_client) -> None:
    response = analytics_client.post(
        "/api/v1/analytics/events",
        json={"event": "page_view", "session_id": "sess-1"},
    )
    assert response.status_code == 400


def test_summary_requires_key(analytics_client, monkeypatch) -> None:
    monkeypatch.setenv("ANALYTICS_READ_KEY", "test-secret")
    get_settings.cache_clear()

    response = analytics_client.get("/api/v1/analytics/summary")
    assert response.status_code == 401

    response = analytics_client.get(
        "/api/v1/analytics/summary",
        headers={"X-Analytics-Key": "test-secret"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "daily" in data
    assert data["totals"]["page_views"] >= 0

    get_settings.cache_clear()
