"""OSRM table client with haversine fallback."""

import logging
import math
from typing import List, Optional, Tuple

import httpx

from app.config import HAVERSINE_WALKING_FACTOR, WALKING_SPEED_M_PER_MIN
from app.settings import get_settings

logger = logging.getLogger(__name__)

# matrix[i][j] = duration seconds from i to j; None if unknown
DurationMatrix = List[List[Optional[float]]]


def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371000.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    )
    return 2 * r * math.asin(math.sqrt(a))


def haversine_duration_sec(
    lat1: float, lon1: float, lat2: float, lon2: float, factor: float = HAVERSINE_WALKING_FACTOR
) -> float:
    distance_m = haversine_m(lat1, lon1, lat2, lon2) * factor
    if distance_m < 1.0:
        return 0.0
    return (distance_m / WALKING_SPEED_M_PER_MIN) * 60.0


class RoutingClient:
    """Walking duration matrix via OSRM table API."""

    def __init__(self) -> None:
        settings = get_settings()
        self._base_url = settings.osrm_base_url.rstrip("/")
        self._timeout = 30.0

    def build_duration_matrix(
        self,
        coordinates: List[Tuple[float, float]],
        profile: str = "walking",
    ) -> Tuple[DurationMatrix, str, List[str]]:
        """
        coordinates: list of (lat, lon)
        Returns (matrix_seconds, source, warnings)
        """
        warnings: List[str] = []
        if len(coordinates) < 2:
            n = len(coordinates)
            return [[0.0 if i == j else None for j in range(n)] for i in range(n)], "haversine", warnings

        try:
            matrix = self._fetch_osrm_table(coordinates, profile)
            matrix, fix_warnings = self._fix_zero_duration_legs(coordinates, matrix)
            warnings.extend(fix_warnings)
            return matrix, "osrm", warnings
        except Exception as exc:
            logger.warning("OSRM table failed, using haversine fallback: %s", exc)
            warnings.append("OSRM unavailable; travel times estimated from straight-line distance.")
            return self._haversine_matrix(coordinates), "haversine", warnings

    def _fetch_osrm_table(
        self, coordinates: List[Tuple[float, float]], profile: str
    ) -> DurationMatrix:
        # OSRM expects lon,lat
        coord_str = ";".join(f"{lon},{lat}" for lat, lon in coordinates)
        url = f"{self._base_url}/table/v1/{profile}/{coord_str}"
        params = {"annotations": "duration"}

        with httpx.Client(timeout=self._timeout) as client:
            response = client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

        if data.get("code") != "Ok":
            raise RuntimeError(data.get("message", "OSRM table error"))

        durations = data.get("durations")
        if not durations:
            raise RuntimeError("OSRM returned empty durations")

        n = len(coordinates)
        matrix: DurationMatrix = []
        for i in range(n):
            row: List[Optional[float]] = []
            for j in range(n):
                val = durations[i][j] if i < len(durations) and j < len(durations[i]) else None
                row.append(val)
            matrix.append(row)
        return matrix

    def _haversine_matrix(self, coordinates: List[Tuple[float, float]]) -> DurationMatrix:
        n = len(coordinates)
        matrix: DurationMatrix = []
        for i in range(n):
            row: List[Optional[float]] = []
            lat1, lon1 = coordinates[i]
            for j in range(n):
                if i == j:
                    row.append(0.0)
                else:
                    lat2, lon2 = coordinates[j]
                    row.append(haversine_duration_sec(lat1, lon1, lat2, lon2))
            matrix.append(row)
        return matrix

    def _fix_zero_duration_legs(
        self,
        coordinates: List[Tuple[float, float]],
        matrix: DurationMatrix,
    ) -> Tuple[DurationMatrix, List[str]]:
        """EC-R-19: replace zero durations when points are far apart."""
        from app.config import LEG_ZERO_DISTANCE_THRESHOLD_M

        warnings: List[str] = []
        n = len(coordinates)
        fixed = [row[:] for row in matrix]
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                dur = fixed[i][j]
                lat1, lon1 = coordinates[i]
                lat2, lon2 = coordinates[j]
                dist = haversine_m(lat1, lon1, lat2, lon2)
                if dist > LEG_ZERO_DISTANCE_THRESHOLD_M and (dur is None or dur <= 0):
                    fixed[i][j] = haversine_duration_sec(lat1, lon1, lat2, lon2)
                    warnings.append(
                        f"Adjusted travel time for leg {i}->{j} (OSRM returned invalid duration)."
                    )
        return fixed, warnings


def chunk_indices(n: int, chunk_size: int) -> List[Tuple[int, int]]:
    """Inclusive index ranges for matrix chunks."""
    ranges = []
    start = 0
    while start < n:
        end = min(start + chunk_size, n)
        ranges.append((start, end))
        start = end
    return ranges


def build_matrix_chunked(
    client: RoutingClient,
    coordinates: List[Tuple[float, float]],
    chunk_size: int,
) -> Tuple[DurationMatrix, str, List[str]]:
    """Build full matrix; chunk OSRM requests when n > chunk_size."""
    n = len(coordinates)
    if n <= chunk_size:
        return client.build_duration_matrix(coordinates)

    warnings: List[str] = []
    # For MVP: use haversine for large sets to avoid complex chunk stitching
    warnings.append(f"Using haversine estimate for {n} stops (exceeds OSRM chunk size {chunk_size}).")
    matrix = client._haversine_matrix(coordinates)
    return matrix, "haversine", warnings
