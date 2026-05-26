"""Health check endpoint."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config import APP_VERSION, DEFAULT_CITY
from app.db.session import get_db
from app.models.health import HealthResponse
from app.services.poi_service import POIService

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check(db: Session = Depends(get_db)) -> HealthResponse:
    """Liveness probe; includes POI count when database is populated."""
    poi_count = POIService(db).count()
    return HealthResponse(
        status="ok",
        version=APP_VERSION,
        city=DEFAULT_CITY,
        poi_count=poi_count,
    )
