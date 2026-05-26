"""ScheduleBuilder unit tests."""

from app.db.models import POIRecord
from app.services.planner.scheduler import ScheduleBuilder


def test_schedule_assigns_times_in_order() -> None:
    pois = [
        POIRecord(
            id="1",
            name="A",
            category="monument",
            lat=28.61,
            lon=77.23,
            estimated_visit_minutes=60,
            source="osm",
        ),
        POIRecord(
            id="2",
            name="B",
            category="park",
            lat=28.62,
            lon=77.24,
            estimated_visit_minutes=30,
            source="osm",
        ),
    ]
    stops, _ = ScheduleBuilder().build(
        pois, leg_travel_minutes=[15, 10], budget_tier="medium"
    )
    assert stops[0].order == 1
    assert stops[0].arrive_at == "09:15"
    assert stops[0].depart_at == "10:15"
    assert stops[1].arrive_at > stops[0].depart_at


def test_nightlife_shifted_to_evening() -> None:
    poi = POIRecord(
        id="bar1",
        name="Bar",
        category="bar",
        lat=28.61,
        lon=77.23,
        estimated_visit_minutes=60,
        source="osm",
    )
    stops, warnings = ScheduleBuilder().build(
        [poi], leg_travel_minutes=[5], budget_tier="high"
    )
    assert stops[0].arrive_at >= "17:00"
    assert any("evening" in w.lower() for w in warnings)
