"""Keep only POIs that travellers can open on Google Maps."""

from __future__ import annotations

from typing import List, Optional, Sequence, Tuple

from app.config import MAX_ITINERARY_STOPS, MIN_ITINERARY_STOPS
from app.db.models import POIRecord
from app.services.google_places_client import GooglePlacesClient


def is_named_maps_poi(poi: POIRecord) -> bool:
    """Named OSM places resolve on Google Maps; unnamed nodes typically do not."""
    name = (poi.name or "").strip()
    if len(name) < 3:
        return False
    if name.startswith("Unnamed "):
        return False
    return True


class MapsEligibilityFilter:
    def __init__(self, places_client: Optional[GooglePlacesClient] = None) -> None:
        self._places = places_client or GooglePlacesClient()

    def apply(self, candidates: Sequence[POIRecord]) -> Tuple[List[POIRecord], List[str]]:
        warnings: List[str] = []
        named = [p for p in candidates if is_named_maps_poi(p)]
        unnamed_skipped = len(candidates) - len(named)
        if unnamed_skipped:
            warnings.append(
                f"Skipped {unnamed_skipped} places without a proper name "
                "(not listed on Google Maps)."
            )

        return named, warnings

    def ensure_shortlist(
        self,
        shortlist: Sequence[POIRecord],
        pool: Sequence[POIRecord],
        *,
        max_stops: int = MAX_ITINERARY_STOPS,
    ) -> Tuple[List[POIRecord], List[str]]:
        """Build a shortlist of Google-verified POIs when Places API is configured."""
        warnings: List[str] = []
        if not self._places.is_configured():
            return list(shortlist), warnings

        chosen: List[POIRecord] = []
        seen: set[str] = set()

        for poi in shortlist:
            if poi.id in seen:
                continue
            if self._places.verify_poi(poi):
                chosen.append(poi)
                seen.add(poi.id)

        if len(chosen) >= MIN_ITINERARY_STOPS:
            return chosen[:max_stops], warnings

        for poi in pool:
            if poi.id in seen:
                continue
            if not self._places.verify_poi(poi):
                continue
            chosen.append(poi)
            seen.add(poi.id)
            if len(chosen) >= max_stops:
                break

        if len(chosen) >= MIN_ITINERARY_STOPS:
            if len(chosen) < len(shortlist):
                warnings.append(
                    "Replaced some stops with Google Maps–verified places near your route."
                )
            return chosen[:max_stops], warnings

        # Places API often misses OSM names — fall back to named landmarks (lat/lon still
        # open correctly in Google Maps).
        named_shortlist = [p for p in shortlist if is_named_maps_poi(p)]
        if len(named_shortlist) >= MIN_ITINERARY_STOPS:
            detail = self._places.last_error or "limited Places API matches"
            warnings.append(
                f"Google Places verified only {len(chosen)} stop(s) ({detail}); "
                "using named landmarks that open on Google Maps via coordinates."
            )
            return named_shortlist[:max_stops], warnings

        named_pool: List[POIRecord] = []
        seen_pool: set[str] = set()
        for poi in list(shortlist) + list(pool):
            if poi.id in seen_pool or not is_named_maps_poi(poi):
                continue
            named_pool.append(poi)
            seen_pool.add(poi.id)
            if len(named_pool) >= max_stops:
                break

        if len(named_pool) >= MIN_ITINERARY_STOPS:
            warnings.append(
                "Google Places verification unavailable for most stops; "
                "using named places from the Delhi NCR database."
            )
            return named_pool[:max_stops], warnings

        return chosen, warnings
