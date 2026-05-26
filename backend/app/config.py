"""Delhi NCR geographic contract and app constants — single source of truth."""

from typing import Dict, Literal, Tuple

# Delhi NCR bounding box (refine with GeoJSON in Phase 1)
NCR_BOUNDS = {
    "min_lat": 28.40,
    "max_lat": 28.88,
    "min_lon": 76.84,
    "max_lon": 77.45,
}

DEFAULT_CITY = "Delhi NCR"

DEFAULT_START = {
    "lat": 28.6129,
    "lon": 77.2295,
    "label": "India Gate",
}

DURATIONS_MINUTES: Dict[str, int] = {
    "4h": 240,
    "8h": 480,
    "1d": 1440,
}

MAX_DURATION_MINUTES = 1440
DEFAULT_TRANSPORT_MODE: Literal["walking"] = "walking"

BudgetTier = Literal["low", "medium", "high"]
Interest = Literal["food", "history", "nightlife", "nature"]
DurationKey = Literal["4h", "8h", "1d"]

SUPPORTED_BUDGET_TIERS: Tuple[BudgetTier, ...] = ("low", "medium", "high")
SUPPORTED_INTERESTS: Tuple[Interest, ...] = ("food", "history", "nightlife", "nature")
SUPPORTED_DURATIONS: Tuple[DurationKey, ...] = ("4h", "8h", "1d")

APP_VERSION = "0.1.0"

# POI categories (internal) — Phase 1
PoiCategory = Literal[
    "cafe",
    "restaurant",
    "monument",
    "museum",
    "attraction",
    "historic",
    "park",
    "nature",
    "bar",
    "pub",
]

SUPPORTED_POI_CATEGORIES: Tuple[PoiCategory, ...] = (
    "cafe",
    "restaurant",
    "monument",
    "museum",
    "attraction",
    "historic",
    "park",
    "nature",
    "bar",
    "pub",
)

# User interest → POI categories for filtering
INTEREST_TO_CATEGORIES: Dict[Interest, Tuple[str, ...]] = {
    "food": ("cafe", "restaurant"),
    "history": ("monument", "museum", "attraction", "historic"),
    "nature": ("park", "nature"),
    "nightlife": ("bar", "pub"),
}

DEFAULT_VISIT_MINUTES_BY_CATEGORY: Dict[str, int] = {
    "cafe": 45,
    "restaurant": 60,
    "monument": 60,
    "museum": 90,
    "attraction": 60,
    "historic": 45,
    "park": 60,
    "nature": 45,
    "bar": 90,
    "pub": 90,
}

POI_LIST_DEFAULT_LIMIT = 50
POI_LIST_MAX_LIMIT = 200
MIN_POI_SEED_COUNT = 500

# Routing (Phase 2)
TransportMode = Literal["walking"]
SUPPORTED_TRANSPORT_MODES: Tuple[TransportMode, ...] = ("walking",)
MAX_ROUTE_POIS = 20
OSRM_TABLE_MAX_COORDS = 50
HAVERSINE_WALKING_FACTOR = 1.3
WALKING_SPEED_M_PER_MIN = 5000.0 / 60.0  # ~5 km/h
LEG_ZERO_DISTANCE_THRESHOLD_M = 500.0

# Planner (Phase 3)
ITINERARY_SCHEMA_VERSION = "1.0"

# AI / Groq (Phase 4)
AI_CONTEXT_POI_CAP = 20
GROQ_TEMPERATURE = 0.3
AI_NOTES_MAX_LENGTH = 500
MIN_ITINERARY_STOPS = 2
MAX_ITINERARY_STOPS = 8
SCHEDULE_BUFFER_MINUTES = 12
DEFAULT_SCHEDULE_START_HOUR = 9
DEFAULT_SCHEDULE_START_MINUTE = 0
NIGHTLIFE_CATEGORIES = ("bar", "pub")
NIGHTLIFE_EARLIEST_HOUR = 17

BUDGET_ALLOWED_CATEGORIES: Dict[str, Tuple[str, ...]] = {
    "low": ("park", "nature", "historic", "monument", "attraction", "museum", "cafe"),
    "medium": SUPPORTED_POI_CATEGORIES,
    "high": SUPPORTED_POI_CATEGORIES,
}

# Per-stop cost heuristics (INR) by category and budget tier: (low, high)
COST_INR_BY_CATEGORY: Dict[str, Dict[str, Tuple[int, int]]] = {
    "low": {
        "cafe": (50, 200),
        "restaurant": (150, 400),
        "monument": (0, 50),
        "museum": (0, 100),
        "attraction": (0, 100),
        "historic": (0, 50),
        "park": (0, 0),
        "nature": (0, 0),
        "bar": (200, 600),
        "pub": (200, 600),
    },
    "medium": {
        "cafe": (100, 350),
        "restaurant": (300, 800),
        "monument": (0, 150),
        "museum": (50, 300),
        "attraction": (0, 200),
        "historic": (0, 100),
        "park": (0, 50),
        "nature": (0, 50),
        "bar": (400, 1200),
        "pub": (400, 1200),
    },
    "high": {
        "cafe": (200, 600),
        "restaurant": (600, 2000),
        "monument": (0, 200),
        "museum": (100, 500),
        "attraction": (0, 400),
        "historic": (0, 200),
        "park": (0, 100),
        "nature": (0, 100),
        "bar": (800, 2500),
        "pub": (800, 2500),
    },
}
