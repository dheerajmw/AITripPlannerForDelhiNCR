# Backend — FastAPI

REST API for TripPilot AI. All planner logic, POI data, routing, and Groq integration live here.

**Phase 0 docs:** [docs/phases/phase-0-foundation/](../docs/phases/phase-0-foundation/)

## Run

```bash
pip install -e ".[dev]"
uvicorn app.main:app --reload --port 8000
```

## API

- `GET /api/v1/health` — liveness
- `GET /docs` — OpenAPI UI
