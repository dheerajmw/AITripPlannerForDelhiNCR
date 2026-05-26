# Phase 1 — Exit Checklist

## API

- [x] `GET /api/v1/pois?category=attraction` returns ≥20 results with `id`, `name`, `lat`, `lon`
- [x] `GET /api/v1/pois?interest=food` returns restaurants/cafes
- [x] Unknown category → `400 VALIDATION_ERROR`
- [x] `/api/v1/health` reports `poi_count > 0`

## Data

- [x] `make ingest` idempotent (upsert by `id`)
- [x] `make check-pois` passes (≥500 total POIs)
- [x] POIs stored in `data/pois.db` (gitignored)

## Tests

- [x] `make test-backend` — normalizer, API, ingest fixture tests

---

**Gate status:** Passed — ready for Phase 2.
