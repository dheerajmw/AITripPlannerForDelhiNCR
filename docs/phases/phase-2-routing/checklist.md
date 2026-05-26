# Phase 2 — Exit Checklist

## API

- [x] `POST /api/v1/route/optimize` returns `ordered_poi_ids` and `legs`
- [x] Unknown `poi_id` → `400 VALIDATION_ERROR`
- [x] Exceeds `max_total_minutes` → `422 UNPROCESSABLE_PLAN`
- [x] OSRM failure → haversine fallback + warning

## Logic

- [x] Nearest-neighbor + 2-opt unit tests
- [x] Zero-duration legs fixed when distance > 500m
- [x] Walking mode only (MVP)

## Tests

- [x] `make test-backend` — 27 tests

---

**Gate status:** Passed — ready for Phase 3.
