"use client";

import { Plus, RefreshCw } from "lucide-react";
import { useAppTab } from "@/components/navigation/useAppTab";
import { useCallback, useEffect, useState, useTransition } from "react";

import { trackEvent } from "@/lib/analytics";
import { ApiError, generateItinerary } from "@/lib/api";
import { loadItinerary, loadPlanForm, saveItinerary } from "@/lib/storage";
import type { ItineraryResponse } from "@/types/itinerary";

import { CostDisclaimer } from "./CostDisclaimer";
import { EmptyItineraryError } from "./EmptyItineraryError";
import { ExpeditionHero } from "./ExpeditionHero";
import { ItineraryMap } from "./ItineraryMap";
import { ItineraryTimeline } from "./ItineraryTimeline";
import { WarningsBanner } from "./WarningsBanner";

export function ItineraryView() {
  const { setTab } = useAppTab();
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
    trackEvent({ event: "itinerary_viewed" });
  }, []);

  const regenerate = useCallback(() => {
    const form = loadPlanForm();
    if (!form) {
      setTab("plan");
      return;
    }
    setError(null);
    const { useAi, startLocation, ...body } = form;
    void startLocation;
    startTransition(async () => {
      try {
        const result = await generateItinerary(body, useAi ? "ai" : "rule");
        if (!result.stops?.length) {
          setError("Empty itinerary returned. Try different interests.");
          return;
        }
        saveItinerary(result);
        setData(result);
        trackEvent({
          event: "itinerary_generated",
          properties: { mode: useAi ? "ai" : "rule" },
        });
      } catch (err) {
        setError(
          err instanceof ApiError
            ? err.message
            : "Regeneration failed. Check the API connection.",
        );
      }
    });
  }, [setTab]);

  if (!data) {
    return <EmptyItineraryError message={error ?? undefined} />;
  }

  return (
    <div className="flex w-full flex-col">
      <ExpeditionHero data={data} />

      <WarningsBanner
        warnings={data.meta.warnings}
        aiStatus={data.meta.ai_status}
        fallbackReason={data.meta.fallback_reason}
      />

      {error ? (
        <p className="mb-4 text-sm text-error" role="alert">
          {error}
        </p>
      ) : null}

      <div className="grid grid-cols-1 items-start gap-xl lg:grid-cols-12">
        <section className="relative lg:col-span-7">
          <div className="absolute bottom-8 left-6 top-8 hidden timeline-line md:block" aria-hidden />
          <ItineraryTimeline stops={data.stops} />
        </section>

        <section className="flex flex-col gap-md lg:col-span-5">
          <div className="glass-card overflow-hidden rounded-2xl">
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

          <div className="glass-card relative overflow-hidden rounded-2xl p-6">
            <div className="absolute -right-12 -top-12 h-32 w-32 rounded-full bg-primary/10 blur-3xl" />
            <h3 className="text-headline-md font-semibold text-on-surface">Pilot intelligence</h3>
            <p className="mt-3 text-body-sm leading-relaxed text-on-surface-variant">
              Routing via {data.meta.routing_source ?? "planner"}. Costs are rough estimates for
              planning — not bookings or tickets.
            </p>
          </div>
        </section>
      </div>

      <div className="mt-xl flex w-full flex-col gap-4 sm:flex-row sm:items-stretch">
        <button
          type="button"
          onClick={regenerate}
          disabled={pending}
          className="btn-primary flex-1 rounded-2xl py-4 disabled:opacity-50"
        >
          <RefreshCw className={`h-5 w-5 ${pending ? "animate-spin" : ""}`} aria-hidden />
          {pending ? "Regenerating…" : "Regenerate"}
        </button>
        <button type="button" onClick={() => setTab("plan")} className="btn-ghost flex-1">
          <Plus className="h-5 w-5" aria-hidden />
          Plan another day
        </button>
      </div>

      <CostDisclaimer />
    </div>
  );
}
