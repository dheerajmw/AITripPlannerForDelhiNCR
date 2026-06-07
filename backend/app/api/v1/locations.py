"""Delhi NCR location search for trip start points."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.config import (
    LOCATION_SEARCH_DEFAULT_LIMIT,
    LOCATION_SEARCH_MAX_LIMIT,
    LOCATION_SEARCH_MIN_QUERY_LEN,
)
from app.db.session import get_db
from app.exceptions import ValidationAppError
from app.models.location import LocationSearchResponse
from app.services.location_service import LocationService

router = APIRouter(tags=["locations"])


@router.get("/locations/search", response_model=LocationSearchResponse)
async def search_locations(
    q: str = Query(..., min_length=1, description="Place name within Delhi NCR"),
    limit: int = Query(LOCATION_SEARCH_DEFAULT_LIMIT, ge=1, le=LOCATION_SEARCH_MAX_LIMIT),
    db: Session = Depends(get_db),
) -> LocationSearchResponse:
    query = q.strip()
    if len(query) < LOCATION_SEARCH_MIN_QUERY_LEN:
        raise ValidationAppError(
            f"Enter at least {LOCATION_SEARCH_MIN_QUERY_LEN} characters to search",
            details={"min_length": LOCATION_SEARCH_MIN_QUERY_LEN},
        )

    items = LocationService(db).search(query, limit=limit)
    return LocationSearchResponse(query=query, items=items)
