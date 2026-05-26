# Phase 4: AI Layer (Groq)

**Status:** Complete  
**Code:** `backend/app/services/ai/`, `POST /api/v1/itinerary/generate?mode=ai`

## Goal

Groq enriches per-stop **notes** on a Phase 3 draft itinerary. Order, times, and costs stay server-controlled.

## Try it

Set `GROQ_API_KEY` in `backend/.env`, then:

```bash
curl -s -X POST "http://localhost:8000/api/v1/itinerary/generate?mode=ai" \
  -H "Content-Type: application/json" \
  -d '{"budget":"medium","interests":["history","nature"],"duration":"8h"}' | jq .
```

Or use the UI: **Plan** → enable **Enhance with AI (Groq)**.

## References

- [Project architecture § Phase 4](../../project/architecture.md)
- [Implementation plan §9](../../project/implementationPlan.md)
