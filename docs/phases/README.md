# Implementation Phases

Every phase folder uses the **same four files**:

| File | Purpose |
|------|---------|
| [README.md](./phase-0-foundation/README.md) | Overview, status, code locations, how to verify |
| [implementation.md](./phase-0-foundation/implementation.md) | Task list (with done/planned status) |
| [checklist.md](./phase-0-foundation/checklist.md) | Phase gate — exit criteria before next phase |
| [architecture.md](./phase-0-foundation/architecture.md) | Phase-specific diagram, components, APIs |

Global specs: [../project/architecture.md](../project/architecture.md), [../project/implementationPlan.md](../project/implementationPlan.md).

Application **code** always lives at repo root (`backend/`, `frontend/`), not under `docs/phases/`.

## Phase index

| Folder | Phase | Status |
|--------|-------|--------|
| [phase-0-foundation](./phase-0-foundation/) | Backend + frontend scaffold | **Complete** |
| [phase-1-poi-data](./phase-1-poi-data/) | POI ingest & API | **Complete** |
| [phase-2-routing](./phase-2-routing/) | OSRM routing | **Complete** |
| [phase-3-planner](./phase-3-planner/) | Rule-based itinerary | Planned |
| [phase-4-groq-ai](./phase-4-groq-ai/) | Groq AI layer | Planned |
| [phase-5-frontend](./phase-5-frontend/) | Full product UI | Planned |
| [phase-6-enhancements](./phase-6-enhancements/) | Weather, Wiki, cache | Post-MVP |
