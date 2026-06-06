import { Hourglass, IndianRupee, Sparkles } from "lucide-react";

import type { ItineraryStop } from "@/types/itinerary";

type Props = {
  stop: ItineraryStop;
  badgeVariant?: "primary" | "secondary";
};

export function ItineraryStopCard({ stop, badgeVariant = "primary" }: Props) {
  const badgeClass =
    badgeVariant === "secondary"
      ? "bg-secondary-container text-on-secondary-container"
      : "bg-primary-container text-on-primary-container";

  return (
    <article className="glass-panel group overflow-hidden rounded-xl transition-all duration-300 hover:-translate-y-1 hover:shadow-2xl glow-cyan">
      <div className="p-6">
        <div className="flex flex-col justify-between gap-4 md:flex-row md:items-start">
          <div className="min-w-0 space-y-1">
            <div className="flex flex-wrap items-center gap-3">
              <span className="text-label-md text-secondary">
                {stop.arrive_at} – {stop.depart_at}
              </span>
              <span className="rounded bg-surface-container-highest px-2 py-0.5 text-[10px] font-bold uppercase tracking-wider text-on-surface-variant">
                {stop.category}
              </span>
            </div>
            <h3 className="text-headline-md font-bold text-on-surface">{stop.name}</h3>
            <div className="flex flex-wrap items-center gap-4 text-body-sm text-on-surface-variant">
              <span className="flex items-center gap-1">
                <Hourglass className="h-4 w-4" aria-hidden />
                {stop.visit_minutes}m
              </span>
              <span className="flex items-center gap-1">
                <IndianRupee className="h-4 w-4" aria-hidden />
                {stop.cost_estimate_inr.low}–{stop.cost_estimate_inr.high}
              </span>
            </div>
          </div>
          <div
            className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-full text-sm font-bold md:hidden ${badgeClass}`}
            aria-hidden
          >
            {stop.order}
          </div>
        </div>
        {stop.notes ? (
          <div className="mt-4 rounded-r-lg border-l-2 border-primary bg-primary/10 p-3">
            <p className="flex items-start gap-2 text-body-sm italic text-primary">
              <Sparkles className="mt-0.5 h-[18px] w-[18px] shrink-0" aria-hidden />
              {stop.notes}
            </p>
          </div>
        ) : null}
      </div>
    </article>
  );
}
