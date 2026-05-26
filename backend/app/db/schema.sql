-- Reference schema for POI store (applied via SQLAlchemy models)
CREATE TABLE IF NOT EXISTS pois (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    tags TEXT NOT NULL DEFAULT '[]',
    lat REAL NOT NULL,
    lon REAL NOT NULL,
    opening_hours TEXT,
    estimated_visit_minutes INTEGER NOT NULL DEFAULT 45,
    source TEXT NOT NULL DEFAULT 'osm',
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_pois_category ON pois(category);
CREATE INDEX IF NOT EXISTS idx_pois_lat_lon ON pois(lat, lon);
