# Problem Statement: TripPilot AI (Delhi-Focused MVP)

## Overview

Planning a trip within a dense urban area like Delhi is fragmented and time-consuming. Travelers jump between apps to discover places, read reviews, estimate travel time, and stitch together a workable schedule. The result is poor decisions, wasted time, and little personalization.

Most existing travel tools are either too generic (built for multi-city or international trips) or too manual (lists and bookmarks without optimization). Neither fits the need for **fast, personalized, single-city itineraries** grounded in real-world constraints.

This project proposes a **lightweight, AI-assisted trip planner** focused on Delhi NCR. It will generate personalized day or half-day itineraries from user preferences—budget, interests, and available time—while respecting feasibility constraints such as distance, travel time, and venue opening hours.

**Primary goal:** reduce trip planning from hours to minutes by combining structured, free/open data sources with an AI reasoning layer.

---

## Problem

| Pain point | Impact |
|------------|--------|
| Fragmented discovery | Users switch across maps, review sites, and notes |
| No unified optimization | Routes and time slots are guessed, not computed |
| Weak personalization | Generic lists ignore budget, interests, and time budget |
| High planning effort | A solid half-day or day plan can take hours to assemble |

---

## Proposed Solution

An MVP that:

1. Collects user preferences through a simple onboarding flow.
2. Retrieves relevant points of interest (POIs) from open geographic data.
3. Filters and ranks candidates by preferences and constraints.
4. Optimizes visit order using routing/travel-time APIs.
5. Produces a **structured itinerary**: time slots, travel legs, and rough cost estimates.

The **AI layer** is the product differentiator: an LLM-based planner that orchestrates retrieval, filtering, routing, and narrative output—not a static template generator.

---

## MVP Scope (Intentional Constraints)

To keep the first version buildable and shippable:

| Dimension | Constraint |
|-----------|------------|
| **Geography** | Delhi NCR only |
| **Trip type** | Day trips and half-day itineraries |
| **Out of scope (v1)** | Flights, hotels, multi-day lodging (avoids cost-heavy APIs) |
| **Data policy** | Free-tier or open data sources only |

---

## Data Sources (MVP)

### 1. Places & attractions (core dataset)

**OpenStreetMap (OSM) via Overpass API** — free, open, no API cost.

- POI types: cafés, monuments, parks, museums, and similar venues.
- Serves as the primary **Delhi knowledge base** for the MVP.

- API: [Overpass API](https://overpass-api.de/)

### 2. Maps, distance, and routing

Choose one (or primary + fallback):

| Option | Role | Link |
|--------|------|------|
| **OSRM** (Open Source Routing Machine) | Travel time, route optimization (walking/driving) | [project-osrm.org](http://project-osrm.org/) |
| **OpenRouteService** | Alternative with a free tier | [openrouteservice.org](https://openrouteservice.org/) |

### 3. Weather (itinerary adjustments)

**OpenWeatherMap** (free tier) — inform outdoor vs. indoor weighting or schedule tweaks.

- [OpenWeatherMap API](https://openweathermap.org/api)

### 4. Optional: reviews and popularity signals

| Source | Use |
|--------|-----|
| **Wikipedia API** | Famous places, historical context (free) |
| **Google Places** | Limited free tier; consider post-MVP only |

### 5. User inputs (no external cost)

Collected at onboarding:

- Budget
- Interests (e.g. food, history, nightlife, nature)
- Time available (e.g. 4h, 8h, full day)

---

## AI Layer (Product Differentiator)

An LLM-based planner that:

1. **Retrieves** relevant POIs from OpenStreetMap (via Overpass).
2. **Filters** by user preferences and hard constraints (hours, budget band).
3. **Optimizes** visit sequence using distance/routing APIs.
4. **Generates** a structured itinerary: time blocks, travel time between stops, and estimated cost.

The model reasons over structured data—not hallucinated venues—so outputs stay tied to real places and feasible routes.

---

## Success Criteria (MVP)

- User can go from preferences → usable itinerary in **under a few minutes**.
- Itinerary respects **time budget** and includes **realistic travel legs**.
- All core POI and routing data comes from **documented free/open sources**.
- Geography and trip length stay within **Delhi NCR day/half-day** scope.

---

## Out of Scope (Post-MVP)

- Multi-city or international trip planning
- Flight and hotel booking integrations
- Paid or premium-only data APIs as hard dependencies
- Full review/rating aggregation beyond lightweight signals (e.g. Wikipedia)
