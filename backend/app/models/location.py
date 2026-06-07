"""Location search schemas for Delhi NCR start points."""

from typing import List, Literal

from pydantic import BaseModel, Field


class LocationOption(BaseModel):
    id: str
    label: str
    lat: float
    lon: float
    source: Literal["landmark", "poi"] = "landmark"


class LocationSearchResponse(BaseModel):
    query: str
    items: List[LocationOption] = Field(default_factory=list)
