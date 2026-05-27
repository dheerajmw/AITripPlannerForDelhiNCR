"""Streamlit runtime setup: import path, secrets → env, POI database."""

from __future__ import annotations

import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = REPO_ROOT / "backend"

# Public GitHub Release asset (see scripts/publish-poi-release.sh to refresh).
DEFAULT_POI_DB_DOWNLOAD_URL = (
    "https://github.com/dheerajmw/AITripPlannerForDelhiNCR/releases/download/v0.1.0-poi/pois.db"
)


def configure_import_path() -> None:
    backend = str(BACKEND_DIR)
    if backend not in sys.path:
        sys.path.insert(0, backend)


def apply_secrets_to_env() -> None:
    """Map Streamlit Cloud secrets into os.environ before Settings loads."""
    try:
        import streamlit as st
    except ImportError:
        return

    if not hasattr(st, "secrets"):
        return

    mapping = {
        "GROQ_API_KEY": "GROQ_API_KEY",
        "GROQ_MODEL": "GROQ_MODEL",
        "GROQ_BASE_URL": "GROQ_BASE_URL",
        "GROQ_TIMEOUT_SEC": "GROQ_TIMEOUT_SEC",
        "OSRM_BASE_URL": "OSRM_BASE_URL",
        "POI_DB_DOWNLOAD_URL": "POI_DB_DOWNLOAD_URL",
        "DATABASE_URL": "DATABASE_URL",
    }
    for secret_key, env_key in mapping.items():
        if secret_key in st.secrets:
            os.environ[env_key] = str(st.secrets[secret_key])


def ensure_poi_database() -> tuple[bool, str]:
    """
    Ensure data/pois.db exists. Download when POI_DB_DOWNLOAD_URL is set.
    Returns (ok, message).
    """
    from app.settings import get_settings

    get_settings.cache_clear()
    settings = get_settings()
    db_path = settings.data_dir / "pois.db"

    if db_path.exists() and db_path.stat().st_size > 10_000:
        return True, f"POI database ready ({db_path.name})"

    download_url = (
        os.environ.get("POI_DB_DOWNLOAD_URL", "").strip() or DEFAULT_POI_DB_DOWNLOAD_URL
    )

    import httpx

    settings.data_dir.mkdir(parents=True, exist_ok=True)
    tmp_path = db_path.with_suffix(".db.download")
    try:
        with httpx.stream("GET", download_url, timeout=120.0, follow_redirects=True) as response:
            response.raise_for_status()
            with tmp_path.open("wb") as f:
                for chunk in response.iter_bytes():
                    f.write(chunk)
        tmp_path.replace(db_path)
    except Exception as exc:
        if tmp_path.exists():
            tmp_path.unlink(missing_ok=True)
        return False, f"Failed to download POI database: {exc}"

    if not db_path.exists() or db_path.stat().st_size < 10_000:
        return False, "Downloaded POI database file is empty or invalid."

    return True, f"Downloaded POI database ({db_path.stat().st_size // 1024} KB)"


def init_backend() -> tuple[bool, str]:
    configure_import_path()
    apply_secrets_to_env()

    from app.settings import get_settings

    get_settings.cache_clear()

    from app.db.session import get_engine, get_session_factory, init_db

    get_engine.cache_clear()
    get_session_factory.cache_clear()

    ok, msg = ensure_poi_database()
    if not ok:
        return False, msg

    init_db()
    return True, msg
