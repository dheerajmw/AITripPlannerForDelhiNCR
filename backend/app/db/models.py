"""SQLAlchemy ORM models."""

import json
from datetime import datetime
from typing import List

from sqlalchemy import DateTime, Float, Integer, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class POIRecord(Base):
    __tablename__ = "pois"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(512), nullable=False)
    category: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    tags: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    lat: Mapped[float] = mapped_column(Float, nullable=False)
    lon: Mapped[float] = mapped_column(Float, nullable=False)
    opening_hours: Mapped[str] = mapped_column(String(256), nullable=True)
    estimated_visit_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=45)
    source: Mapped[str] = mapped_column(String(32), nullable=False, default="osm")
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    def get_tags_list(self) -> List[str]:
        try:
            data = json.loads(self.tags)
            return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            return []

    def set_tags_list(self, tag_list: List[str]) -> None:
        self.tags = json.dumps(sorted(set(tag_list)))
