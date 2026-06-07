import { describe, expect, it } from "vitest";

import {
  buildGoogleMapsPlaceUrl,
  buildGoogleMapsRouteUrl,
  stopGoogleMapsUrl,
} from "./googleMaps";
import type { ItineraryResponse } from "@/types/itinerary";

const sampleItinerary: ItineraryResponse = {
  meta: {
    city: "Delhi NCR",
    duration_minutes: 480,
    budget_tier: "medium",
    schema_version: "1",
    start_point: { lat: 28.6129, lon: 77.2295, label: "India Gate" },
    warnings: [],
    planner_mode: "rule",
  },
  stops: [
    {
      order: 1,
      poi_id: "a",
      name: "Red Fort",
      category: "monument",
      lat: 28.6562,
      lon: 77.241,
      arrive_at: "09:00",
      depart_at: "10:30",
      visit_minutes: 90,
      cost_estimate_inr: { low: 50, high: 200 },
      notes: "",
    },
    {
      order: 2,
      poi_id: "b",
      name: "Qutub Minar",
      category: "monument",
      lat: 28.5244,
      lon: 77.1855,
      arrive_at: "11:00",
      depart_at: "12:30",
      visit_minutes: 90,
      cost_estimate_inr: { low: 50, high: 200 },
      notes: "",
    },
  ],
  summary: {
    total_stops: 2,
    total_travel_min: 40,
    total_visit_min: 180,
    total_cost_inr: { low: 100, high: 400 },
  },
};

describe("googleMaps urls", () => {
  it("builds place url with label", () => {
    const url = buildGoogleMapsPlaceUrl({ lat: 28.6129, lon: 77.2295 }, "India Gate");
    expect(url).toContain("google.com/maps/search/");
    expect(url).toContain("India+Gate");
  });

  it("builds walking route with start and stops", () => {
    const url = buildGoogleMapsRouteUrl(sampleItinerary);
    expect(url).toContain("google.com/maps/dir/");
    expect(url).toContain("travelmode=walking");
    expect(url).toContain("28.6129%2C77.2295");
    expect(url).toContain("28.5244%2C77.1855");
  });

  it("builds per-stop url", () => {
    const url = stopGoogleMapsUrl(sampleItinerary.stops[0]);
    expect(url).toContain("Red+Fort");
  });
});
