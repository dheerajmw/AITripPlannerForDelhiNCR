import type { TripLocation } from "@/types/itinerary";

import { API_BASE_URL } from "./constants";

/** Delhi NCR bounding box — mirrors backend/app/config.py */
export const NCR_BOUNDS = {
  min_lat: 28.4,
  max_lat: 28.88,
  min_lon: 76.84,
  max_lon: 77.45,
} as const;

export const DEFAULT_START_LOCATION: TripLocation = {
  id: "landmark:india-gate",
  label: "India Gate",
  lat: 28.6129,
  lon: 77.2295,
  source: "landmark",
};

/** Popular quick picks (subset of backend NCR_START_LOCATIONS). */
export const POPULAR_START_LOCATIONS: TripLocation[] = [
  DEFAULT_START_LOCATION,
  {
    id: "landmark:connaught-place",
    label: "Connaught Place",
    lat: 28.6315,
    lon: 77.2167,
    source: "landmark",
  },
  {
    id: "landmark:hauz-khas",
    label: "Hauz Khas Village",
    lat: 28.5494,
    lon: 77.2001,
    source: "landmark",
  },
  {
    id: "landmark:cyber-hub",
    label: "Cyber Hub, Gurgaon",
    lat: 28.495,
    lon: 77.089,
    source: "landmark",
  },
];

export function isInNcrBounds(lat: number, lon: number): boolean {
  return (
    lat >= NCR_BOUNDS.min_lat &&
    lat <= NCR_BOUNDS.max_lat &&
    lon >= NCR_BOUNDS.min_lon &&
    lon <= NCR_BOUNDS.max_lon
  );
}

export type LocationSearchResponse = {
  query: string;
  items: TripLocation[];
};

export async function searchLocations(query: string, limit = 8): Promise<TripLocation[]> {
  const q = query.trim();
  if (q.length < 2) return [];

  const params = new URLSearchParams({ q, limit: String(limit) });
  const response = await fetch(`${API_BASE_URL}/locations/search?${params}`, {
    headers: { Accept: "application/json" },
    cache: "no-store",
  });

  if (!response.ok) {
    return [];
  }

  const data = (await response.json()) as LocationSearchResponse;
  return data.items ?? [];
}

export function sameLocation(a: TripLocation, b: TripLocation): boolean {
  return a.id === b.id || (a.label === b.label && a.lat === b.lat && a.lon === b.lon);
}
