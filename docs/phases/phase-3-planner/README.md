# Phase 3: Rule-Based Planner

**Status:** Complete  
**Code:** `backend/app/services/planner/`, `POST /api/v1/itinerary/generate`

## Goal

End-to-end **deterministic** itinerary: preferences → POIs → filter → route → schedule → cost — no LLM.

## Depends on

[Phase 2 — Routing](../phase-2-routing/)

## Documents in this folder

| File | Description |
|------|-------------|
| [README.md](./README.md) | This overview |
| [implementation.md](./implementation.md) | Task list (3.1–3.12) |
| [checklist.md](./checklist.md) | Phase gate |
| [architecture.md](./architecture.md) | Diagrams, APIs, code map |

## References

- [Project architecture](../../project/architecture.md)
- [Implementation plan §8](../../project/implementationPlan.md)

## Try it

```bash
curl -s -X POST http://localhost:8000/api/v1/itinerary/generate?mode=rule \
  -H "Content-Type: application/json" \
  -d '{"budget":"medium","interests":["history","nature"],"duration":"8h"}' | jq .
```
