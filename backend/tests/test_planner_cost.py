"""CostEstimator unit tests."""

from app.db.models import POIRecord
from app.services.planner.cost import CostEstimator


def test_stop_cost_within_tier() -> None:
    poi = POIRecord(
        id="x",
        name="Park",
        category="park",
        lat=28.61,
        lon=77.23,
        estimated_visit_minutes=60,
        source="osm",
    )
    cost = CostEstimator().estimate_stop(poi, "low")
    assert cost.low == 0
    assert cost.high == 0


def test_summary_sums_stop_costs() -> None:
    from app.models.itinerary import CostRangeInr

    costs = [CostRangeInr(low=10, high=20), CostRangeInr(low=5, high=15)]
    summary = CostEstimator().build_summary(
        costs, total_stops=2, total_travel_min=30, total_visit_min=120
    )
    assert summary.total_cost_inr.low == 15
    assert summary.total_cost_inr.high == 35
    assert summary.total_stops == 2
