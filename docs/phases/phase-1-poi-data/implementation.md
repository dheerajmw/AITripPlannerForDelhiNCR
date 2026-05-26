# Phase 1 — Implementation Details

**Status:** Complete

## Tasks

| # | Task | Status |
|---|------|--------|
| 1.1 | SQLite schema + SQLAlchemy models | Done |
| 1.2 | Overpass query templates | Done |
| 1.3 | `ingest_pois.py` | Done |
| 1.4 | OSM normalizer | Done |
| 1.5 | Dedupe (&lt;50m, similar name) | Done |
| 1.6 | Out-of-bounds / missing coords filter | Done |
| 1.7 | `POIRepository` | Done |
| 1.8 | `GET /api/v1/pois` | Done |
| 1.9 | `poi_count` on health | Done |
| 1.10 | `check_poi_seed.py` | Done |

## Ingest stats (reference run)

After `make ingest`: ~13k+ POIs across cafe, restaurant, park, nature, attraction, historic, museum, bar, pub.

## Overpass strategy

- Ingest only via `make ingest` — **never** on user request path
- 3s pause between query files; 5 retries with exponential backoff
- User-Agent header required by Overpass API
