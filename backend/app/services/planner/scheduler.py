"""Build a day schedule with arrival/departure times."""

import re
from datetime import datetime, timedelta
from typing import List, Optional, Sequence, Tuple

from app.config import (
    DEFAULT_SCHEDULE_START_HOUR,
    DEFAULT_SCHEDULE_START_MINUTE,
    NIGHTLIFE_CATEGORIES,
    NIGHTLIFE_EARLIEST_HOUR,
    SCHEDULE_BUFFER_MINUTES,
)
from app.db.models import POIRecord
from app.models.itinerary import ItineraryStop
from app.services.planner.cost import CostEstimator


class ScheduleBuilder:
    def __init__(self) -> None:
        self._cost = CostEstimator()

    def build(
        self,
        ordered_pois: Sequence[POIRecord],
        *,
        leg_travel_minutes: Sequence[int],
        budget_tier: str,
        warnings: Optional[List[str]] = None,
    ) -> Tuple[List[ItineraryStop], List[str]]:
        local_warnings: List[str] = list(warnings or [])
        stops: List[ItineraryStop] = []

        current = datetime(2000, 1, 1, DEFAULT_SCHEDULE_START_HOUR, DEFAULT_SCHEDULE_START_MINUTE)

        for idx, poi in enumerate(ordered_pois):
            if idx > 0:
                current = current + timedelta(minutes=SCHEDULE_BUFFER_MINUTES)
            travel_min = leg_travel_minutes[idx] if idx < len(leg_travel_minutes) else 0
            current = current + timedelta(minutes=travel_min)
            arrive = current
            if poi.category in NIGHTLIFE_CATEGORIES and arrive.hour < NIGHTLIFE_EARLIEST_HOUR:
                arrive = arrive.replace(hour=NIGHTLIFE_EARLIEST_HOUR, minute=0)
                local_warnings.append(
                    f"Adjusted {poi.name} to evening hours (nightlife)."
                )

            closed_msg = _opening_hours_warning(poi.opening_hours, arrive)
            if closed_msg:
                local_warnings.append(closed_msg)

            visit = poi.estimated_visit_minutes
            depart = arrive + timedelta(minutes=visit)
            current = depart

            travel_to_next: Optional[int] = None
            if idx < len(ordered_pois) - 1:
                travel_to_next = leg_travel_minutes[idx + 1] if idx + 1 < len(leg_travel_minutes) else 0

            cost = self._cost.estimate_stop(poi, budget_tier)
            stops.append(
                ItineraryStop(
                    order=idx + 1,
                    poi_id=poi.id,
                    name=poi.name,
                    category=poi.category,
                    lat=poi.lat,
                    lon=poi.lon,
                    arrive_at=_format_time(arrive),
                    depart_at=_format_time(depart),
                    visit_minutes=visit,
                    travel_to_next_minutes=travel_to_next,
                    cost_estimate_inr=cost,
                    notes="",
                )
            )

        return stops, local_warnings


def _format_time(dt: datetime) -> str:
    return dt.strftime("%H:%M")


_TIME_RANGE_RE = re.compile(
    r"(\d{1,2}):(\d{2})\s*-\s*(\d{1,2}):(\d{2})",
    re.IGNORECASE,
)


def _opening_hours_warning(opening_hours: Optional[str], arrive: datetime) -> Optional[str]:
    if not opening_hours:
        return None
    text = opening_hours.strip()
    if not text or text.lower() in ("24/7", "24 hours", "always"):
        return None

    match = _TIME_RANGE_RE.search(text)
    if not match:
        return None

    open_h, open_m, close_h, close_m = (int(match.group(i)) for i in range(1, 5))
    open_minutes = open_h * 60 + open_m
    close_minutes = close_h * 60 + close_m
    arrive_minutes = arrive.hour * 60 + arrive.minute

    if close_minutes > open_minutes:
        if arrive_minutes < open_minutes or arrive_minutes >= close_minutes:
            return f"Scheduled arrival may be outside opening hours ({text})."
    return None
