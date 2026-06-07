"""Write rolling usage stats to data/analytics_summary.json."""

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from app.db.analytics_session import get_analytics_session_factory
from app.services.analytics_service import AnalyticsService
from app.settings import get_settings

SNAPSHOT_DAYS = 30
_DEBOUNCE_SEC = 30
_last_write_monotonic = 0.0


def analytics_snapshot_path() -> Path:
    return get_settings().data_dir / "analytics_summary.json"


def refresh_analytics_snapshot(*, force: bool = False) -> Optional[Path]:
    """Recompute stats from the DB and write JSON snapshot. Debounced unless force=True."""
    global _last_write_monotonic
    now = time.monotonic()
    if not force and now - _last_write_monotonic < _DEBOUNCE_SEC:
        return None

    settings = get_settings()
    session = get_analytics_session_factory()()
    try:
        summary = AnalyticsService(session).summary(days=SNAPSHOT_DAYS)
        today_utc = datetime.now(timezone.utc).date().isoformat()
        today_row = next((d for d in summary.daily if d.date == today_utc), None)

        payload: Dict[str, Any] = {
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "summary_days": SNAPSHOT_DAYS,
            "today": today_row.model_dump() if today_row else None,
            "daily": [d.model_dump() for d in summary.daily],
            "totals": summary.totals.model_dump(),
            "notes": {
                "unique_sessions": "Daily active users (one per browser session)",
                "page_views": "Explore / plan / itinerary page loads",
                "itineraries_generated": "Successful trip generations",
                "itineraries_viewed": "Itinerary page opens with saved data",
            },
        }

        path = analytics_snapshot_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        _last_write_monotonic = now
        return path
    finally:
        session.close()
