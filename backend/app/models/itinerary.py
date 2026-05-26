"""Itinerary generation API schemas."""

from typing import List, Literal, Optional

from pydantic import BaseModel, Field, field_validator

from app.config import (
    DURATIONS_MINUTES,
    SUPPORTED_BUDGET_TIERS,
    SUPPORTED_DURATIONS,
    SUPPORTED_INTERESTS,
)


class CostRangeInr(BaseModel):
    low: int
    high: int

    @field_validator("high")
    @classmethod
    def high_gte_low(cls, v: int, info) -> int:
        low = info.data.get("low", 0)
        if v < low:
            return low
        return v


class StartPoint(BaseModel):
    lat: float
    lon: float
    label: str = "Custom start"


class ItineraryGenerateRequest(BaseModel):
    budget: Literal["low", "medium", "high"]
    interests: List[str] = Field(..., min_length=1)
    duration: Literal["4h", "8h", "1d"]
    start_lat: Optional[float] = None
    start_lon: Optional[float] = None
    start_label: Optional[str] = None

    @field_validator("interests")
    @classmethod
    def validate_interests(cls, v: List[str]) -> List[str]:
        invalid = [i for i in v if i not in SUPPORTED_INTERESTS]
        if invalid:
            raise ValueError(f"Unsupported interests: {invalid}")
        return list(dict.fromkeys(v))

    @field_validator("budget")
    @classmethod
    def validate_budget(cls, v: str) -> str:
        if v not in SUPPORTED_BUDGET_TIERS:
            raise ValueError(f"Unsupported budget: {v}")
        return v

    @field_validator("duration")
    @classmethod
    def validate_duration(cls, v: str) -> str:
        if v not in SUPPORTED_DURATIONS:
            raise ValueError(f"Unsupported duration: {v}")
        return v

    @property
    def duration_minutes(self) -> int:
        return DURATIONS_MINUTES[self.duration]

    def resolved_start(self) -> StartPoint:
        from app.config import DEFAULT_START

        if self.start_lat is not None and self.start_lon is not None:
            return StartPoint(
                lat=self.start_lat,
                lon=self.start_lon,
                label=self.start_label or "Custom start",
            )
        return StartPoint(
            lat=DEFAULT_START["lat"],
            lon=DEFAULT_START["lon"],
            label=DEFAULT_START.get("label", "India Gate"),
        )


class ItineraryStop(BaseModel):
    order: int
    poi_id: str
    name: str
    category: str
    lat: float
    lon: float
    arrive_at: str
    depart_at: str
    visit_minutes: int
    travel_to_next_minutes: Optional[int] = None
    cost_estimate_inr: CostRangeInr
    notes: str = ""


class ItineraryMeta(BaseModel):
    city: str
    duration_minutes: int
    budget_tier: str
    schema_version: str
    start_point: StartPoint
    warnings: List[str] = Field(default_factory=list)
    planner_mode: str = "rule"
    routing_source: Optional[str] = None
    ai_status: Optional[str] = None
    fallback_reason: Optional[str] = None


class ItinerarySummary(BaseModel):
    total_stops: int
    total_travel_min: int
    total_visit_min: int = 0
    total_cost_inr: CostRangeInr


class ItineraryResponse(BaseModel):
    meta: ItineraryMeta
    stops: List[ItineraryStop]
    summary: ItinerarySummary
