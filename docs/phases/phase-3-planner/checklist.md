# Phase 3 — Exit Checklist

Do **not** start [Phase 4](../phase-4-groq-ai/) until all items pass.

## API

- [x] `POST /api/v1/itinerary/generate` with budget + interests + duration → valid itinerary JSON
- [x] Response matches `shared/schemas/itinerary.schema.json`
- [x] Unknown preferences rejected with `400`

## Logic

- [x] Every `poi_id` in response exists in POI database
- [x] Sum(visit + travel) ≤ user time budget
- [x] Same input → same output (deterministic, `mode=rule`)
- [ ] E2E-01, E2E-02, E2E-03 from [edgeCases](../../project/edgeCases.md) (manual smoke with real DB)

## Tests

- [x] Unit tests: filter, selector, scheduler, cost
- [x] Integration test: full generate with test DB

---

**Gate status:** Complete (automated). Run E2E scenarios manually against ingested POI DB before Phase 4.
