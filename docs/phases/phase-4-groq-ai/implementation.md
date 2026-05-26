# Phase 4 — Implementation Details

**Status:** Complete  
**Pattern A:** Rule-based itinerary from Phase 3; Groq enriches `notes` only.

## Backend tasks

| # | Task | Status |
|---|------|--------|
| 4.1 | `GroqClient` (`groq_client.py`) | Done |
| 4.2 | `GROQ_API_KEY`, `GROQ_MODEL` in settings | Done |
| 4.3 | JSON object response format | Done |
| 4.4 | `ContextBuilder` | Done |
| 4.5 | Prompt templates | Done |
| 4.6 | `ItineraryValidator` + fallback | Done |
| 4.7 | Fallback on error/timeout/429 | Done |
| 4.8 | `?mode=ai` on generate endpoint | Done |
| 4.9 | Server-side cost/summary (unchanged from rule draft) | Done |
| 4.10 | Cap context POIs to 20 | Done |
| 4.11 | Mock Groq in tests | Done |

## Frontend tasks

| # | Task | Status |
|---|------|--------|
| 4.F1 | “Enhance with AI (Groq)” checkbox on `/plan` | Done |
| 4.F2 | Longer loading copy for AI mode | Done |
| 4.F3 | `WarningsBanner` — `meta.warnings`, fallback | Done |
