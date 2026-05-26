# Phase 0 — Implementation Details

Moved from the master plan so Phase 0 lives entirely under `docs/phases/phase-0-foundation/`.

**Parent:** [Implementation plan](../../project/implementationPlan.md)  
**Architecture:** [architecture.md](./architecture.md)

---

## Backend tasks (`backend/`)

| # | Task | Output | Status |
|---|------|--------|--------|
| 0.B1 | FastAPI app + `/api/v1` router | `app/main.py`, `api/v1/router.py` | Done |
| 0.B2 | `GET /api/v1/health` | `{ status, poi_count?, version }` | Done |
| 0.B3 | `config.py`: `NCR_BOUNDS`, `DEFAULT_START`, durations, enums | Single config source | Done |
| 0.B4 | Pydantic settings: DB, CORS, Groq placeholders | `backend/.env.example` | Done |
| 0.B5 | CORS: `http://localhost:3000` | Middleware | Done |
| 0.B6 | Standard error model + exception handlers | edgeCases §14 | Done |
| 0.B7 | Geo utils: `in_ncr_bounds`, `clamp_to_ncr` | `app/utils/geo.py` | Done |
| 0.B8 | `pytest` + health integration test | `tests/test_health.py` | Done |

## Frontend tasks (`frontend/`)

| # | Task | Output | Status |
|---|------|--------|--------|
| 0.F1 | Next.js (TS, Tailwind, App Router) | Runnable UI | Done |
| 0.F2 | `lib/api.ts`: `checkHealth()` | API client stub | Done |
| 0.F3 | Landing page with backend status badge | `app/page.tsx` | Done |
| 0.F4 | Shared layout + basic nav | `app/layout.tsx` | Done |
| 0.F5 | `.env.local.example` | `NEXT_PUBLIC_API_URL` only | Done |
| 0.F6 | Vitest + API client test | `lib/api.test.ts` | Done |

## Monorepo / DX (repo root)

| # | Task | Output | Status |
|---|------|--------|--------|
| 0.M1 | Root `package.json` + `pnpm-workspace.yaml` | `npm run dev` | Done |
| 0.M2 | `Makefile`: `dev`, `test`, `ingest` | Shortcuts | Done |
| 0.M3 | Root `README.md` | Dev onboarding | Done |

## Config values (backend `app/config.py`)

```python
NCR_BOUNDS = {
    "min_lat": 28.40, "max_lat": 28.88,
    "min_lon": 76.84, "max_lon": 77.45,
}
DEFAULT_START = {"lat": 28.6129, "lon": 77.2295, "label": "India Gate"}
DURATIONS_MINUTES = {"4h": 240, "8h": 480, "1d": 1440}
MAX_DURATION_MINUTES = 1440
DEFAULT_TRANSPORT_MODE = "walking"
```

## Edge cases (Phase 0 scope)

EC-G-06, EC-G-07, EC-X-10, EC-S-09 — see [edgeCases.md](../../project/edgeCases.md).

## Duration

Estimated 2–3 days (1 developer). **Completed** in initial scaffold.
