"use client";

import { Clock, IndianRupee, Plus, RefreshCw, Route, Sparkles } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useCallback, useEffect, useState, useTransition } from "react";

import { trackEvent } from "@/lib/analytics";
import { ApiError, generateItinerary } from "@/lib/api";
import { loadItinerary, loadPlanForm, saveItinerary } from "@/lib/storage";
import type { ItineraryResponse } from "@/types/itinerary";

import { CostDisclaimer } from "./CostDisclaimer";
import { EmptyItineraryError } from "./EmptyItineraryError";
import { ItineraryMap } from "./ItineraryMap";
import { ItineraryTimeline } from "./ItineraryTimeline";
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
    trackEvent({ event: "itinerary_viewed" });
  }, []);

  const regenerate = useCallback(() => {
    const form = loadPlanForm();
    if (!form) {
      router.push("/plan");
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
  }, [router]);

  if (!data) {
    return <EmptyItineraryError message={error ?? undefined} />;
  }

  const isAi = data.meta.planner_mode === "ai";
  const cost = data.summary.total_cost_inr;
  const hours = Math.round(data.meta.duration_minutes / 60);

  return (
    <div className="flex flex-col">
      <header className="mb-xl text-center">
        <h1 className="text-display-lg-mobile font-extrabold md:text-display-lg aurora-text">
          Your expedition
        </h1>
        <p className="mx-auto mt-md max-w-2xl text-body-lg text-on-surface-variant">
          {hours}h · {data.meta.budget_tier} budget · {data.summary.total_stops} stops ·{" "}
          {data.summary.total_travel_min} min walking
        </p>
        <div className="mt-md flex flex-wrap justify-center gap-2">
          {isAi ? (
            <span className="flex items-center gap-1 rounded-full border border-primary/30 bg-primary/15 px-3 py-1 text-xs font-semibold text-primary">
              <Sparkles className="h-3.5 w-3.5" aria-hidden />
              AI enhanced
            </span>
          ) : null}
          <span className="rounded-full border border-secondary/30 bg-secondary/10 px-3 py-1 text-xs font-semibold text-secondary">
            {data.meta.city}
          </span>
        </div>
      </header>

      <div className="mb-xl grid grid-cols-2 gap-md md:grid-cols-4">
        {[
          {
            icon: IndianRupee,
            label: "Est. cost",
            value: `₹${cost.low}–${cost.high}`,
          },
          {
            icon: Route,
            label: "Travel time",
            value: `${data.summary.total_travel_min} min`,
          },
          {
            icon: Clock,
            label: "Duration",
            value: `${hours}h`,
          },
          {
            icon: Sparkles,
            label: "Stops",
            value: String(data.summary.total_stops),
          },
        ].map(({ icon: Icon, label, value }) => (
          <div
            key={label}
            className="glass-card glass-card-hover flex flex-col items-center rounded-xl p-md text-center"
          >
            <Icon className="mb-2 h-8 w-8 text-primary" aria-hidden />
            <span className="text-caption font-semibold uppercase tracking-wider text-on-surface-variant">
              {label}
            </span>
            <span className="mt-1 text-headline-md font-bold text-on-surface">{value}</span>
          </div>
        ))}
      </div>

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

      <div className="grid grid-cols-1 gap-xl lg:grid-cols-12">
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

      <div className="mt-xl flex flex-col gap-4 sm:flex-row">
        <button
          type="button"
          onClick={regenerate}
          disabled={pending}
          className="btn-primary flex-1 rounded-2xl py-4 disabled:opacity-50"
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
