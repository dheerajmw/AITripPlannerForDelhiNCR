"""Delhi NCR geographic contract and app constants — single source of truth."""

from typing import Dict, FrozenSet, Literal, Tuple

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

# Curated start points — all inside NCR_BOUNDS (used for location search + validation)
NCR_START_LOCATIONS: Tuple[Dict[str, object], ...] = (
    {"id": "landmark:india-gate", "label": "India Gate", "lat": 28.6129, "lon": 77.2295},
    {"id": "landmark:connaught-place", "label": "Connaught Place", "lat": 28.6315, "lon": 77.2167},
    {"id": "landmark:red-fort", "label": "Red Fort", "lat": 28.6562, "lon": 77.2410},
    {"id": "landmark:qutub-minar", "label": "Qutub Minar", "lat": 28.5244, "lon": 77.1855},
    {"id": "landmark:lodhi-gardens", "label": "Lodhi Gardens", "lat": 28.5931, "lon": 77.2197},
    {"id": "landmark:hauz-khas", "label": "Hauz Khas Village", "lat": 28.5494, "lon": 77.2001},
    {"id": "landmark:akshardham", "label": "Akshardham Temple", "lat": 28.6127, "lon": 77.2773},
    {"id": "landmark:khan-market", "label": "Khan Market", "lat": 28.6003, "lon": 77.2269},
    {"id": "landmark:nizamuddin", "label": "Nizamuddin", "lat": 28.5911, "lon": 77.2420},
    {"id": "landmark:cyber-hub", "label": "Cyber Hub, Gurgaon", "lat": 28.4950, "lon": 77.0890},
    {"id": "landmark:select-citywalk", "label": "Select Citywalk", "lat": 28.5286, "lon": 77.2189},
    {"id": "landmark:dwarka", "label": "Dwarka Sector 21", "lat": 28.5522, "lon": 77.0590},
)

LOCATION_SEARCH_MIN_QUERY_LEN = 2
LOCATION_SEARCH_DEFAULT_LIMIT = 10
LOCATION_SEARCH_MAX_LIMIT = 20

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

# Weather-aware planning (Phase 6)
OUTDOOR_POI_CATEGORIES: FrozenSet[str] = frozenset({"park", "nature"})
INDOOR_POI_CATEGORIES: FrozenSet[str] = frozenset(
    {
        "cafe",
        "restaurant",
        "monument",
        "museum",
        "attraction",
        "historic",
        "bar",
        "pub",
    }
)
WEATHER_PLANNING_TZ = "Asia/Kolkata"

# Google Maps — only named / verified POIs are used in itineraries
MAPS_VERIFY_MAX_DISTANCE_M = 1500
WEATHER_RAIN_CONDITIONS: FrozenSet[str] = frozenset({"Rain", "Drizzle", "Thunderstorm"})
WEATHER_HEAT_THRESHOLD_C = 40.0
WEATHER_OUTDOOR_VISIT_FACTOR = 0.75
WEATHER_MIN_OUTDOOR_VISIT_MINUTES = 20
WEATHER_FORECAST_MAX_DAYS = 5
WEATHER_CACHE_TTL_SEC = 3 * 60 * 60
WEATHER_DISCLAIMER = "Weather forecasts are approximate; conditions may differ on the day."

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
