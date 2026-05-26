/** DTOs aligned with shared/schemas/itinerary.schema.json */

export type BudgetTier = "low" | "medium" | "high";
export type Interest = "food" | "history" | "nightlife" | "nature";
export type DurationKey = "4h" | "8h" | "1d";
export type PlannerMode = "rule" | "ai";

export type CostRangeInr = {
  low: number;
  high: number;
};

export type StartPoint = {
  lat: number;
  lon: number;
  label: string;
};

export type ItineraryGenerateBody = {
  budget: BudgetTier;
  interests: Interest[];
  duration: DurationKey;
  start_lat?: number;
  start_lon?: number;
  start_label?: string;
};

export type SavedPlanForm = ItineraryGenerateBody & {
  useAi: boolean;
};

export type ItineraryMeta = {
  city: string;
  duration_minutes: number;
  budget_tier: string;
  schema_version: string;
  start_point?: StartPoint;
  warnings: string[];
  planner_mode: string;
  routing_source?: string | null;
  ai_status?: string | null;
  fallback_reason?: string | null;
};

export type ItineraryStop = {
  order: number;
  poi_id: string;
  name: string;
  category: string;
  lat: number;
  lon: number;
  arrive_at: string;
  depart_at: string;
  visit_minutes: number;
  travel_to_next_minutes?: number | null;
  cost_estimate_inr: CostRangeInr;
  notes: string;
};

export type ItinerarySummary = {
  total_stops: number;
  total_travel_min: number;
  total_visit_min: number;
  total_cost_inr: CostRangeInr;
};

export type ItineraryResponse = {
  meta: ItineraryMeta;
  stops: ItineraryStop[];
  summary: ItinerarySummary;
};
