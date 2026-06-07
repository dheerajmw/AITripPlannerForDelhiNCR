"""SQLite session for anonymous analytics events."""

from functools import lru_cache
from typing import Generator

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.db.analytics_models import AnalyticsBase
from app.settings import get_settings


@lru_cache
def get_analytics_engine() -> Engine:
    settings = get_settings()
    url = settings.resolved_analytics_database_url
    connect_args = {}
    if url.startswith("sqlite"):
        connect_args["check_same_thread"] = False
    engine = create_engine(url, connect_args=connect_args)

    if url.startswith("sqlite"):

        @event.listens_for(engine, "connect")
        def _set_sqlite_pragma(dbapi_conn, _connection_record) -> None:
            cursor = dbapi_conn.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    return engine


@lru_cache
def get_analytics_session_factory() -> sessionmaker:
    return sessionmaker(
        bind=get_analytics_engine(),
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
    )


def init_analytics_db() -> None:
    settings = get_settings()
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    AnalyticsBase.metadata.create_all(bind=get_analytics_engine())


def get_analytics_db() -> Generator[Session, None, None]:
    session = get_analytics_session_factory()()
    try:
        yield session
    finally:
        session.close()
