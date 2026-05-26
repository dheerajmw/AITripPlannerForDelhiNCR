# Phase 2: Routing & Constraints

**Status:** Complete  
**Code:** `backend/app/services/routing_client.py`, `order_optimizer.py`, `route_service.py`, `POST /api/v1/route/optimize`

## Goal

Compute walking travel times between stops and return an optimized visit order within an optional time budget.

## API

```http
POST /api/v1/route/optimize
Content-Type: application/json

{
  "poi_ids": ["osm:node/1", "osm:node/2"],
  "start_lat": 28.6129,
  "start_lon": 77.2295,
  "mode": "walking",
  "max_total_minutes": 480
}
```

## Verify

```bash
make test-backend

# Example (API running, POIs from ingest):
curl -X POST http://localhost:8000/api/v1/route/optimize \
  -H "Content-Type: application/json" \
  -d '{"poi_ids":["...","..."],"start_lat":28.6129,"start_lon":77.2295,"max_total_minutes":480}'
```

## Documents in this folder

| File | Description |
|------|-------------|
| [README.md](./README.md) | This overview |
| [implementation.md](./implementation.md) | Task list (2.1–2.8) |
| [checklist.md](./checklist.md) | Phase gate |
| [architecture.md](./architecture.md) | Diagrams, APIs, code map |

## Next

[Phase 3 — Rule-based planner](../phase-3-planner/)
