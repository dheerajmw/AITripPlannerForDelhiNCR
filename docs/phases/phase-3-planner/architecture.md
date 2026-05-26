# Phase 3 — Architecture

Excerpt from [project architecture](../../project/architecture.md).

## Goal

Ship end-to-end itinerary generation using **deterministic** logic (no LLM).

## Sequence

```mermaid
sequenceDiagram
    participant FE as frontend
    participant API as Planner API
    participant POI as POI Service
    participant F as Filter
    participant R as Route Optimizer
    participant S as Schedule Builder

    FE->>API: POST preferences
    API->>POI: candidates by interests
    API->>F: filter + budget
    API->>R: optimize order
    API->>S: time slots + cost
    API-->>FE: itinerary JSON
```

## Components (planned)

| Component | Path |
|-----------|------|
| Filter | `backend/app/services/planner/filter.py` |
| Selector | `backend/app/services/planner/selector.py` |
| Scheduler | `backend/app/services/planner/scheduler.py` |
| Cost | `backend/app/services/planner/cost.py` |
| Orchestrator | `backend/app/services/planner/orchestrator.py` |
| API | `backend/app/api/v1/itinerary.py` |
| Schema | `shared/schemas/itinerary.schema.json` |

## API

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/api/v1/itinerary/generate` | Full plan (`mode=rule` default) |
