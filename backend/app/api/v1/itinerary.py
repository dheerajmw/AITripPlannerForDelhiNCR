"""Itinerary generation API."""

from typing import Literal

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.exceptions import ValidationAppError
from app.models.itinerary import ItineraryGenerateRequest, ItineraryResponse
from app.services.ai.ai_planner import AIPlannerService
from app.services.planner.orchestrator import PlannerOrchestrator

router = APIRouter(tags=["itinerary"])


@router.post("/itinerary/generate", response_model=ItineraryResponse)
async def generate_itinerary(
    body: ItineraryGenerateRequest,
    mode: Literal["rule", "ai"] = Query(default="rule", description="Planner mode"),
    db: Session = Depends(get_db),
) -> ItineraryResponse:
    """Build a day itinerary (rule-based or Groq-enhanced notes)."""
    if mode == "rule":
        return PlannerOrchestrator(db).generate(body)
    if mode == "ai":
        return AIPlannerService(db).generate(body)
    raise ValidationAppError(
        f"Unsupported planner mode '{mode}'",
        details={"allowed": ["rule", "ai"]},
    )
