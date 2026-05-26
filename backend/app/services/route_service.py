"""Route optimization orchestration."""

from typing import Dict, List, Tuple

from sqlalchemy.orm import Session

from app.config import MAX_ROUTE_POIS, OSRM_TABLE_MAX_COORDS, SUPPORTED_TRANSPORT_MODES
from app.db.models import POIRecord
from app.db.repository import POIRepository
from app.exceptions import ValidationAppError
from app.models.route import RouteLeg, RouteOptimizeRequest, RouteOptimizeResponse
from app.services.order_optimizer import optimize_visit_order
from app.services.route_validator import (
    duration_min_from_matrix,
    total_travel_minutes,
    total_visit_minutes,
    validate_time_budget,
)
from app.services.routing_client import RoutingClient, build_matrix_chunked, haversine_m
from app.utils.geo import in_ncr_bounds, is_delhi_area_coordinate, is_valid_coordinate

START_ID = "start"


class RouteService:
    def __init__(self, session: Session) -> None:
        self._repo = POIRepository(session)
        self._routing = RoutingClient()

    def optimize(self, request: RouteOptimizeRequest) -> RouteOptimizeResponse:
        if request.mode not in SUPPORTED_TRANSPORT_MODES:
            raise ValidationAppError(
                f"Unsupported mode '{request.mode}'",
                details={"allowed": list(SUPPORTED_TRANSPORT_MODES)},
            )

        if len(request.poi_ids) > MAX_ROUTE_POIS:
            raise ValidationAppError(
                f"At most {MAX_ROUTE_POIS} POIs allowed per route optimization",
                details={"max": MAX_ROUTE_POIS},
            )

        if len(set(request.poi_ids)) != len(request.poi_ids):
            raise ValidationAppError("Duplicate poi_ids are not allowed")

        if not is_valid_coordinate(request.start_lat, request.start_lon):
            raise ValidationAppError("Invalid start coordinates")

        if not is_delhi_area_coordinate(request.start_lat, request.start_lon):
            raise ValidationAppError("Start point must be within Delhi NCR area")

        if not in_ncr_bounds(request.start_lat, request.start_lon):
            raise ValidationAppError("Start point must be within Delhi NCR bounds")

        pois, missing = self._repo.get_by_ids(request.poi_ids)
        if missing:
            raise ValidationAppError(
                "Unknown POI ids",
                details={"unknown_poi_ids": missing},
            )

        if len(pois) == 1:
            return self._single_poi_response(pois[0], request)

        coordinates: List[Tuple[float, float]] = [(request.start_lat, request.start_lon)]
        index_to_id: Dict[int, str] = {0: START_ID}
        for idx, poi in enumerate(pois, start=1):
            coordinates.append((poi.lat, poi.lon))
            index_to_id[idx] = poi.id

        matrix, routing_source, warnings = build_matrix_chunked(
            self._routing, coordinates, OSRM_TABLE_MAX_COORDS
        )

        order_indices = optimize_visit_order(matrix, start_index=0, use_two_opt=True)
        ordered_pois = [pois[i - 1] for i in order_indices]
        ordered_ids = [p.id for p in ordered_pois]

        legs: List[RouteLeg] = []
        leg_durations: List[int] = []
        prev_idx = 0
        for next_idx in order_indices:
            dur = duration_min_from_matrix(matrix, prev_idx, next_idx)
            lat1, lon1 = coordinates[prev_idx]
            lat2, lon2 = coordinates[next_idx]
            legs.append(
                RouteLeg.model_validate(
                    {
                        "from": index_to_id[prev_idx],
                        "to": index_to_id[next_idx],
                        "duration_min": dur,
                        "distance_m": int(haversine_m(lat1, lon1, lat2, lon2)),
                    }
                )
            )
            leg_durations.append(dur)
            prev_idx = next_idx

        if request.max_total_minutes is not None:
            validate_time_budget(ordered_pois, leg_durations, request.max_total_minutes)

        return RouteOptimizeResponse(
            ordered_poi_ids=ordered_ids,
            legs=legs,
            warnings=warnings,
            total_travel_minutes=total_travel_minutes(leg_durations),
            total_visit_minutes=total_visit_minutes(ordered_pois),
            routing_source=routing_source,
        )

    def _single_poi_response(
        self, poi: POIRecord, request: RouteOptimizeRequest
    ) -> RouteOptimizeResponse:
        matrix, routing_source, warnings = self._routing.build_duration_matrix(
            [(request.start_lat, request.start_lon), (poi.lat, poi.lon)]
        )
        dur = duration_min_from_matrix(matrix, 0, 1)
        dist_m = int(haversine_m(request.start_lat, request.start_lon, poi.lat, poi.lon))
        legs = [
            RouteLeg.model_validate(
                {
                    "from": START_ID,
                    "to": poi.id,
                    "duration_min": dur,
                    "distance_m": dist_m,
                }
            )
        ]
        if request.max_total_minutes is not None:
            validate_time_budget([poi], [dur], request.max_total_minutes)

        return RouteOptimizeResponse(
            ordered_poi_ids=[poi.id],
            legs=legs,
            warnings=warnings,
            total_travel_minutes=dur,
            total_visit_minutes=poi.estimated_visit_minutes,
            routing_source=routing_source,
        )
