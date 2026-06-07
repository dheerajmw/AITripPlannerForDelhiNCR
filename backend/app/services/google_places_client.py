"""Verify POIs exist on Google Maps via Places API (optional)."""

from __future__ import annotations

import logging
import os
import time
from typing import Dict, Optional, Tuple

import httpx

from app.config import MAPS_VERIFY_MAX_DISTANCE_M
from app.db.models import POIRecord
from app.settings import get_settings
from app.services.routing_client import haversine_m

logger = logging.getLogger(__name__)

_PLACEHOLDER_KEYS = frozenset({"", "your_google_maps_key", "changeme", "xxx"})
_CACHE: Dict[str, Tuple[float, bool]] = {}
_CACHE_TTL_SEC = 7 * 24 * 60 * 60


class GooglePlacesClient:
    def __init__(self) -> None:
        self.last_error: Optional[str] = None

    def _resolve_api_key(self) -> str:
        settings = get_settings()
        return (
            settings.google_maps_api_key
            or os.environ.get("GOOGLE_MAPS_API_KEY")
            or os.environ.get("NEXT_PUBLIC_GOOGLE_MAPS_API_KEY")
            or ""
        ).strip()

    def is_configured(self) -> bool:
        key = self._resolve_api_key().lower()
        return bool(key) and key not in _PLACEHOLDER_KEYS

    def verify_poi(self, poi: POIRecord) -> bool:
        """Return True if Google Places finds this name near the POI coordinates."""
        self.last_error = None
        api_key = self._resolve_api_key()
        if not api_key or api_key.lower() in _PLACEHOLDER_KEYS:
            return True

        cache_key = f"{poi.id}:{poi.lat:.4f},{poi.lon:.4f}"
        cached = _CACHE.get(cache_key)
        if cached and time.time() - cached[0] < _CACHE_TTL_SEC:
            return cached[1]

        ok = self._lookup_place(api_key=api_key, name=poi.name, lat=poi.lat, lon=poi.lon)
        _CACHE[cache_key] = (time.time(), ok)
        return ok

    def _lookup_place(self, *, api_key: str, name: str, lat: float, lon: float) -> bool:
        url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
        params = {
            "input": name,
            "inputtype": "textquery",
            "fields": "place_id,name,geometry",
            "locationbias": f"circle:{MAPS_VERIFY_MAX_DISTANCE_M}@{lat},{lon}",
            "key": api_key,
        }
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(url, params=params)
        except httpx.HTTPError as exc:
            self.last_error = str(exc)
            logger.warning("Google Places request failed for %s: %s", name, exc)
            return False

        if response.status_code != 200:
            self.last_error = f"HTTP {response.status_code}"
            return False

        payload = response.json()
        status = payload.get("status")
        if status == "ZERO_RESULTS":
            return False
        if status not in {"OK", "ZERO_RESULTS"}:
            self.last_error = str(status)
            logger.warning("Google Places status %s for %s", status, name)
            return False

        candidates = payload.get("candidates") or []
        if not candidates:
            return False

        place = candidates[0]
        geometry = place.get("geometry") or {}
        location = geometry.get("location") or {}
        place_lat = location.get("lat")
        place_lon = location.get("lng")
        if not isinstance(place_lat, (int, float)) or not isinstance(place_lon, (int, float)):
            return False

        distance = haversine_m(lat, lon, float(place_lat), float(place_lon))
        return distance <= MAPS_VERIFY_MAX_DISTANCE_M
