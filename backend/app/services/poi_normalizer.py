"""Map raw OSM elements to normalized POI records."""

import re
from typing import Any, Dict, List, Optional, Tuple

from app.config import DEFAULT_VISIT_MINUTES_BY_CATEGORY, Interest
from app.db.models import POIRecord
from app.utils.geo import in_ncr_bounds, is_valid_coordinate

_UNNAMED_PREFIX = {
    "cafe": "Unnamed cafe",
    "restaurant": "Unnamed restaurant",
    "monument": "Unnamed monument",
    "museum": "Unnamed museum",
    "attraction": "Unnamed attraction",
    "historic": "Unnamed historic site",
    "park": "Unnamed park",
    "nature": "Unnamed natural site",
    "bar": "Unnamed bar",
    "pub": "Unnamed pub",
}


def _tags_dict(element: Dict[str, Any]) -> Dict[str, str]:
    raw = element.get("tags") or {}
    return {str(k): str(v) for k, v in raw.items()}


def _element_coords(element: Dict[str, Any]) -> Optional[Tuple[float, float]]:
    lat = element.get("lat")
    lon = element.get("lon")
    if lat is not None and lon is not None:
        return float(lat), float(lon)
    center = element.get("center") or {}
    clat = center.get("lat")
    clon = center.get("lon")
    if clat is not None and clon is not None:
        return float(clat), float(clon)
    return None


def _osm_id(element: Dict[str, Any]) -> Optional[str]:
    osm_type = element.get("type")
    osm_id = element.get("id")
    if osm_type and osm_id is not None:
        return f"osm:{osm_type}/{osm_id}"
    return None


def classify_category(tags: Dict[str, str]) -> Tuple[str, List[str]]:
    """Return (category, interest_tags)."""
    amenity = tags.get("amenity", "")
    tourism = tags.get("tourism", "")
    leisure = tags.get("leisure", "")
    historic = tags.get("historic", "")
    natural = tags.get("natural", "")

    interest_tags: List[str] = []

    if amenity in ("cafe", "coffee_shop"):
        interest_tags.append("food")
        return "cafe", interest_tags
    if amenity == "restaurant":
        interest_tags.append("food")
        return "restaurant", interest_tags
    if amenity in ("bar", "biergarten"):
        interest_tags.extend(["food", "nightlife"])
        return "bar", interest_tags
    if amenity == "pub":
        interest_tags.extend(["food", "nightlife"])
        return "pub", interest_tags
    if tourism == "museum":
        interest_tags.append("history")
        return "museum", interest_tags
    if tourism in ("attraction", "viewpoint", "artwork"):
        interest_tags.append("history")
        return "attraction", interest_tags
    if historic:
        interest_tags.append("history")
        return "historic", interest_tags
    if leisure == "park" or tourism == "park":
        interest_tags.append("nature")
        return "park", interest_tags
    if natural:
        interest_tags.append("nature")
        return "nature", interest_tags
    if tags.get("tourism") == "attraction":
        interest_tags.append("history")
        return "attraction", interest_tags

    # Fallbacks for loose tagging
    if amenity:
        interest_tags.append("food")
        return "restaurant", interest_tags
    if tourism:
        interest_tags.append("history")
        return "attraction", interest_tags

    return "attraction", ["history"]


def display_name(tags: Dict[str, str], category: str) -> str:
    for key in ("name:en", "name", "brand"):
        if tags.get(key):
            return tags[key].strip()
    prefix = _UNNAMED_PREFIX.get(category, "Unnamed place")
    return prefix


def normalize_element(element: Dict[str, Any]) -> Optional[POIRecord]:
    """Convert one Overpass element to POIRecord, or None if invalid."""
    if element.get("type") not in ("node", "way", "relation"):
        return None

    poi_id = _osm_id(element)
    coords = _element_coords(element)
    if not poi_id or not coords:
        return None

    lat, lon = coords
    if not is_valid_coordinate(lat, lon) or not in_ncr_bounds(lat, lon):
        return None

    tags = _tags_dict(element)
    if not tags:
        return None

    category, interest_tags = classify_category(tags)
    name = display_name(tags, category)
    opening_hours = tags.get("opening_hours")
    visit_min = DEFAULT_VISIT_MINUTES_BY_CATEGORY.get(category, 45)

    tag_set = list(set(interest_tags))
    if category not in tag_set:
        tag_set.append(category)

    record = POIRecord(
        id=poi_id,
        name=name,
        category=category,
        lat=lat,
        lon=lon,
        opening_hours=opening_hours,
        estimated_visit_minutes=visit_min,
        source="osm",
    )
    record.set_tags_list(tag_set)
    return record


def normalize_elements(elements: List[Dict[str, Any]]) -> List[POIRecord]:
    results: List[POIRecord] = []
    for element in elements:
        record = normalize_element(element)
        if record:
            results.append(record)
    return results


def _normalize_name(name: str) -> str:
    return re.sub(r"\s+", " ", name.lower().strip())


def _names_similar(a: str, b: str) -> bool:
    na, nb = _normalize_name(a), _normalize_name(b)
    if na == nb:
        return True
    if na in nb or nb in na:
        return True
    # Simple token overlap
    ta, tb = set(na.split()), set(nb.split())
    if not ta or not tb:
        return False
    overlap = len(ta & tb) / min(len(ta), len(tb))
    return overlap >= 0.8


def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    from math import asin, cos, radians, sin, sqrt

    r = 6371000.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    return 2 * r * asin(sqrt(a))


def dedupe_pois(records: List[POIRecord], distance_m: float = 50.0) -> List[POIRecord]:
    """Remove duplicates within distance_m with similar names."""
    kept: List[POIRecord] = []
    for record in sorted(records, key=lambda r: (r.name.startswith("Unnamed"), r.name)):
        duplicate = False
        for existing in kept:
            if record.category != existing.category:
                continue
            if haversine_m(record.lat, record.lon, existing.lat, existing.lon) > distance_m:
                continue
            if _names_similar(record.name, existing.name):
                duplicate = True
                break
        if not duplicate:
            kept.append(record)
    return kept
