"""Database engine and session factory."""

from functools import lru_cache
from typing import Generator

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.db.models import Base
from app.settings import get_settings


def _sqlite_path(database_url: str) -> str:
    if database_url.startswith("sqlite:///"):
        return database_url.replace("sqlite:///", "", 1)
    return database_url


@lru_cache
def get_engine() -> Engine:
    settings = get_settings()
    url = settings.resolved_database_url
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
def get_session_factory() -> sessionmaker:
    return sessionmaker(bind=get_engine(), autocommit=False, autoflush=False, expire_on_commit=False)


def init_db() -> None:
    """Create tables if they do not exist."""
    settings = get_settings()
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(bind=get_engine())


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency: yield a DB session."""
    session = get_session_factory()()
    try:
        yield session
    finally:
        session.close()
