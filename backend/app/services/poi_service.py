"""POI domain service."""

from typing import List, Optional, Tuple

from sqlalchemy.orm import Session

from app.db.repository import POIRepository
from app.models.poi import POIListResponse, POIResponse


class POIService:
    def __init__(self, session: Session) -> None:
        self._repo = POIRepository(session)

    def count(self) -> int:
        return self._repo.count()

    def list_pois(
        self,
        *,
        category: Optional[str] = None,
        interest: Optional[str] = None,
        min_lat: Optional[float] = None,
        max_lat: Optional[float] = None,
        min_lon: Optional[float] = None,
        max_lon: Optional[float] = None,
        limit: int = 50,
    ) -> POIListResponse:
        items, total = self._repo.list_pois(
            category=category,
            interest=interest,
            min_lat=min_lat,
            max_lat=max_lat,
            min_lon=min_lon,
            max_lon=max_lon,
            limit=limit,
        )
        return POIListResponse(items=items, total=total, limit=limit)
