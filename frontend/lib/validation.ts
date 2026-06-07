import { isInNcrBounds } from "@/lib/locations";
import type {
  BudgetTier,
  DurationKey,
  Interest,
  ItineraryGenerateBody,
  TripLocation,
} from "@/types/itinerary";

const BUDGETS: BudgetTier[] = ["low", "medium", "high"];
const DURATIONS: DurationKey[] = ["4h", "8h", "1d"];
const INTERESTS: Interest[] = ["food", "history", "nightlife", "nature"];

export type PlanFormValidationResult =
  | { ok: true; value: ItineraryGenerateBody }
  | { ok: false; message: string };

export function validatePlanForm(input: {
  budget: string;
  interests: string[];
  duration: string;
  location: TripLocation | null;
}): PlanFormValidationResult {
  if (!BUDGETS.includes(input.budget as BudgetTier)) {
    return { ok: false, message: "Please select a valid budget." };
  }

  if (!DURATIONS.includes(input.duration as DurationKey)) {
    return { ok: false, message: "Please select a valid duration." };
  }

  const interests = input.interests.filter((i): i is Interest =>
    INTERESTS.includes(i as Interest),
  );

  if (interests.length === 0) {
    return { ok: false, message: "Select at least one interest." };
  }

  const unique = [...new Set(interests)];

  const loc = input.location;
  if (!loc?.id || !loc.label.trim()) {
    return {
      ok: false,
      message: "Select a starting location from the Delhi NCR list.",
    };
  }
  if (!isInNcrBounds(loc.lat, loc.lon)) {
    return {
      ok: false,
      message: "That location is outside Delhi NCR. Choose a place from the suggestions.",
    };
  }

  return {
    ok: true,
    value: {
      budget: input.budget as BudgetTier,
      interests: unique,
      duration: input.duration as DurationKey,
      start_lat: loc.lat,
      start_lon: loc.lon,
      start_label: loc.label,
    },
  };
}
