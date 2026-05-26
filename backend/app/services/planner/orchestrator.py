"""Wire POI fetch → filter → select → route → schedule → cost."""

from typing import List, Sequence

from sqlalchemy.orm import Session

from app.config import (
    DEFAULT_CITY,
    DEFAULT_TRANSPORT_MODE,
    ITINERARY_SCHEMA_VERSION,
    MIN_ITINERARY_STOPS,
)
from app.db.models import POIRecord
from app.db.repository import POIRepository
from app.exceptions import UnprocessablePlanError, ValidationAppError
from app.models.itinerary import (
    ItineraryGenerateRequest,
    ItineraryMeta,
    ItineraryResponse,
    StartPoint,
)
from app.models.route import RouteOptimizeRequest
from app.services.planner.cost import CostEstimator
from app.services.planner.filter import PreferenceFilter
from app.services.planner.scheduler import ScheduleBuilder
from app.services.planner.selector import CandidateSelector
from app.services.route_service import RouteService
from app.utils.geo import in_ncr_bounds, is_delhi_area_coordinate, is_valid_coordinate


class PlannerOrchestrator:
    def __init__(self, session: Session) -> None:
        self._repo = POIRepository(session)
        self._route = RouteService(session)
        self._filter = PreferenceFilter()
        self._selector = CandidateSelector()
        self._scheduler = ScheduleBuilder()
        self._cost = CostEstimator()

    def generate(self, request: ItineraryGenerateRequest) -> ItineraryResponse:
        start = request.resolved_start()
        self._validate_start(start)

        warnings: List[str] = []
        candidates = self._repo.find_by_interests(request.interests, limit=500)
        if not candidates:
            raise UnprocessablePlanError(
                "No POIs match the selected interests in Delhi NCR.",
                details={"interests": list(request.interests)},
            )

        filtered = self._filter.apply(
            candidates, interests=request.interests, budget=request.budget
        )
        if not filtered:
            raise UnprocessablePlanError(
                "No POIs remain after applying budget and interest filters.",
                details={"budget": request.budget, "interests": list(request.interests)},
            )

        shortlist = self._selector.select(filtered)
        ordered_pois, route_warnings, routing_source, leg_minutes = self._fit_route(
            shortlist,
            start=start,
            max_minutes=request.duration_minutes,
        )
        warnings.extend(route_warnings)

        stops, schedule_warnings = self._scheduler.build(
            ordered_pois,
            leg_travel_minutes=leg_minutes,
            budget_tier=request.budget,
            warnings=warnings,
        )
        warnings = schedule_warnings

        stop_costs = [s.cost_estimate_inr for s in stops]
        summary = self._cost.build_summary(
            stop_costs,
            total_stops=len(stops),
            total_travel_min=sum(leg_minutes),
            total_visit_min=sum(s.visit_minutes for s in stops),
        )

        return ItineraryResponse(
            meta=ItineraryMeta(
                city=DEFAULT_CITY,
                duration_minutes=request.duration_minutes,
                budget_tier=request.budget,
                schema_version=ITINERARY_SCHEMA_VERSION,
                start_point=start,
                warnings=warnings,
                planner_mode="rule",
                routing_source=routing_source,
            ),
            stops=stops,
            summary=summary,
        )

    def _fit_route(
        self,
        shortlist: Sequence[POIRecord],
        *,
        start: StartPoint,
        max_minutes: int,
    ) -> tuple[List[POIRecord], List[str], str, List[int]]:
        poi_ids = [p.id for p in shortlist]
        warnings: List[str] = []
        routing_source = "haversine"

        while len(poi_ids) >= MIN_ITINERARY_STOPS:
            route_resp = self._route.optimize(
                RouteOptimizeRequest(
                    poi_ids=poi_ids,
                    start_lat=start.lat,
                    start_lon=start.lon,
                    mode=DEFAULT_TRANSPORT_MODE,
                )
            )
            total = route_resp.total_travel_minutes + route_resp.total_visit_minutes
            if total <= max_minutes:
                ordered, _ = self._repo.get_by_ids(route_resp.ordered_poi_ids)
                leg_minutes = [leg.duration_min for leg in route_resp.legs]
                warnings.extend(route_resp.warnings)
                return ordered, warnings, route_resp.routing_source, leg_minutes

            drop_id = route_resp.ordered_poi_ids[-1]
            poi_ids = [pid for pid in poi_ids if pid != drop_id]

        raise UnprocessablePlanError(
            "Could not build an itinerary that fits the time budget with at least "
            f"{MIN_ITINERARY_STOPS} stops.",
            details={"max_minutes": max_minutes},
        )

    @staticmethod
    def _validate_start(start: StartPoint) -> None:
        if not is_valid_coordinate(start.lat, start.lon):
            raise ValidationAppError("Invalid start coordinates")
        if not is_delhi_area_coordinate(start.lat, start.lon):
            raise ValidationAppError("Start point must be within Delhi NCR area")
        if not in_ncr_bounds(start.lat, start.lon):
            raise ValidationAppError("Start point must be within Delhi NCR bounds")
