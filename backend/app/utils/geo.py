"""Geographic helpers for Delhi NCR scope enforcement."""

from app.config import NCR_BOUNDS


def in_ncr_bounds(lat: float, lon: float) -> bool:
    """Return True if point is inside Delhi NCR bounding box (inclusive)."""
    return (
        NCR_BOUNDS["min_lat"] <= lat <= NCR_BOUNDS["max_lat"]
        and NCR_BOUNDS["min_lon"] <= lon <= NCR_BOUNDS["max_lon"]
    )


def clamp_to_ncr(lat: float, lon: float) -> tuple[float, float]:
    """Clamp coordinates to the nearest point inside NCR bounds."""
    clamped_lat = min(max(lat, NCR_BOUNDS["min_lat"]), NCR_BOUNDS["max_lat"])
    clamped_lon = min(max(lon, NCR_BOUNDS["min_lon"]), NCR_BOUNDS["max_lon"])
    return clamped_lat, clamped_lon


def is_valid_coordinate(lat: float, lon: float) -> bool:
    """Basic WGS84 sanity check."""
    return -90 <= lat <= 90 and -180 <= lon <= 180


def is_delhi_area_coordinate(lat: float, lon: float) -> bool:
    """Rough sanity check for Delhi NCR region (EC-G-06)."""
    return 28.0 <= lat <= 29.5 and 76.5 <= lon <= 78.0
