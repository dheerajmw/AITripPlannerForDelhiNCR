# Frontend UI — Stitch / AI Prompt Guide

Use this document to generate or refine the **AI Trip Planner** frontend in **Next.js 15 + TypeScript + Tailwind**. Paste sections into [Stitch](https://stitch.withgoogle.com), Cursor, v0, or any UI agent.

**Sources of truth:** [architecture.md](./project/architecture.md) (Phase 5), [implementationPlan.md](./project/implementationPlan.md) (§10), [itinerary.schema.json](../shared/schemas/itinerary.schema.json).

**Scope:** Delhi NCR day-trip MVP. **Dark theme only** (no light mode in MVP). No planner logic in the browser — only `fetch` to `backend/`.

---

## 1. Project context (paste first)

```
Product: AI Trip Planner — Delhi NCR day/half-day itineraries from real OpenStreetMap POIs.

Stack:
- frontend/ — Next.js 15 App Router, React 19, TypeScript, Tailwind CSS 3.4
- backend/ — FastAPI at NEXT_PUBLIC_API_URL (default http://localhost:8000/api/v1)
- Maps: Leaflet + OSM tiles (client-only, dynamic import, no SSR for map)
- NO secrets in frontend. NO Groq calls. AI = query param mode=ai only.

User flow (< 3 minutes):
  Landing (/) → Plan form (/plan) → POST generate → Itinerary (/itinerary)

API:
  GET  /health
  POST /itinerary/generate?mode=rule|ai
  Body: { budget, interests[], duration, start_lat?, start_lon?, start_label? }
  Errors: { error: { code, message, details? } }

Interests: food | history | nightlife | nature
Budget: low | medium | high
Duration: 4h | 8h | 1d

Existing partial UI (upgrade, don't rewrite blindly):
  app/page.tsx, app/plan/page.tsx, app/itinerary/page.tsx
  lib/api.ts (checkHealth, generateItinerary)
  components/WarningsBanner.tsx (basic — move to components/itinerary/)
```

---

## 2. Dark theme design system (required)

Force **dark mode always** — do not rely on `prefers-color-scheme`. Set `class="dark"` on `<html>` in `app/layout.tsx`.

### 2.1 Color tokens (Tailwind + CSS variables in `globals.css`)

| Token | Hex | Usage |
|-------|-----|--------|
| `bg-base` | `#0B0F14` | Page background (deep blue-black) |
| `bg-surface` | `#12181F` | Cards, panels |
| `bg-elevated` | `#1A222C` | Hover, inputs |
| `border-subtle` | `#2A3441` | Borders |
| `text-primary` | `#F4F7FB` | Headings, body |
| `text-muted` | `#9AA8B8` | Secondary copy |
| `accent` | `#FF6B35` | Primary CTA, Delhi warmth (saffron-orange) |
| `accent-glow` | `#FF6B3540` | Button glow / focus ring |
| `success` | `#3DD68C` | API healthy badge |
| `warning` | `#F5C542` | Warnings banner |
| `error` | `#FF5C6C` | Form/API errors |
| `travel-line` | `#4ECDC4` | Timeline connector / map route |

### 2.2 Typography

- **Display:** `Geist` or `DM Sans` — bold, tight tracking on H1
- **Body:** `Geist` or `Inter` — 15–16px, line-height 1.6
- **Mono:** times `09:15`, costs — `Geist Mono` or `JetBrains Mono`

### 2.3 Visual style

- **Mood:** Modern travel app — glassmorphism-lite (subtle `backdrop-blur` on header), soft gradients (`bg-gradient-to-br from-[#0B0F14] via-[#12181F] to-[#0f1419]`)
- **Cards:** `rounded-2xl`, `border border-[#2A3441]`, faint inner shadow, hover `border-accent/30`
- **Buttons:** Primary = filled accent with glow on hover; secondary = outline on `bg-elevated`
- **Chips** (interests/budget): pill toggles — selected = accent border + `bg-accent/10`
- **Motion:** `transition-all duration-200`; stagger fade-in on itinerary stops (optional `framer-motion` if added)
- **Icons:** Lucide React (install `lucide-react`) — map-pin, clock, wallet, sparkles for AI

### 2.4 Layout

- Max width `max-w-3xl` centered (mobile-first)
- Min touch target 44px
- Sticky top: compact header + optional trip summary bar on `/itinerary`
- Safe area padding `px-4 pb-8`

---

## 3. Target file structure

```
frontend/
├── app/
│   ├── layout.tsx          # dark html, header nav, gradient bg
│   ├── page.tsx            # Landing
│   ├── plan/page.tsx       # thin page → <PlanForm />
│   ├── itinerary/page.tsx  # thin page → timeline + map + summary
│   └── globals.css         # CSS variables + dark base
├── components/
│   ├── layout/
│   │   ├── SiteHeader.tsx
│   │   └── ApiStatusBadge.tsx   # move from components/ if exists
│   ├── plan/
│   │   └── PlanForm.tsx
│   └── itinerary/
│       ├── ItineraryTimeline.tsx
│       ├── ItineraryStopCard.tsx
│       ├── TravelLeg.tsx
│       ├── TripSummaryBar.tsx
│       ├── WarningsBanner.tsx
│       ├── ItineraryMap.tsx
│       ├── CostDisclaimer.tsx
│       └── EmptyItineraryError.tsx
├── lib/
│   ├── api.ts
│   ├── constants.ts
│   └── validation.ts       # client-side EC-U-01, EC-U-05, EC-U-06
├── types/
│   └── itinerary.ts        # mirror shared/schemas/itinerary.schema.json
└── hooks/
    └── usePlanForm.ts      # optional: form state + sessionStorage prefill
```

---

## 4. Master Stitch prompt (full UI pass)

Copy everything inside the block:

```markdown
Build a complete dark-theme Next.js 15 App Router UI for "AI Trip Planner" (Delhi NCR).

DESIGN: Modern, cool dark UI. Background #0B0F14, surfaces #12181F, accent #FF6B35 (saffron-orange), teal #4ECDC4 for travel connectors. Glass header, rounded-2xl cards, subtle gradients. Use Tailwind only (no CSS modules). Install lucide-react for icons.

CONSTRAINTS:
- TypeScript strict. Client components only where needed (forms, map, sessionStorage).
- Never import or reference GROQ_API_KEY. Call backend via lib/api.ts fetch only.
- Escape POI names when rendering (React text nodes are fine; no dangerouslySetInnerHTML).
- Mobile-first 375px+, no horizontal scroll.

PAGES:

1) LANDING (app/page.tsx)
- Hero: "Plan your Delhi NCR day in minutes"
- Subcopy: real OSM places, walking routes, optional AI tips (server-side Groq)
- ApiStatusBadge: green dot if GET /health ok, show poi_count
- Primary CTA → /plan
- Secondary: 3 feature pills (Real places | Walking times | AI tips optional)

2) PLAN (app/plan/page.tsx + components/plan/PlanForm.tsx)
- PlanForm controlled fields:
  - Budget: low | medium | high (radio pill group)
  - Interests: food, history, nature, nightlife (multi-select chips, min 1)
  - Duration: 4h | 8h | 1d
  - Checkbox: "Enhance with AI (Groq)" → passes mode=ai to generateItinerary
- Client validation before submit (validation.ts):
  - At least one interest
  - Valid budget/duration enums
- Submit: useTransition, disabled while pending
- Loading copy: rule = "Building your itinerary…"; ai = "Generating with AI tips (5–20s)…"
- On success: sessionStorage key `aitp_itinerary` + `aitp_plan_form` → router.push('/itinerary')
- On error: inline alert with error.message + Retry (preserve form)
- Debounce double-submit (EC-U-17)

3) ITINERARY (app/itinerary/page.tsx)
- Load JSON from sessionStorage; if missing → EmptyItineraryError + link /plan
- If stops.length === 0 → treat as error (EC-UI-03)
- Layout order:
  a) TripSummaryBar (sticky): city, duration, budget, stop count, ₹ low–high total
  b) WarningsBanner: meta.warnings + ai_status fallback message (amber dark style)
  c) ItineraryMap (Leaflet, dynamic import ssr:false) — pins per stop + polyline; if tiles fail, hide map (EC-UI-05)
  d) ItineraryTimeline: ordered stops with ItineraryStopCard + TravelLeg between
  e) CostDisclaimer footer: estimates not actual prices (EC-C-06)
  f) Actions: "Plan another day" → /plan; "Regenerate" re-posts last form from sessionStorage

COMPONENTS:

ItineraryStopCard:
- order badge, name (truncate long), category chip, arrive_at–depart_at, visit_minutes
- cost_estimate_inr low–high in ₹
- notes block (italic muted) when non-empty — AI tips

TravelLeg:
- icon walk + "{travel_to_next_minutes} min walk to next stop"
- vertical line accent teal

ItineraryMap:
- react-leaflet + leaflet CSS
- Center Delhi ~28.61, 77.23; OSM tile layer
- Markers numbered 1..n; polyline through stops; include start_point from meta if present

SiteHeader:
- Logo text APP_NAME, links Home + Plan, dark glass border-b

Update app/layout.tsx: className dark on html, gradient body, SiteHeader, main slot.

Add types/itinerary.ts matching shared schema (meta.ai_status, meta.fallback_reason included).

Keep lib/api.ts generateItinerary(body, mode) and checkHealth().

Do not add share/export buttons (EC-UI-06). No broken features.
```

---

## 5. Per-screen prompts (Stitch iterations)

### 5.1 Landing only

```
Dark landing page for AI Trip Planner, Delhi NCR. Next.js + Tailwind.
Hero with gradient mesh background (#0B0F14 → #1a1f2e). Large headline, muted subtext.
Orange CTA button "Start planning" → /plan.
Small API status pill (connected / offline) using fetch /health.
Three icon cards: Real OSM venues, Optimized walking route, Optional AI tips.
Footer line: "Estimates only · MVP". No light theme.
```

### 5.2 Plan form only

```
Dark onboarding form component PlanForm.tsx for a trip planner.
Fields: budget pills (low/medium/high), interest multi-chips (food/history/nature/nightlife),
duration radios (4h/8h/full day), AI enhancement toggle with sparkles icon and helper text.
Validate at least one interest. Submit button full-width accent #FF6B35.
Loading states for rule vs AI mode. Error banner rose/red on API failure with retry.
Store form in sessionStorage on success. Modern, minimal, 375px mobile.
```

### 5.3 Itinerary results only

```
Dark itinerary results view. Timeline vertical list with numbered stops.
Each card: time range, POI name, category tag, visit duration, INR cost range, AI notes paragraph.
Teal connector lines between stops showing walk minutes.
Sticky summary bar at top: 4 stops · 120 min travel · ₹500–1200.
Amber warnings banner for meta.warnings and AI fallback.
Leaflet map section above timeline (dark UI chrome, OSM tiles).
Bottom disclaimer: costs are estimates. Buttons: Regenerate, Plan another day.
```

---

## 6. Per-component micro-prompts

| Component | Prompt snippet |
|-----------|----------------|
| `ApiStatusBadge` | Small pill: pulsing green dot + "API ready · {poi_count} places" or red offline. Dark surface background. |
| `WarningsBanner` | Amber/dark banner, list of warning strings, show fallback_reason when ai_status=fallback. Dismiss optional. |
| `TripSummaryBar` | Sticky top bar, blur backdrop, icons for clock/wallet/map-pin, compact stats from itinerary.summary + meta. |
| `ItineraryStopCard` | Dark card `bg-surface`, left order circle accent-filled, right content stack, monospace times. |
| `TravelLeg` | Narrow row between cards, dashed teal line, walking icon, minutes label. |
| `ItineraryMap` | Leaflet container h-64 rounded-2xl border; numbered divIcons; fitBounds all points. |
| `CostDisclaimer` | `text-xs text-muted` centered: "Cost ranges are estimates, not bookings or tickets." |
| `EmptyItineraryError` | Centered empty state illustration placeholder, CTA to /plan. |

---

## 7. API & types reference (for codegen)

### Request `ItineraryGenerateBody`

```ts
{
  budget: "low" | "medium" | "high";
  interests: ("food" | "history" | "nightlife" | "nature")[];
  duration: "4h" | "8h" | "1d";
  start_lat?: number;
  start_lon?: number;
  start_label?: string;
}
```

### Response highlights

```ts
meta: {
  city: string;
  duration_minutes: number;
  budget_tier: string;
  schema_version: string;
  start_point?: { lat: number; lon: number; label: string };
  warnings: string[];
  planner_mode: "rule" | "ai";
  routing_source?: string;
  ai_status?: "success" | "fallback";
  fallback_reason?: string;
}
stops: Array<{
  order: number;
  poi_id: string;
  name: string;
  category: string;
  arrive_at: string;  // HH:mm
  depart_at: string;
  visit_minutes: number;
  travel_to_next_minutes?: number | null;
  cost_estimate_inr: { low: number; high: number };
  notes: string;
}>
summary: {
  total_stops: number;
  total_travel_min: number;
  total_visit_min: number;
  total_cost_inr: { low: number; high: number };
}
```

### sessionStorage keys

| Key | Content |
|-----|---------|
| `aitp_itinerary` | Full `ItineraryResponse` JSON |
| `aitp_plan_form` | Last submit body + `useAi: boolean` for regenerate |

---

## 8. Edge cases to implement (from edgeCases.md)

| ID | UI behavior |
|----|-------------|
| EC-UI-01 | API error screen inline on `/plan`; keep form values; Retry button |
| EC-UI-02 | Loading >10s: show "Still working…" subtext after 10s |
| EC-UI-03 | `stops.length === 0` → error state, not blank timeline |
| EC-UI-05 | Map tile error → hide map, show "Map unavailable" once |
| EC-UI-07 | Browser back to `/plan` → prefill from `aitp_plan_form` |
| EC-UI-08 | `navigator.onLine === false` → banner before submit |
| EC-UI-10 | Test 320–375px width, no overflow on long POI names |
| EC-UI-11 | Always render `WarningsBanner` when warnings.length > 0 or fallback |
| EC-UI-12 | Regenerate replaces entire itinerary state + remount map |

---

## 9. Dependencies to add (prompt agent)

```bash
cd frontend
npm install lucide-react leaflet react-leaflet
npm install -D @types/leaflet
```

Map component pattern:

```tsx
"use client";
import dynamic from "next/dynamic";
const ItineraryMap = dynamic(() => import("@/components/itinerary/ItineraryMap"), { ssr: false });
```

---

## 10. Acceptance checklist (Phase 5 gate)

- [ ] Landing → Plan → Itinerary flow works against `make dev-backend`
- [ ] `mode=rule` works without Groq key
- [ ] `mode=ai` shows longer loading + notes when key configured
- [ ] `meta.warnings` and AI fallback visible
- [ ] Map shows stop order (or degrades gracefully)
- [ ] No `GROQ` in `frontend/` env except docs/comments
- [ ] Responsive 375px+
- [ ] Vitest: `validation.ts` unit tests for form rules

---

## 11. Suggested Stitch workflow

1. Paste **§1 Project context** + **§2 Design system** into a new Stitch project.
2. Generate **Layout + Landing** (§5.1).
3. Generate **PlanForm** (§5.2) → integrate into repo `components/plan/`.
4. Generate **Itinerary view** (§5.3) → split into timeline/map/banner components.
5. Run app locally; paste component screenshots back into Stitch for polish pass: "tighten spacing, increase contrast on muted text, add hover states."
6. Export/copy Tailwind code into `frontend/`; align imports with `@/` paths.

---

## 12. Related docs

- [architecture.md § Phase 5](./project/architecture.md)
- [implementationPlan.md § 10](./project/implementationPlan.md)
- [edgeCases.md § UI](./project/edgeCases.md)
- [phase-5 frontend checklist](../phases/phase-5-frontend/) (if present)
