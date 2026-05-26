"""Filter POI candidates by budget and interests."""

from typing import List, Sequence

from app.config import BUDGET_ALLOWED_CATEGORIES, INTEREST_TO_CATEGORIES
from app.db.models import POIRecord


class PreferenceFilter:
    def apply(
        self,
        candidates: Sequence[POIRecord],
        *,
        interests: Sequence[str],
        budget: str,
    ) -> List[POIRecord]:
        allowed_categories = set(self._categories_for_interests(interests))
        budget_categories = set(BUDGET_ALLOWED_CATEGORIES.get(budget, ()))

        filtered: List[POIRecord] = []
        for poi in sorted(candidates, key=lambda p: p.id):
            if poi.category not in allowed_categories:
                continue
            if poi.category not in budget_categories:
                continue
            if budget == "low" and poi.category == "restaurant":
                continue
            filtered.append(poi)
        return filtered

    @staticmethod
    def _categories_for_interests(interests: Sequence[str]) -> List[str]:
        cats: List[str] = []
        for interest in interests:
            mapped = INTEREST_TO_CATEGORIES.get(interest)  # type: ignore[arg-type]
            if mapped:
                cats.extend(mapped)
        return list(dict.fromkeys(cats))
