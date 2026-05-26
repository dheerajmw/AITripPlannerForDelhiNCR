"""Shared pytest fixtures."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.models import Base, POIRecord


@pytest.fixture
def db_session() -> Session:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture
def sample_pois(db_session: Session) -> None:
    records = [
        POIRecord(
            id="osm:node/1",
            name="India Gate",
            category="monument",
            lat=28.6129,
            lon=77.2295,
            estimated_visit_minutes=60,
            source="osm",
        ),
        POIRecord(
            id="osm:node/2",
            name="Lodhi Garden",
            category="park",
            lat=28.5931,
            lon=77.2190,
            estimated_visit_minutes=60,
            source="osm",
        ),
        POIRecord(
            id="osm:node/3",
            name="Karim's",
            category="restaurant",
            lat=28.6507,
            lon=77.2302,
            estimated_visit_minutes=60,
            source="osm",
        ),
    ]
    for r in records:
        r.set_tags_list([r.category, "history" if r.category == "monument" else "food"])
    db_session.add_all(records)
    db_session.commit()


@pytest.fixture
def api_client(db_session: Session, sample_pois: None):
    from fastapi.testclient import TestClient

    from app.db.session import get_db
    from app.main import app

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()
