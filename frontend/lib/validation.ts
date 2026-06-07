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

function isValidPlanDate(value: string | undefined): boolean {
  if (!value?.trim()) return true;
  if (!/^\d{4}-\d{2}-\d{2}$/.test(value)) return false;
  const parsed = new Date(`${value}T12:00:00`);
  return !Number.isNaN(parsed.getTime());
}

export function validatePlanForm(input: {
  budget: string;
  interests: string[];
  duration: string;
  location: TripLocation | null;
  planDate?: string;
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

  const planDate = input.planDate?.trim();
  if (planDate && !isValidPlanDate(planDate)) {
    return { ok: false, message: "Please enter a valid trip date (YYYY-MM-DD)." };
  }

  const body: ItineraryGenerateBody = {
    budget: input.budget as BudgetTier,
    interests: unique,
    duration: input.duration as DurationKey,
    start_lat: loc.lat,
    start_lon: loc.lon,
    start_label: loc.label,
  };
  if (planDate) {
    body.plan_date = planDate;
  }

  return { ok: true, value: body };
}
