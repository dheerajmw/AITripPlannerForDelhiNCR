# Phase 4 — Exit Checklist

## Security

- [x] Groq called only from backend (`grep GROQ` in `frontend/` → no env usage)
- [x] `GROQ_API_KEY` in `backend/.env` only

## API

- [x] `POST /api/v1/itinerary/generate?mode=ai`
- [x] Fallback to rule-based draft on error / missing key
- [x] `meta.ai_status`, `meta.fallback_reason`

## Tests

- [x] Mock Groq in `backend/tests/test_groq_planner.py`
- [x] Invalid `poi_id` → fallback
- [x] Timeout → fallback
- [x] Notes enrichment success path

## Manual

- [ ] Live Groq call with real `GROQ_API_KEY` (optional smoke)

---

**Gate status:** Complete (automated).
