"""POI persistence and queries."""

from typing import List, Optional, Sequence, Set, Tuple

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.config import INTEREST_TO_CATEGORIES, NCR_BOUNDS, POI_LIST_MAX_LIMIT
from app.db.models import POIRecord
from app.models.poi import POIResponse
from app.utils.geo import in_ncr_bounds


class POIRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def count(self) -> int:
        return int(self._session.scalar(select(func.count()).select_from(POIRecord)) or 0)

    def count_by_category(self) -> List[Tuple[str, int]]:
        rows = self._session.execute(
            select(POIRecord.category, func.count())
            .group_by(POIRecord.category)
            .order_by(POIRecord.category)
        ).all()
        return [(str(cat), int(cnt)) for cat, cnt in rows]

    def find_by_interests(
        self, interests: Sequence[str], *, limit: int = 500
    ) -> List[POIRecord]:
        """Return POIs matching any interest category, ordered by id for determinism."""
        categories: Set[str] = set()
        for interest in interests:
            if interest in INTEREST_TO_CATEGORIES:
                categories.update(INTEREST_TO_CATEGORIES[interest])  # type: ignore[index]
        if not categories:
            return []

        stmt = (
            select(POIRecord)
            .where(POIRecord.category.in_(list(categories)))
            .order_by(POIRecord.id)
            .limit(min(max(1, limit), POI_LIST_MAX_LIMIT))
        )
        rows = self._session.execute(stmt).scalars().all()
        return [r for r in rows if in_ncr_bounds(r.lat, r.lon)]

    def get_by_ids(self, poi_ids: Sequence[str]) -> Tuple[List[POIRecord], List[str]]:
        """Return POIs in request order; missing lists unknown ids."""
        if not poi_ids:
            return [], []
        unique_ids = list(dict.fromkeys(poi_ids))
        rows = (
            self._session.execute(select(POIRecord).where(POIRecord.id.in_(unique_ids)))
            .scalars()
            .all()
        )
        by_id = {r.id: r for r in rows}
        ordered: List[POIRecord] = []
        missing: List[str] = []
        for pid in poi_ids:
            if pid in by_id:
                ordered.append(by_id[pid])
            else:
                missing.append(pid)
        return ordered, missing

    def upsert_many(self, records: Sequence[POIRecord]) -> int:
        """Insert or replace POIs by primary key."""
        for record in records:
            self._session.merge(record)
        self._session.commit()
        return len(records)

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
    ) -> Tuple[List[POIResponse], int]:
        limit = min(max(1, limit), POI_LIST_MAX_LIMIT)

        categories: Optional[List[str]] = None
        if category:
            categories = [category]
        elif interest:
            if interest not in INTEREST_TO_CATEGORIES:
                return [], 0
            categories = list(INTEREST_TO_CATEGORIES[interest])  # type: ignore[index]

        b_min_lat = max(min_lat, NCR_BOUNDS["min_lat"]) if min_lat is not None else NCR_BOUNDS["min_lat"]
        b_max_lat = min(max_lat, NCR_BOUNDS["max_lat"]) if max_lat is not None else NCR_BOUNDS["max_lat"]
        b_min_lon = max(min_lon, NCR_BOUNDS["min_lon"]) if min_lon is not None else NCR_BOUNDS["min_lon"]
        b_max_lon = min(max_lon, NCR_BOUNDS["max_lon"]) if max_lon is not None else NCR_BOUNDS["max_lon"]

        filters = [
            POIRecord.lat >= b_min_lat,
            POIRecord.lat <= b_max_lat,
            POIRecord.lon >= b_min_lon,
            POIRecord.lon <= b_max_lon,
        ]
        if categories:
            filters.append(POIRecord.category.in_(categories))

        count_stmt = select(func.count()).select_from(POIRecord).where(*filters)
        total = int(self._session.scalar(count_stmt) or 0)

        query = select(POIRecord).where(*filters).order_by(POIRecord.name).limit(limit)
        rows = self._session.execute(query).scalars().all()

        items = [_record_to_response(r) for r in rows if in_ncr_bounds(r.lat, r.lon)]
        return items, total


def _record_to_response(record: POIRecord) -> POIResponse:
    return POIResponse(
        id=record.id,
        name=record.name,
        category=record.category,
        tags=record.get_tags_list(),
        lat=record.lat,
        lon=record.lon,
        opening_hours=record.opening_hours,
        estimated_visit_minutes=record.estimated_visit_minutes,
        source=record.source,
    )
