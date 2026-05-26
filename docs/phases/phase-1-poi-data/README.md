# Phase 1: POI Data Layer

**Status:** Complete  
**Code:** `backend/app/db/`, `backend/app/services/`, `backend/scripts/`, `GET /api/v1/pois`

## Goal

Build the Delhi knowledge base from OpenStreetMap (Overpass), normalize POIs, persist to SQLite, expose query API.

## Deliverables

| Item | Location |
|------|----------|
| SQLite schema | `backend/app/db/schema.sql`, `models.py` |
| Overpass queries | `backend/scripts/overpass_queries/*.overpass` |
| Ingest CLI | `make ingest` → `scripts/ingest_pois.py` |
| Seed check | `make check-pois` → `scripts/check_poi_seed.py` |
| POI API | `GET /api/v1/pois?category=&interest=&limit=` |
| Health `poi_count` | `GET /api/v1/health` |

## Verify

```bash
make ingest          # ~5 min; requires network
make check-pois      # ≥500 POIs, ≥20 monument-like
make test-backend

curl "http://localhost:8000/api/v1/pois?category=attraction&limit=5"
curl "http://localhost:8000/api/v1/health"
```

## Documents in this folder

| File | Description |
|------|-------------|
| [README.md](./README.md) | This overview |
| [implementation.md](./implementation.md) | Task list (1.1–1.10) |
| [checklist.md](./checklist.md) | Phase gate |
| [architecture.md](./architecture.md) | Diagrams, APIs, code map |

## Next

[Phase 2 — Routing](../phase-2-routing/)
