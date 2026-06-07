"""Anonymous usage analytics."""

from typing import Optional

from fastapi import APIRouter, Depends, Header, Query
from sqlalchemy.orm import Session

from app.db.analytics_session import get_analytics_db
from app.exceptions import AppError, ValidationAppError
from app.models.analytics import (
    AnalyticsEventAccepted,
    AnalyticsEventCreate,
    AnalyticsSummaryResponse,
)
from app.services.analytics_service import AnalyticsService
from app.settings import get_settings

router = APIRouter(tags=["analytics"])


@router.post("/analytics/events", response_model=AnalyticsEventAccepted, status_code=202)
async def record_event(
    payload: AnalyticsEventCreate,
    db: Session = Depends(get_analytics_db),
) -> AnalyticsEventAccepted:
    """Accept anonymous funnel events from the frontend."""
    try:
        AnalyticsService(db).record(payload)
    except ValueError as exc:
        raise ValidationAppError(str(exc)) from exc
    return AnalyticsEventAccepted()


@router.get("/analytics/summary", response_model=AnalyticsSummaryResponse)
async def analytics_summary(
    days: int = Query(7, ge=1, le=90),
    x_analytics_key: Optional[str] = Header(default=None, alias="X-Analytics-Key"),
    db: Session = Depends(get_analytics_db),
) -> AnalyticsSummaryResponse:
    """Daily active sessions and funnel counts. Requires ANALYTICS_READ_KEY header."""
    settings = get_settings()
    if not settings.analytics_read_key:
        raise AppError(
            "ANALYTICS_DISABLED",
            "Analytics summary is not configured. Set ANALYTICS_READ_KEY on the server.",
            status_code=503,
        )
    if x_analytics_key != settings.analytics_read_key:
        raise AppError("UNAUTHORIZED", "Invalid analytics key.", status_code=401)

    return AnalyticsService(db).summary(days=days)
