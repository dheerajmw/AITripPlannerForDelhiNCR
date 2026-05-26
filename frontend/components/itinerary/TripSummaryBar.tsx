import { Clock, IndianRupee, MapPin, Sparkles } from "lucide-react";

import type { ItineraryResponse } from "@/types/itinerary";

type Props = {
  data: ItineraryResponse;
};

export function TripSummaryBar({ data }: Props) {
  const { meta, summary } = data;
  const hours = Math.round((meta.duration_minutes / 60) * 10) / 10;
  const isAi = meta.planner_mode === "ai";

  return (
    <nav className="sticky top-16 z-40 -mx-container-mobile border-b border-outline-variant bg-surface-container-low/90 px-container-mobile py-3 backdrop-blur-md md:-mx-container-desktop md:px-container-desktop">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="flex flex-wrap items-center gap-3">
          <span className="flex items-center gap-1 rounded-full border border-secondary/20 bg-secondary/10 px-3 py-1 font-mono text-mono-xs text-secondary">
            <MapPin className="h-3.5 w-3.5" aria-hidden />
            {meta.city}
          </span>
          <div className="hidden h-4 w-px bg-outline-variant sm:block" aria-hidden />
          <div className="flex flex-wrap items-center gap-4 font-mono text-label-mono text-on-surface-variant">
            <span className="flex items-center gap-1">
              <Clock className="h-4 w-4" aria-hidden />
              {hours}h
            </span>
            <span className="flex items-center gap-1">
              <IndianRupee className="h-4 w-4" aria-hidden />
              {summary.total_cost_inr.low}–{summary.total_cost_inr.high}
            </span>
            <span>{summary.total_stops} stops</span>
          </div>
        </div>
        {isAi ? (
          <div className="flex items-center gap-2">
            <span className="ai-pulse h-2 w-2 rounded-full bg-primary" aria-hidden />
            <span className="font-mono text-label-mono text-primary">
              {meta.ai_status === "success" ? "AI Optimized" : "AI Fallback"}
            </span>
            <Sparkles className="h-4 w-4 text-primary" aria-hidden />
          </div>
        ) : null}
      </div>
    </nav>
  );
}
