import type { ItineraryResponse, ItineraryStop, StartPoint } from "@/types/itinerary";

type LatLon = { lat: number; lon: number };

const GOOGLE_MAPS_WAYPOINT_LIMIT = 9;

function coord(point: LatLon): string {
  return `${point.lat},${point.lon}`;
}

/** Open a single place in Google Maps (app or web). */
export function buildGoogleMapsPlaceUrl(point: LatLon, label?: string): string {
  const params = new URLSearchParams({ api: "1" });
  if (label?.trim()) {
    params.set("query", `${label.trim()}@${coord(point)}`);
  } else {
    params.set("query", coord(point));
  }
  return `https://www.google.com/maps/search/?${params}`;
}

/** Walking directions for the full itinerary (start → stops → end). */
export function buildGoogleMapsRouteUrl(data: ItineraryResponse): string | null {
  const points: LatLon[] = [];
  if (data.meta.start_point) {
    points.push(data.meta.start_point);
  }
  for (const stop of data.stops) {
    if (Number.isFinite(stop.lat) && Number.isFinite(stop.lon)) {
      points.push({ lat: stop.lat, lon: stop.lon });
    }
  }
  if (points.length === 0) return null;
  if (points.length === 1) {
    const only = points[0];
    const label =
      data.meta.start_point?.label ?? data.stops[0]?.name;
    return buildGoogleMapsPlaceUrl(only, label);
  }

  const origin = points[0];
  const destination = points[points.length - 1];
  const middle = points.slice(1, -1).slice(0, GOOGLE_MAPS_WAYPOINT_LIMIT);

  const params = new URLSearchParams({
    api: "1",
    origin: coord(origin),
    destination: coord(destination),
    travelmode: "walking",
  });
  if (middle.length > 0) {
    params.set("waypoints", middle.map(coord).join("|"));
  }
  return `https://www.google.com/maps/dir/?${params}`;
}

export function collectRoutePoints(data: ItineraryResponse): LatLon[] {
  const points: LatLon[] = [];
  if (data.meta.start_point) {
    points.push(data.meta.start_point);
  }
  for (const stop of data.stops) {
    if (Number.isFinite(stop.lat) && Number.isFinite(stop.lon)) {
      points.push({ lat: stop.lat, lon: stop.lon });
    }
  }
  return points;
}

export function stopGoogleMapsUrl(stop: ItineraryStop): string {
  return buildGoogleMapsPlaceUrl({ lat: stop.lat, lon: stop.lon }, stop.name);
}

export function startPointGoogleMapsUrl(start: StartPoint): string {
  return buildGoogleMapsPlaceUrl(start, start.label);
}

export const GOOGLE_MAPS_API_KEY =
  process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY?.trim() ?? "";

export function hasGoogleMapsApiKey(): boolean {
  return GOOGLE_MAPS_API_KEY.length > 0;
}
