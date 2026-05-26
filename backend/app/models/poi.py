"""POI API schemas."""

from typing import List, Optional

from pydantic import BaseModel, Field


class POIResponse(BaseModel):
    id: str
    name: str
    category: str
    tags: List[str] = Field(default_factory=list)
    lat: float
    lon: float
    opening_hours: Optional[str] = None
    estimated_visit_minutes: int
    source: str = "osm"


class POIListResponse(BaseModel):
    items: List[POIResponse]
    total: int
    limit: int
