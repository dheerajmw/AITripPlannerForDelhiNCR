import { DEFAULT_START_LOCATION } from "@/lib/locations";
import type { ItineraryResponse, SavedPlanForm, TripLocation } from "@/types/itinerary";

export const STORAGE_KEYS = {
  itinerary: "aitp_itinerary",
  planForm: "aitp_plan_form",
} as const;

export function saveItinerary(data: ItineraryResponse): void {
  if (typeof sessionStorage === "undefined") return;
  sessionStorage.setItem(STORAGE_KEYS.itinerary, JSON.stringify(data));
}

export function loadItinerary(): ItineraryResponse | null {
  if (typeof sessionStorage === "undefined") return null;
  const raw = sessionStorage.getItem(STORAGE_KEYS.itinerary);
  if (!raw) return null;
  try {
    const data = JSON.parse(raw) as ItineraryResponse;
    if (!data?.stops || !Array.isArray(data.stops)) return null;
    return data;
  } catch {
    return null;
  }
}

export function savePlanForm(form: SavedPlanForm): void {
  if (typeof sessionStorage === "undefined") return;
  sessionStorage.setItem(STORAGE_KEYS.planForm, JSON.stringify(form));
}

export function loadPlanForm(): SavedPlanForm | null {
  if (typeof sessionStorage === "undefined") return null;
  const raw = sessionStorage.getItem(STORAGE_KEYS.planForm);
  if (!raw) return null;
  try {
    return JSON.parse(raw) as SavedPlanForm;
  } catch {
    return null;
  }
}

/** Restore start location from saved form (handles older sessions without startLocation). */
export function resolveStartLocation(saved: SavedPlanForm | null): TripLocation {
  if (saved?.startLocation?.id) {
    return saved.startLocation;
  }
  if (
    saved?.start_lat != null &&
    saved.start_lon != null &&
    saved.start_label?.trim()
  ) {
    return {
      id: `legacy:${saved.start_label}`,
      label: saved.start_label,
      lat: saved.start_lat,
      lon: saved.start_lon,
      source: "landmark",
    };
  }
  return DEFAULT_START_LOCATION;
}
