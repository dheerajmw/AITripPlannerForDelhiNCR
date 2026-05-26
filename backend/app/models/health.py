"""Health check response models."""

from typing import Optional

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    version: str
    city: str
    poi_count: Optional[int] = None
