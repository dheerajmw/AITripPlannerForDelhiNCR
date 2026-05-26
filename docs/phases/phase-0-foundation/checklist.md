# Phase 0 — Exit Checklist (Phase Gate)

Do **not** start [Phase 1](../phase-1-poi-data/) until all items below pass.

## API

- [x] `curl http://localhost:8000/api/v1/health` returns `200` with `status: "ok"`
- [x] OpenAPI docs available at `http://localhost:8000/docs`
- [x] Error responses use `{ "error": { "code", "message", "details" } }`

## Frontend

- [x] `http://localhost:3000` loads landing page
- [x] API status badge shows **API connected** when backend is running
- [x] No `GROQ_API_KEY` (or any backend secret) in `frontend/` env files committed to repo

## Backend

- [x] `NCR_BOUNDS` and related constants only in `backend/app/config.py`
- [x] Geo unit tests: inside NCR, outside NCR, clamp, invalid coordinates
- [x] Health integration test passes

## Tests

- [x] `make test-backend` — 7 passed
- [x] `make test-frontend` — 2 passed

## Documentation

- [x] Phase 0 docs in `docs/phases/phase-0-foundation/`
- [x] [Repository structure](../../project/repository-structure.md) describes layout

---

**Gate status:** Passed — ready for Phase 1.
