import { Clock, Footprints, IndianRupee, MapPin, Sparkles } from "lucide-react";

import type { ItineraryResponse } from "@/types/itinerary";

type Props = {
  data: ItineraryResponse;
};

export function ExpeditionHero({ data }: Props) {
  const { meta, summary } = data;
  const hours = Math.round((meta.duration_minutes / 60) * 10) / 10;
  const cost = summary.total_cost_inr;
  const isAi = meta.planner_mode === "ai";
  const startLabel = meta.start_point?.label ?? meta.city;

  const metrics = [
    { icon: Clock, label: "Duration", value: `${hours}h` },
    { icon: IndianRupee, label: "Est. cost", value: `₹${cost.low.toLocaleString()}–${cost.high.toLocaleString()}` },
    { icon: Sparkles, label: "Stops", value: String(summary.total_stops) },
    { icon: Footprints, label: "Walking", value: `${summary.total_travel_min} min` },
  ] as const;

  return (
    <section className="expedition-hero glass-panel mb-xl rounded-3xl p-6 md:p-8">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <span className="expedition-location-pill inline-flex items-center gap-2">
          <MapPin className="h-4 w-4 shrink-0 text-secondary" aria-hidden />
          {startLabel}
        </span>
        {isAi ? (
          <span className="expedition-ai-pill inline-flex items-center gap-1.5">
            <Sparkles className="h-3.5 w-3.5" aria-hidden />
            {meta.ai_status === "success" ? "AI enhanced" : "AI fallback"}
          </span>
        ) : null}
      </div>

      <h1 className="expedition-title mt-5 text-center text-display-lg-mobile font-extrabold md:text-display-lg">
        Your expedition
      </h1>

      <div className="expedition-metrics mt-6 grid grid-cols-2 gap-3 md:grid-cols-4 md:gap-4">
        {metrics.map(({ icon: Icon, label, value }) => (
          <div key={label} className="expedition-metric text-center">
            <Icon className="mx-auto mb-2 h-5 w-5 text-primary" aria-hidden />
            <p className="expedition-metric-value text-headline-md font-bold text-on-surface">{value}</p>
            <p className="expedition-metric-label mt-0.5 text-caption font-semibold uppercase tracking-wider text-on-surface-variant">
              {label}
            </p>
          </div>
        ))}
      </div>

      <p className="expedition-meta mt-5 text-center text-body-sm text-on-surface-variant">
        <span className="capitalize">{meta.budget_tier}</span> budget · {meta.city}
      </p>
    </section>
  );
}
