"""Record and summarize anonymous usage events."""

import json
from datetime import date, datetime, timedelta, timezone
from typing import Dict, List, Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.analytics_models import AnalyticsEventRecord
from app.models.analytics import (
    AnalyticsEventCreate,
    AnalyticsSummaryResponse,
    DailyAnalyticsRow,
)

_EVENT_REQUIRES_PAGE = frozenset({"page_view"})


class AnalyticsService:
    def __init__(self, session: Session) -> None:
        self._session = session

    def record(self, payload: AnalyticsEventCreate) -> None:
        if payload.event in _EVENT_REQUIRES_PAGE and not payload.page:
            raise ValueError("page is required for page_view events")

        props_json: Optional[str] = None
        if payload.properties:
            props_json = json.dumps(payload.properties, separators=(",", ":"))

        row = AnalyticsEventRecord(
            session_id=(payload.session_id or "").strip() or None,
            event=payload.event,
            page=payload.page,
            properties_json=props_json,
            created_at=datetime.now(timezone.utc),
        )
        self._session.add(row)
        self._session.commit()

        from app.services.analytics_snapshot import refresh_analytics_snapshot

        refresh_analytics_snapshot()

    def summary(self, *, days: int = 7) -> AnalyticsSummaryResponse:
        days = max(1, min(days, 90))
        start = datetime.now(timezone.utc).replace(
            hour=0, minute=0, second=0, microsecond=0
        ) - timedelta(days=days - 1)

        rows = self._session.execute(
            select(AnalyticsEventRecord).where(AnalyticsEventRecord.created_at >= start)
        ).scalars().all()

        by_date: Dict[str, DailyAnalyticsRow] = {}
        for offset in range(days):
            d = (start.date() + timedelta(days=offset)).isoformat()
            by_date[d] = DailyAnalyticsRow(
                date=d,
                unique_sessions=0,
                page_views=0,
                itineraries_generated=0,
                itineraries_viewed=0,
            )

        sessions_per_day: Dict[str, set[str]] = {d: set() for d in by_date}

        for row in rows:
            day_key = row.created_at.astimezone(timezone.utc).date().isoformat()
            if day_key not in by_date:
                continue
            bucket = by_date[day_key]
            if row.event == "page_view":
                bucket.page_views += 1
            elif row.event == "itinerary_generated":
                bucket.itineraries_generated += 1
            elif row.event == "itinerary_viewed":
                bucket.itineraries_viewed += 1
            if row.session_id:
                sessions_per_day[day_key].add(row.session_id)

        daily: List[DailyAnalyticsRow] = []
        totals = DailyAnalyticsRow(
            date="total",
            unique_sessions=0,
            page_views=0,
            itineraries_generated=0,
            itineraries_viewed=0,
        )
        all_sessions: set[str] = set()

        for day_key in sorted(by_date.keys()):
            row = by_date[day_key]
            row.unique_sessions = len(sessions_per_day[day_key])
            all_sessions.update(sessions_per_day[day_key])
            daily.append(row)
            totals.page_views += row.page_views
            totals.itineraries_generated += row.itineraries_generated
            totals.itineraries_viewed += row.itineraries_viewed

        totals.unique_sessions = len(all_sessions)

        return AnalyticsSummaryResponse(days=days, daily=daily, totals=totals)
