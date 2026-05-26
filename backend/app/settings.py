"""Environment-backed settings (secrets stay in backend/.env only)."""

from functools import lru_cache
from pathlib import Path
from typing import List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# backend/app/settings.py -> parents[1] = backend/, parents[2] = repo root
_BACKEND_DIR = Path(__file__).resolve().parents[1]
_REPO_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(_BACKEND_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "AI Trip Planner API"
    debug: bool = False

    database_url: str = Field(
        default="",
        description="SQLAlchemy URL; empty uses sqlite:///<repo>/data/pois.db",
    )

    overpass_api_url: str = Field(
        default="https://overpass-api.de/api/interpreter",
        description="Overpass API endpoint for POI ingest",
    )
    overpass_timeout_sec: int = 90
    overpass_max_retries: int = 5

    cors_origins: str = Field(
        default="http://localhost:3000",
        description="Comma-separated allowed frontend origins",
    )

    # Groq (Phase 4) — placeholders for Phase 0
    groq_api_key: Optional[str] = None
    groq_model: str = "llama-3.3-70b-versatile"
    groq_base_url: str = "https://api.groq.com/openai/v1"
    groq_timeout_sec: int = 25

    osrm_base_url: str = Field(
        default="https://router.project-osrm.org",
        description="OSRM API base (Phase 2)",
    )

    @property
    def data_dir(self) -> Path:
        return _REPO_ROOT / "data"

    @property
    def resolved_database_url(self) -> str:
        if self.database_url:
            return self.database_url
        db_path = self.data_dir / "pois.db"
        return f"sqlite:///{db_path}"

    @property
    def cors_origin_list(self) -> List[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
