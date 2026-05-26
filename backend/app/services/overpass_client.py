"""Overpass API client with retries (ingest only — not on user request path)."""

import logging
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import httpx

from app.config import NCR_BOUNDS
from app.settings import get_settings

logger = logging.getLogger(__name__)

QUERIES_DIR = Path(__file__).resolve().parents[2] / "scripts" / "overpass_queries"


def _bbox_placeholder() -> str:
    b = NCR_BOUNDS
    return f"{b['min_lat']},{b['min_lon']},{b['max_lat']},{b['max_lon']}"


def load_query(name: str) -> str:
    path = QUERIES_DIR / f"{name}.overpass"
    if not path.exists():
        raise FileNotFoundError(f"Overpass query not found: {path}")
    template = path.read_text(encoding="utf-8")
    return template.replace("{{bbox}}", _bbox_placeholder())


def list_query_names() -> List[str]:
    return sorted(p.stem for p in QUERIES_DIR.glob("*.overpass"))


class OverpassClient:
    def __init__(self) -> None:
        settings = get_settings()
        self._url = settings.overpass_api_url
        self._timeout = settings.overpass_timeout_sec
        self._max_retries = settings.overpass_max_retries

    def fetch_query(self, query: str) -> List[Dict[str, Any]]:
        last_error: Optional[Exception] = None
        for attempt in range(self._max_retries):
            try:
                with httpx.Client(timeout=self._timeout) as client:
                    response = client.post(
                        self._url,
                        data={"data": query},
                        headers={
                            "User-Agent": "AITripPlanner/0.1 (Delhi MVP; contact: local-dev)",
                        },
                    )
                if response.status_code == 429:
                    wait = 2 ** attempt
                    logger.warning("Overpass rate limit; retry in %ss", wait)
                    time.sleep(wait)
                    continue
                if response.status_code >= 500:
                    wait = 2 ** attempt
                    logger.warning("Overpass server error %s; retry in %ss", response.status_code, wait)
                    time.sleep(wait)
                    continue
                response.raise_for_status()
                payload = response.json()
                return payload.get("elements") or []
            except (httpx.HTTPError, ValueError) as exc:
                last_error = exc
                wait = 2 ** attempt
                logger.warning("Overpass request failed: %s; retry in %ss", exc, wait)
                time.sleep(wait)
        raise RuntimeError(f"Overpass API failed after {self._max_retries} retries") from last_error

    def fetch_named_query(self, name: str) -> List[Dict[str, Any]]:
        query = load_query(name)
        logger.info("Fetching Overpass query: %s", name)
        return self.fetch_query(query)

    def fetch_all_queries(self, pause_sec: float = 3.0) -> List[Dict[str, Any]]:
        elements: List[Dict[str, Any]] = []
        seen_ids = set()
        names = list_query_names()
        for index, name in enumerate(names):
            if index > 0 and pause_sec > 0:
                time.sleep(pause_sec)
            batch = self.fetch_named_query(name)
            for el in batch:
                key = (el.get("type"), el.get("id"))
                if key in seen_ids:
                    continue
                seen_ids.add(key)
                elements.append(el)
        return elements
