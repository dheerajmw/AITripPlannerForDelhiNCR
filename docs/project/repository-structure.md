# Repository Structure

Canonical layout for the TripPilot AI monorepo. Phase-specific details and checklists live under [`docs/phases/`](../phases/).

```
AITripPlanner/
│
├── backend/                    # Python FastAPI — all API & business logic
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py           # Delhi NCR constants (Phase 0)
│   │   ├── settings.py
│   │   ├── api/v1/             # REST routes
│   │   ├── models/
│   │   ├── services/           # POI, routing, planner, Groq (later phases)
│   │   └── utils/geo.py
│   ├── scripts/                # ingest_pois.py (Phase 1+)
│   ├── tests/
│   ├── pyproject.toml
│   └── .env.example
│
├── frontend/                   # Next.js — UI only, no secrets
│   ├── app/                    # App Router pages
│   ├── components/
│   ├── lib/api.ts              # Backend HTTP client
│   ├── package.json
│   └── .env.local.example
│
├── shared/schemas/             # JSON Schema contracts (Phase 3+)
├── data/                       # SQLite POI DB (gitignored, Phase 1+)
│
├── docs/                       # All documentation
│   ├── project/                # Global specs
│   └── phases/                 # Per-phase docs (4 files each — see phases/README.md)
│       ├── phase-0-foundation/ # README, implementation, checklist, architecture
│       ├── phase-1-poi-data/
│       ├── phase-2-routing/
│       └── phase-3 … phase-6/
│
├── Makefile                    # dev, test, ingest
├── package.json                # Root scripts (concurrently)
├── pnpm-workspace.yaml
└── README.md                   # Quick start
```

## Rules

1. **Do not put application code under `docs/`** — only markdown and phase artifacts.
2. **One phase folder per milestone** under `docs/phases/` — see [phases README](../phases/README.md).
3. **Groq keys** only in `backend/.env`, never in `frontend/`.
4. **Shared API contract** in `shared/schemas/` once Phase 3 freezes the itinerary JSON schema.

## Phase → code mapping

| Phase | Primary code locations | Phase docs |
|-------|------------------------|------------|
| 0 | `backend/app/*`, `frontend/*`, root `Makefile` | [phase-0-foundation](../phases/phase-0-foundation/) |
| 1 | `backend/scripts/`, `backend/app/db/`, `GET /pois` | [phase-1-poi-data](../phases/phase-1-poi-data/) |
| 2 | `backend/app/services/routing_*` | [phase-2-routing](../phases/phase-2-routing/) |
| 3 | `backend/app/services/planner/` | [phase-3-planner](../phases/phase-3-planner/) |
| 4 | `backend/app/services/ai/groq_client.py` | [phase-4-groq-ai](../phases/phase-4-groq-ai/) |
| 5 | `frontend/app/plan`, `frontend/app/itinerary` | [phase-5-frontend](../phases/phase-5-frontend/) |
| 6 | Weather, Wikipedia, caching | [phase-6-enhancements](../phases/phase-6-enhancements/) |
