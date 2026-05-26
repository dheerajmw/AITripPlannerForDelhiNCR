# Phase 5 — Implementation Details

**Status:** Complete

| # | Task | Status |
|---|------|--------|
| 5.1 | `types/itinerary.ts` from shared JSON schema | Done |
| 5.2 | `lib/api.ts`: `generateItinerary(body, mode?)` | Done |
| 5.3 | **Landing** `app/page.tsx` | Done |
| 5.4 | **PlanForm** `components/plan/PlanForm.tsx` | Done |
| 5.5 | Client validation (`lib/validation.ts`) | Done |
| 5.6 | Loading + debounced submit (`useTransition`, submit lock) | Done |
| 5.7 | sessionStorage handoff | Done |
| 5.8 | **ItineraryTimeline** + stop cards + travel legs | Done |
| 5.9 | **WarningsBanner** | Done |
| 5.10 | Error UI + retry | Done |
| 5.11 | **ItineraryMap** (Leaflet, dynamic import) | Done |
| 5.12 | Cost disclaimer footer | Done |
| 5.13 | Responsive dark UI (375px+) | Done |

**Note:** Stops include `lat`/`lon` from backend for map pins (small API extension).
