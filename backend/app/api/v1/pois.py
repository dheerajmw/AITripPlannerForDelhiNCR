"""POI query API."""

from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.config import POI_LIST_DEFAULT_LIMIT, SUPPORTED_INTERESTS, SUPPORTED_POI_CATEGORIES
from app.db.session import get_db
from app.exceptions import ValidationAppError
from app.models.poi import POIListResponse
from app.services.poi_service import POIService

router = APIRouter(tags=["pois"])


@router.get("/pois", response_model=POIListResponse)
async def list_pois(
    category: Optional[str] = Query(None, description="Filter by POI category"),
    interest: Optional[str] = Query(
        None, description="Filter by user interest (food, history, nature, nightlife)"
    ),
    min_lat: Optional[float] = Query(None),
    max_lat: Optional[float] = Query(None),
    min_lon: Optional[float] = Query(None),
    max_lon: Optional[float] = Query(None),
    limit: int = Query(POI_LIST_DEFAULT_LIMIT, ge=1, le=200),
    db: Session = Depends(get_db),
) -> POIListResponse:
    if category and category not in SUPPORTED_POI_CATEGORIES:
        raise ValidationAppError(
            f"Unknown category '{category}'",
            details={"allowed": list(SUPPORTED_POI_CATEGORIES)},
        )
    if interest and interest not in SUPPORTED_INTERESTS:
        raise ValidationAppError(
            f"Unknown interest '{interest}'",
            details={"allowed": list(SUPPORTED_INTERESTS)},
        )
    if category and interest:
        raise ValidationAppError("Provide either category or interest, not both")

    service = POIService(db)
    return service.list_pois(
        category=category,
        interest=interest,
        min_lat=min_lat,
        max_lat=max_lat,
        min_lon=min_lon,
        max_lon=max_lon,
        limit=limit,
    )
