"""Estimate per-stop and trip cost in INR."""

from typing import List, Sequence, Tuple

from app.config import COST_INR_BY_CATEGORY
from app.db.models import POIRecord
from app.models.itinerary import CostRangeInr, ItinerarySummary


class CostEstimator:
    def estimate_stop(self, poi: POIRecord, budget_tier: str) -> CostRangeInr:
        low, high = self._category_cost(poi.category, budget_tier)
        return CostRangeInr(low=low, high=high)

    def build_summary(
        self,
        stops_cost: Sequence[CostRangeInr],
        *,
        total_stops: int,
        total_travel_min: int,
        total_visit_min: int,
    ) -> ItinerarySummary:
        low_sum = sum(c.low for c in stops_cost)
        high_sum = sum(c.high for c in stops_cost)
        return ItinerarySummary(
            total_stops=total_stops,
            total_travel_min=total_travel_min,
            total_visit_min=total_visit_min,
            total_cost_inr=CostRangeInr(low=low_sum, high=high_sum),
        )

    @staticmethod
    def _category_cost(category: str, budget_tier: str) -> Tuple[int, int]:
        tier_map = COST_INR_BY_CATEGORY.get(budget_tier, COST_INR_BY_CATEGORY["medium"])
        return tier_map.get(category, (0, 200))
