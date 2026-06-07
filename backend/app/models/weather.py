"""Weather context returned with itineraries."""

from typing import Literal, Optional

from pydantic import BaseModel

WeatherBias = Literal["rain", "heat", "clear"]


class WeatherSummary(BaseModel):
    plan_date: str
    condition: str
    description: str
    temp_c: float
    bias: WeatherBias
    applied: bool = False
