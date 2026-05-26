"""Select a diverse shortlist of POIs for routing."""

from collections import defaultdict
from typing import Dict, List, Sequence

from app.config import MAX_ITINERARY_STOPS
from app.db.models import POIRecord


class CandidateSelector:
    def select(
        self,
        candidates: Sequence[POIRecord],
        *,
        max_stops: int = MAX_ITINERARY_STOPS,
    ) -> List[POIRecord]:
        if not candidates:
            return []

        by_category: Dict[str, List[POIRecord]] = defaultdict(list)
        for poi in sorted(candidates, key=lambda p: (p.category, p.id)):
            by_category[poi.category].append(poi)

        categories = sorted(by_category.keys())
        selected: List[POIRecord] = []
        idx = 0
        while len(selected) < max_stops:
            progressed = False
            for cat in categories:
                pool = by_category[cat]
                if idx < len(pool):
                    selected.append(pool[idx])
                    progressed = True
                    if len(selected) >= max_stops:
                        break
            if not progressed:
                break
            idx += 1

        return selected
