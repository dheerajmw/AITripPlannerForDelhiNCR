# Phase 2 — Implementation Details

**Status:** Complete

| # | Task | Status |
|---|------|--------|
| 2.1 | `RoutingClient` + OSRM table | Done |
| 2.2 | Haversine fallback + warnings | Done |
| 2.3 | Matrix builder (chunk → haversine if n>50) | Done |
| 2.4 | Nearest-neighbor + 2-opt | Done |
| 2.5 | `ConstraintValidator` time budget | Done |
| 2.6 | Leg sanity (zero duration fix) | Done |
| 2.7 | `POST /api/v1/route/optimize` | Done |
| 2.8 | Unknown `poi_id` → 400 | Done |

## Modules

| Module | Role |
|--------|------|
| `routing_client.py` | OSRM `/table/v1/walking/...` |
| `order_optimizer.py` | NN + 2-opt |
| `route_validator.py` | Budget check → 422 |
| `route_service.py` | Orchestration |
| `api/v1/route.py` | HTTP endpoint |
