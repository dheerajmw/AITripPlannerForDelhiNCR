"use client";

import { Plus, RefreshCw, Sparkles } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useCallback, useEffect, useState, useTransition } from "react";

import { ApiError, generateItinerary } from "@/lib/api";
import { loadItinerary, loadPlanForm, saveItinerary } from "@/lib/storage";
import type { ItineraryResponse } from "@/types/itinerary";

import { CostDisclaimer } from "./CostDisclaimer";
import { EmptyItineraryError } from "./EmptyItineraryError";
import { ItineraryMap } from "./ItineraryMap";
import { ItineraryTimeline } from "./ItineraryTimeline";
import { TripSummaryBar } from "./TripSummaryBar";
import { WarningsBanner } from "./WarningsBanner";

export function ItineraryView() {
  const router = useRouter();
  const [data, setData] = useState<ItineraryResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [pending, startTransition] = useTransition();

  useEffect(() => {
    const loaded = loadItinerary();
    if (!loaded || loaded.stops.length === 0) {
      setData(null);
      return;
    }
    setData(loaded);
  }, []);

  const regenerate = useCallback(() => {
    const form = loadPlanForm();
    if (!form) {
      router.push("/plan");
      return;
    }
    setError(null);
    const { useAi, ...body } = form;
    startTransition(async () => {
      try {
        const result = await generateItinerary(body, useAi ? "ai" : "rule");
        if (!result.stops?.length) {
          setError("Empty itinerary returned. Try different interests.");
          return;
        }
        saveItinerary(result);
        setData(result);
      } catch (err) {
        setError(
          err instanceof ApiError
            ? err.message
            : "Regeneration failed. Check the API connection.",
        );
      }
    });
  }, [router]);

  if (!data) {
    return <EmptyItineraryError message={error ?? undefined} />;
  }

  const isAi = data.meta.planner_mode === "ai";
  const cost = data.summary.total_cost_inr;

  return (
    <div className="flex flex-col">
      <TripSummaryBar data={data} />

      <div className="grid grid-cols-1 gap-gutter lg:grid-cols-12">
        {/* Timeline column */}
        <section className="col-span-12 space-y-6 lg:col-span-7">
          <div>
            <h1 className="text-display-lg text-on-surface">Your expedition</h1>
            <div className="mt-3 flex flex-wrap gap-2">
              <span className="rounded-full border border-secondary/20 bg-secondary/10 px-3 py-1 text-xs font-semibold text-secondary">
                {Math.round(data.meta.duration_minutes / 60)}h
              </span>
              <span className="rounded-full border border-tertiary/20 bg-tertiary/10 px-3 py-1 text-xs font-semibold text-tertiary">
                {data.meta.budget_tier} budget
              </span>
              {isAi ? (
                <span className="flex items-center gap-1 rounded-full border border-primary/20 bg-primary/10 px-3 py-1 text-xs font-semibold text-primary">
                  <Sparkles className="h-3.5 w-3.5" aria-hidden />
                  AI enhanced
                </span>
              ) : null}
            </div>
            <p className="mt-2 text-body-sm text-on-surface-variant">
              {data.summary.total_travel_min} min walking · {data.summary.total_stops} stops
            </p>
          </div>

          <WarningsBanner
            warnings={data.meta.warnings}
            aiStatus={data.meta.ai_status}
            fallbackReason={data.meta.fallback_reason}
          />

          {error ? (
            <p className="text-sm text-error" role="alert">
              {error}
            </p>
          ) : null}

          <ItineraryTimeline stops={data.stops} />
        </section>

        {/* Map + stats column */}
        <section className="col-span-12 flex flex-col gap-6 lg:col-span-5">
          <div className="glass-panel overflow-hidden rounded-2xl">
            <div className="border-b border-white/5 px-4 py-3">
              <span className="text-xs font-bold uppercase tracking-widest text-primary">
                Live Route
              </span>
            </div>
            <ItineraryMap
              key={data.stops.map((s) => s.poi_id).join("-")}
              data={data}
            />
          </div>

          <div className="glass-panel relative overflow-hidden rounded-2xl p-6">
            <div className="absolute -right-12 -top-12 h-32 w-32 rounded-full bg-primary/10 blur-3xl" />
            <h3 className="text-headline-md font-semibold text-on-surface">Expedition stats</h3>
            <div className="mt-6 grid grid-cols-2 gap-4">
              <div className="rounded-xl border border-white/5 bg-surface-container-low/50 p-4">
                <p className="mb-1 text-[10px] font-bold uppercase tracking-widest text-on-surface-variant">
                  Travel
                </p>
                <p className="text-2xl font-bold text-on-surface">
                  {data.summary.total_travel_min}
                  <span className="text-sm font-normal text-on-surface-variant"> min</span>
                </p>
              </div>
              <div className="rounded-xl border border-white/5 bg-surface-container-low/50 p-4">
                <p className="mb-1 text-[10px] font-bold uppercase tracking-widest text-on-surface-variant">
                  Est. cost
                </p>
                <p className="text-2xl font-bold text-on-surface">
                  ₹{cost.low}–{cost.high}
                </p>
              </div>
              <div className="col-span-2 rounded-xl border border-primary/20 bg-primary/5 p-4">
                <div className="flex items-start gap-3">
                  <Sparkles className="h-5 w-5 shrink-0 text-primary" aria-hidden />
                  <div>
                    <h5 className="mb-1 text-sm font-bold text-primary">Pilot intelligence</h5>
                    <p className="text-xs leading-relaxed text-on-surface-variant">
                      Routing via {data.meta.routing_source ?? "planner"}. Costs are rough
                      estimates for planning — not bookings or tickets.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>

      <div className="mt-8 flex flex-col gap-4 sm:flex-row">
        <button
          type="button"
          onClick={regenerate}
          disabled={pending}
          className="btn-primary flex-1 rounded-xl py-4 disabled:opacity-50"
        >
          <RefreshCw className={`h-5 w-5 ${pending ? "animate-spin" : ""}`} aria-hidden />
          {pending ? "Regenerating…" : "Regenerate"}
        </button>
        <Link href="/plan" className="btn-ghost flex-1">
          <Plus className="h-5 w-5" aria-hidden />
          Plan another day
        </Link>
      </div>

      <CostDisclaimer />
    </div>
  );
}
