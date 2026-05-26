"""Route feasibility validation."""

from typing import List, Optional, Sequence

from app.db.models import POIRecord
from app.exceptions import AppError


def total_visit_minutes(pois: Sequence[POIRecord]) -> int:
    return sum(p.estimated_visit_minutes for p in pois)


def total_travel_minutes(legs_duration: Sequence[int]) -> int:
    return sum(legs_duration)


def validate_time_budget(
    pois: Sequence[POIRecord],
    legs_duration_min: Sequence[int],
    max_total_minutes: int,
) -> None:
    travel = total_travel_minutes(legs_duration_min)
    visits = total_visit_minutes(pois)
    total = travel + visits
    if total > max_total_minutes:
        raise AppError(
            code="UNPROCESSABLE_PLAN",
            message=(
                f"Route exceeds time budget: {total} min needed "
                f"({visits} min visits + {travel} min travel) "
                f"but max is {max_total_minutes} min."
            ),
            status_code=422,
            details={
                "total_minutes": total,
                "visit_minutes": visits,
                "travel_minutes": travel,
                "max_total_minutes": max_total_minutes,
            },
        )


def duration_min_from_matrix(
    matrix: Sequence[Sequence[Optional[float]]], i: int, j: int
) -> int:
    val = matrix[i][j]
    if val is None:
        return 9999
    return max(0, int(round(val / 60.0)))
