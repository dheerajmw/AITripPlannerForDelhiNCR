# AI Trip Planner (Delhi NCR MVP)

Monorepo for a Delhi-focused, AI-assisted day trip planner. The **backend** (FastAPI) owns all business logic and Groq calls; the **frontend** (Next.js) is UI-only.

## Project structure

```
├── backend/          # Python FastAPI REST API (port 8000)
├── frontend/         # Next.js App Router UI (port 3000)
├── docs/
│   ├── project/      # Problem statement, architecture, edge cases
│   └── phases/       # Per-phase plans (Phase 0 ✅ complete)
├── shared/schemas/   # Shared JSON contracts (Phase 3+)
└── data/             # SQLite POI database (Phase 1+)
```

Full layout: [docs/project/repository-structure.md](docs/project/repository-structure.md)  
Documentation index: [docs/README.md](docs/README.md)

## Prerequisites

- Python 3.9+ (3.11+ recommended)
- Node.js 20+
- npm

## Quick start

### 1. Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
cp .env.example .env
cd ..
make dev-backend
```

Health check: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)  
OpenAPI docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### 2. Frontend

```bash
cd frontend
cp .env.local.example .env.local
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) — the landing page shows **API ready** when both apps are running.

**You need two processes:** backend on **:8000** and frontend on **:3000**.  
If the browser says **“connection failed”**, the frontend is usually not started — run `make dev-frontend` (or `make dev` for both).

```bash
./scripts/dev-check.sh   # verifies :8000, planner route, and :3000
```

### Troubleshooting “Not Found” when generating

If **Generate Itinerary** shows **Not Found**, port **8000** is almost always an **old or wrong** Python process (only `/health`, no planner routes).

```bash
lsof -i :8000          # find the PID
kill <PID>             # stop the stale server
make dev-backend       # from repo root — must use backend/ in this project
./scripts/dev-check.sh # should print OK planner + poi_count > 0
```

Health should look like: `"poi_count": 13705` (not `null`). If `poi_count` is `null`, restart the backend from this repo and run `make ingest` if the DB is missing.

### “OSRM unavailable” warning

On macOS, system Python often uses **LibreSSL**, which cannot complete TLS to the public OSRM demo over `https://`. The backend defaults to `http://router.project-osrm.org` and retries over HTTP if HTTPS fails. Restart the backend after pulling updates. Override with `OSRM_BASE_URL` in `backend/.env` if you run your own OSRM instance.

### 3. Both apps (from repo root)

```bash
make install
make dev
```

The UI calls `/api/v1` on the same host; Next.js proxies those requests to the backend on port 8000.

## Environment variables

| App | File | Key vars |
|-----|------|----------|
| Backend | `backend/.env` | `CORS_ORIGINS`, `GROQ_API_KEY` (Phase 4), `DATABASE_URL` |
| Frontend | `frontend/.env.local` | `NEXT_PUBLIC_API_URL` only |

**Never** put `GROQ_API_KEY` in the frontend.

## POI data (Phase 1)

```bash
make ingest       # Download Delhi NCR POIs from Overpass (~5 min)
make check-pois   # Verify ≥500 POIs in database
```

## Tests

```bash
make test
```

## Implementation status

| Phase | Docs | Status |
|-------|------|--------|
| 0 — Foundation | [docs/phases/phase-0-foundation](docs/phases/phase-0-foundation/) | **Complete** |
| 1 — POI data | [docs/phases/phase-1-poi-data](docs/phases/phase-1-poi-data/) | **Complete** |
| 2 — Routing | [docs/phases/phase-2-routing](docs/phases/phase-2-routing/) | **Complete** |
| 3–6 | [docs/phases/](docs/phases/) | Planned |

See [docs/project/implementationPlan.md](docs/project/implementationPlan.md) for the full roadmap.
