"use client";

import { Plus, RefreshCw } from "lucide-react";
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

  return (
    <div className="-mx-container-mobile flex flex-col md:-mx-container-desktop">
      <TripSummaryBar data={data} />

      <div className="mt-6 space-y-6 px-0">
        <div>
          <h1 className="text-headline-md font-bold text-on-surface">Your itinerary</h1>
          <p className="mt-1 text-body-sm text-on-surface-variant">
            {data.meta.planner_mode === "ai" ? "AI-enhanced" : "Standard"} plan ·{" "}
            {data.summary.total_travel_min} min walking
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

        <ItineraryMap key={data.stops.map((s) => s.poi_id).join("-")} data={data} />

        <ItineraryTimeline stops={data.stops} />

        <div className="flex flex-col gap-4 sm:flex-row">
          <button
            type="button"
            onClick={regenerate}
            disabled={pending}
            className="btn-primary flex-1 rounded-xl py-4 shadow-glow-btn disabled:opacity-50"
          >
            <RefreshCw className={`h-5 w-5 ${pending ? "animate-spin" : ""}`} aria-hidden />
            {pending ? "Regenerating…" : "Regenerate"}
          </button>
          <Link
            href="/plan"
            className="flex flex-1 items-center justify-center gap-2 rounded-xl border border-outline py-4 font-semibold text-on-surface transition-all hover:bg-surface-container-high active:scale-95"
          >
            <Plus className="h-5 w-5" aria-hidden />
            Plan another day
          </Link>
        </div>

        <CostDisclaimer />
      </div>
    </div>
  );
}
