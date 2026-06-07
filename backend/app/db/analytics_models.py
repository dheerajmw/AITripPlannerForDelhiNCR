"""Anonymous usage events — separate from POI data."""

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import DateTime, Index, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class AnalyticsBase(DeclarativeBase):
    pass


class AnalyticsEventRecord(AnalyticsBase):
    __tablename__ = "analytics_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    event: Mapped[str] = mapped_column(String(64), nullable=False)
    page: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    properties_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    __table_args__ = (
        Index("ix_analytics_events_created_at", "created_at"),
        Index("ix_analytics_events_event", "event"),
        Index("ix_analytics_events_session_id", "session_id"),
    )
