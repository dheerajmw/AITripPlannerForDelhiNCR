# Phase 0: Foundation

**Status:** Complete  
**Code:** [`backend/`](../../../backend/), [`frontend/`](../../../frontend/) (repo root — not under `docs/`)

## Goal

Establish the split **backend** (FastAPI) + **frontend** (Next.js) monorepo, Delhi NCR geographic contract, health API, CORS, standard errors, and geo utilities.

## Deliverables

| Area | Deliverable | Location |
|------|-------------|----------|
| Backend | `GET /api/v1/health` | `backend/app/api/v1/health.py` |
| Backend | NCR bounds & enums | `backend/app/config.py` |
| Backend | Env settings (incl. Groq placeholders) | `backend/app/settings.py`, `.env.example` |
| Backend | Error model + handlers | `backend/app/models/errors.py`, `main.py` |
| Backend | Geo utils | `backend/app/utils/geo.py` |
| Backend | Tests | `backend/tests/test_health.py`, `test_geo.py` |
| Frontend | Landing + API status badge | `frontend/app/page.tsx`, `components/ApiStatusBadge.tsx` |
| Frontend | API client | `frontend/lib/api.ts` |
| Frontend | Tests | `frontend/lib/api.test.ts` |
| Root | Dev orchestration | `Makefile`, `package.json` |

## Documents in this folder

| File | Description |
|------|-------------|
| [README.md](./README.md) | This overview |
| [implementation.md](./implementation.md) | Task breakdown (0.B*, 0.F*, 0.M*) |
| [checklist.md](./checklist.md) | Phase gate — exit criteria |
| [architecture.md](./architecture.md) | Diagrams, APIs, code map |

## How to verify

```bash
make test-backend    # 7 tests
make test-frontend   # 2 tests
make dev-backend     # → curl http://localhost:8000/api/v1/health
make dev-frontend    # → http://localhost:3000 shows "API connected"
```

## Next phase

[Phase 1 — POI data layer](../phase-1-poi-data/)
