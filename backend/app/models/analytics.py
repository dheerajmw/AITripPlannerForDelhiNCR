"""Analytics API schemas."""

from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, Field

AnalyticsEventName = Literal[
    "page_view",
    "itinerary_generated",
    "itinerary_viewed",
]

AnalyticsPage = Literal["explore", "plan", "itinerary"]


class AnalyticsEventCreate(BaseModel):
    event: AnalyticsEventName
    session_id: Optional[str] = Field(default=None, max_length=64)
    page: Optional[AnalyticsPage] = None
    properties: Optional[Dict[str, str]] = None


class AnalyticsEventAccepted(BaseModel):
    ok: bool = True


class DailyAnalyticsRow(BaseModel):
    date: str
    unique_sessions: int
    page_views: int
    itineraries_generated: int
    itineraries_viewed: int


class AnalyticsSummaryResponse(BaseModel):
    days: int
    daily: List[DailyAnalyticsRow]
    totals: DailyAnalyticsRow
