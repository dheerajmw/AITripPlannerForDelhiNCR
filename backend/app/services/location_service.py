"""Search Delhi NCR start locations (landmarks + POI names)."""

from typing import List

from sqlalchemy.orm import Session

from app.config import NCR_START_LOCATIONS
from app.db.repository import POIRepository
from app.models.location import LocationOption


class LocationService:
    def __init__(self, session: Session) -> None:
        self._pois = POIRepository(session)

    def search(self, query: str, *, limit: int = 10) -> List[LocationOption]:
        q = query.strip().lower()
        if len(q) < 2:
            return []

        limit = max(1, min(limit, 20))
        results: List[LocationOption] = []
        seen_labels: set[str] = set()

        for entry in NCR_START_LOCATIONS:
            label = str(entry["label"])
            if q in label.lower():
                key = label.lower()
                if key not in seen_labels:
                    seen_labels.add(key)
                    results.append(
                        LocationOption(
                            id=str(entry["id"]),
                            label=label,
                            lat=float(entry["lat"]),
                            lon=float(entry["lon"]),
                            source="landmark",
                        )
                    )
            if len(results) >= limit:
                return results[:limit]

        for poi in self._pois.search_by_name(q, limit=limit):
            key = poi.name.strip().lower()
            if key in seen_labels:
                continue
            seen_labels.add(key)
            results.append(
                LocationOption(
                    id=poi.id,
                    label=poi.name,
                    lat=poi.lat,
                    lon=poi.lon,
                    source="poi",
                )
            )
            if len(results) >= limit:
                break

        return results[:limit]
