"""Analytics snapshot file tests."""

from datetime import datetime, timezone

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.analytics_models import AnalyticsBase, AnalyticsEventRecord
from app.services.analytics_snapshot import analytics_snapshot_path, refresh_analytics_snapshot


@pytest.fixture
def analytics_db(tmp_path, monkeypatch):
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    AnalyticsBase.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

    monkeypatch.setattr(
        "app.services.analytics_snapshot.get_analytics_session_factory",
        lambda: SessionLocal,
    )
    monkeypatch.setattr(
        "app.services.analytics_snapshot.get_settings",
        lambda: type("S", (), {"data_dir": tmp_path})(),
    )

    session = SessionLocal()
    session.add(
        AnalyticsEventRecord(
            session_id="user-a",
            event="page_view",
            page="explore",
            created_at=datetime.now(timezone.utc),
        )
    )
    session.commit()
    session.close()
    return tmp_path


def test_writes_summary_json(analytics_db) -> None:
    path = refresh_analytics_snapshot(force=True)
    assert path == analytics_db / "analytics_summary.json"
    text = path.read_text(encoding="utf-8")
    assert "unique_sessions" in text
    assert "today" in text
    assert path == analytics_snapshot_path()
