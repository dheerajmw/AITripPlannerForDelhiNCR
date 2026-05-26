"""Route optimization API schemas."""

from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from app.config import DEFAULT_TRANSPORT_MODE


class RouteOptimizeRequest(BaseModel):
    poi_ids: List[str] = Field(..., min_length=1)
    start_lat: float
    start_lon: float
    mode: Literal["walking"] = DEFAULT_TRANSPORT_MODE
    max_total_minutes: Optional[int] = Field(None, ge=1, le=1440)


class RouteLeg(BaseModel):
    from_id: str = Field(..., alias="from")
    to_id: str = Field(..., alias="to")
    duration_min: int
    distance_m: Optional[int] = None

    model_config = {"populate_by_name": True}


class RouteOptimizeResponse(BaseModel):
    ordered_poi_ids: List[str]
    legs: List[RouteLeg]
    warnings: List[str] = Field(default_factory=list)
    total_travel_minutes: int
    total_visit_minutes: int
    routing_source: str = "osrm"
