# Documentation — TripPilot AI

All project documentation lives under `docs/`. **Application code** stays at the repo root (`backend/`, `frontend/`).

## Layout

```
docs/
├── README.md                 ← you are here
├── project/                  # Cross-cutting specs (all phases)
│   ├── problemStatement.md
│   ├── architecture.md
│   ├── implementationPlan.md
│   ├── edgeCases.md
│   └── repository-structure.md
└── phases/                   # Per-phase: README + implementation + checklist + architecture
    ├── README.md             # Index + 4-file standard
    ├── phase-0-foundation/   # ✅ Complete (all 4 files)
    ├── phase-1-poi-data/       # ✅ Complete (all 4 files)
    ├── phase-2-routing/        # ✅ Complete (all 4 files)
    ├── phase-3-planner/        # Planned (all 4 files, tasks TBD)
    ├── phase-4-groq-ai/
    ├── phase-5-frontend/
    └── phase-6-enhancements/
```

## Quick links

| Document | Purpose |
|----------|---------|
| [Problem statement](./project/problemStatement.md) | Product scope and MVP constraints |
| [Architecture](./project/architecture.md) | System design, stack, API contract |
| [Implementation plan](./project/implementationPlan.md) | Timeline and phase index |
| [Edge cases](./project/edgeCases.md) | QA catalog |
| [Repository structure](./project/repository-structure.md) | Where code and docs live |
| [Phase 0 — Foundation](./phases/phase-0-foundation/README.md) | Completed scaffold (backend + frontend) |

## Phase status

| Phase | Folder | Status |
|-------|--------|--------|
| 0 | [phase-0-foundation](./phases/phase-0-foundation/) | **Complete** |
| 1 | [phase-1-poi-data](./phases/phase-1-poi-data/) | **Complete** |
| 2 | [phase-2-routing](./phases/phase-2-routing/) | **Complete** |
| 3 | [phase-3-planner](./phases/phase-3-planner/) | Planned |
| 4 | [phase-4-groq-ai](./phases/phase-4-groq-ai/) | Planned |
| 5 | [phase-5-frontend](./phases/phase-5-frontend/) | Planned |
| 6 | [phase-6-enhancements](./phases/phase-6-enhancements/) | Post-MVP |
