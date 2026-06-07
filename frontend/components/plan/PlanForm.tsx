"use client";

import {
  Calendar,
  Diamond,
  Footprints,
  History,
  MapPin,
  Moon,
  Sparkles,
  UtensilsCrossed,
  Wallet,
  WifiOff,
  type LucideIcon,
} from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useRef, useState, useTransition } from "react";

import { AiProcessingView } from "@/components/plan/AiProcessingView";
import { LocationPicker } from "@/components/plan/LocationPicker";
import { ApiError, generateItinerary } from "@/lib/api";
import { DEFAULT_CITY } from "@/lib/constants";
import { DEFAULT_START_LOCATION } from "@/lib/locations";
import {
  loadPlanForm,
  resolveStartLocation,
  saveItinerary,
  savePlanForm,
} from "@/lib/storage";
import { validatePlanForm } from "@/lib/validation";
import type { BudgetTier, DurationKey, Interest, TripLocation } from "@/types/itinerary";

const INTERESTS: {
  id: Interest;
  label: string;
  icon: LucideIcon;
}[] = [
  { id: "food", label: "Food", icon: UtensilsCrossed },
  { id: "history", label: "History", icon: History },
  { id: "nature", label: "Nature", icon: Footprints },
  { id: "nightlife", label: "Nightlife", icon: Moon },
];

const BUDGETS: { id: BudgetTier; label: string; icon: LucideIcon }[] = [
  { id: "low", label: "Low", icon: UtensilsCrossed },
  { id: "medium", label: "Medium", icon: Wallet },
  { id: "high", label: "High", icon: Diamond },
];

const DURATIONS: { id: DurationKey; label: string }[] = [
  { id: "4h", label: "4h" },
  { id: "8h", label: "8h" },
  { id: "1d", label: "1 day" },
];

export function PlanForm() {
  const router = useRouter();
  const [pending, startTransition] = useTransition();
  const [error, setError] = useState<string | null>(null);
  const [slowHint, setSlowHint] = useState(false);
  const [offline, setOffline] = useState(false);
  const submitLock = useRef(false);

  const [budget, setBudget] = useState<BudgetTier>("medium");
  const [duration, setDuration] = useState<DurationKey>("8h");
  const [selected, setSelected] = useState<Interest[]>(["history", "nature"]);
  const [useAi, setUseAi] = useState(false);
  const [startLocation, setStartLocation] = useState<TripLocation>(DEFAULT_START_LOCATION);
  const [locationError, setLocationError] = useState<string | null>(null);

  useEffect(() => {
    const saved = loadPlanForm();
    if (saved) {
      setBudget(saved.budget);
      setDuration(saved.duration);
      setSelected(saved.interests);
      setUseAi(saved.useAi);
      setStartLocation(resolveStartLocation(saved));
    }
  }, []);

  useEffect(() => {
    const update = () => setOffline(typeof navigator !== "undefined" && !navigator.onLine);
    update();
    window.addEventListener("online", update);
    window.addEventListener("offline", update);
    return () => {
      window.removeEventListener("online", update);
      window.removeEventListener("offline", update);
    };
  }, []);

  useEffect(() => {
    if (!pending) {
      setSlowHint(false);
      return;
    }
    const t = window.setTimeout(() => setSlowHint(true), 10_000);
    return () => window.clearTimeout(t);
  }, [pending]);

  function toggleInterest(id: Interest) {
    setSelected((prev) =>
      prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id],
    );
  }

  function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    if (offline) {
      setError("Internet connection required to generate an itinerary.");
      return;
    }
    if (submitLock.current) return;

    const validation = validatePlanForm({
      budget,
      interests: selected,
      duration,
      location: startLocation,
    });
    if (!validation.ok) {
      setLocationError(validation.message);
      setError(validation.message);
      return;
    }
    setLocationError(null);

    const body = validation.value;
    const savedForm = { ...body, useAi, startLocation };
    submitLock.current = true;

    startTransition(async () => {
      try {
        const result = await generateItinerary(body, useAi ? "ai" : "rule");
        if (!result.stops?.length) {
          setError("The server returned an empty itinerary. Please try again.");
          return;
        }
        saveItinerary(result);
        savePlanForm(savedForm);
        router.push("/itinerary");
      } catch (err) {
        setError(
          err instanceof ApiError
            ? err.message
            : "Could not generate itinerary. Is the API running?",
        );
      } finally {
        submitLock.current = false;
      }
    });
  }

  if (pending) {
    return <AiProcessingView useAi={useAi} />;
  }

  return (
    <div className="mx-auto max-w-4xl">
      <header className="mb-xl text-center">
        <div className="relative mx-auto mb-lg w-fit">
          <div className="relative z-10 flex h-20 w-20 items-center justify-center rounded-full bg-gradient-to-br from-primary to-secondary orb-glow">
            <Sparkles className="h-10 w-10 text-on-primary" aria-hidden />
          </div>
          <div className="absolute inset-0 scale-150 rounded-full bg-primary/30 blur-3xl" />
        </div>
        <h1 className="text-display-lg-mobile font-extrabold md:text-display-lg">
          Generate Your <span className="aurora-text">Expedition</span>
        </h1>
        <p className="mx-auto mt-md max-w-2xl text-body-lg text-on-surface-variant">
          Tailor your {DEFAULT_CITY} experience with AI-driven precision. Every route is optimized
          for walking times and your interests.
        </p>
      </header>

      {offline ? (
        <div className="mb-6 flex items-center gap-2 rounded-xl border border-error-container/40 bg-error-container/20 px-4 py-3 text-sm text-on-error-container">
          <WifiOff className="h-4 w-4 shrink-0" aria-hidden />
          Internet required to generate a plan.
        </div>
      ) : null}

      <form
        onSubmit={onSubmit}
        className="glass-panel rounded-4xl p-6 shadow-2xl shadow-primary/5 md:p-10"
      >
        <div className="grid grid-cols-1 gap-lg md:grid-cols-2">
          <div className="space-y-md">
            <div>
              <span className="section-label mb-xs flex items-center gap-2">
                <MapPin className="h-4 w-4" aria-hidden />
                Region
              </span>
              <p className="rounded-xl bg-surface-container-highest/40 px-4 py-3 text-on-surface">
                {DEFAULT_CITY}
              </p>
            </div>

            <LocationPicker
              value={startLocation}
              onChange={(loc) => {
                setStartLocation(loc);
                setLocationError(null);
              }}
              error={locationError}
            />

            <div>
              <span className="section-label mb-xs flex items-center gap-2">
                <Calendar className="h-4 w-4" aria-hidden />
                Travel Duration
              </span>
              <div className="flex gap-2">
                {DURATIONS.map(({ id, label }) => (
                  <button
                    key={id}
                    type="button"
                    onClick={() => setDuration(id)}
                    className={`flex-1 rounded-xl py-3 text-center text-sm font-semibold transition-all active:scale-95 ${
                      duration === id
                        ? "bg-primary-container text-on-primary-container shadow-glow"
                        : "bg-surface-container-highest/40 text-on-surface-variant hover:bg-surface-container-high"
                    }`}
                  >
                    {label}
                  </button>
                ))}
              </div>
            </div>
          </div>

          <div className="space-y-md">
            <div>
              <span className="section-label mb-xs flex items-center gap-2">
                <Wallet className="h-4 w-4" aria-hidden />
                Estimated Budget
              </span>
              <div className="grid grid-cols-3 gap-2">
                {BUDGETS.map(({ id, label, icon: Icon }) => (
                  <button
                    key={id}
                    type="button"
                    onClick={() => setBudget(id)}
                    className={`flex flex-col items-center justify-center rounded-xl border py-3 text-sm transition-all active:scale-95 ${
                      budget === id
                        ? "border-primary/40 bg-primary/20 text-primary shadow-glow"
                        : "border-outline-variant/30 bg-surface-container-highest/40 text-on-surface-variant hover:border-primary/30"
                    }`}
                  >
                    <Icon className="mb-1 h-4 w-4" aria-hidden />
                    {label}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <span className="section-label mb-xs block">Interests</span>
              <div className="flex flex-wrap gap-2">
                {INTERESTS.map(({ id, label, icon: Icon }) => {
                  const on = selected.includes(id);
                  return (
                    <button
                      key={id}
                      type="button"
                      onClick={() => toggleInterest(id)}
                      className={`interest-chip flex items-center gap-2 ${
                        on
                          ? "border-primary/30 bg-primary/20 text-primary"
                          : "border-outline-variant/30 bg-surface-container-highest/60 text-on-surface-variant hover:border-primary/40"
                      }`}
                    >
                      <Icon className="h-3.5 w-3.5" aria-hidden />
                      {label}
                    </button>
                  );
                })}
              </div>
            </div>
          </div>
        </div>

        <div className="mt-lg flex items-center justify-between rounded-xl border border-outline-variant/20 bg-surface-container-highest/40 p-4 transition-colors hover:border-primary/30">
          <div className="flex items-center gap-3">
            <div className="rounded-lg bg-primary/20 p-2">
              <Sparkles className="h-5 w-5 text-primary" aria-hidden />
            </div>
            <div>
              <p className="font-bold text-body-md">Enhance with AI (Groq)</p>
              <p className="text-sm text-on-surface-variant">
                Real-time tips &amp; hidden gems per stop
              </p>
            </div>
          </div>
          <label className="relative inline-flex cursor-pointer items-center">
            <input
              type="checkbox"
              checked={useAi}
              onChange={(e) => setUseAi(e.target.checked)}
              className="peer sr-only"
            />
            <div className="peer h-6 w-11 rounded-full bg-surface-container-highest after:absolute after:left-[2px] after:top-[2px] after:h-5 after:w-5 after:rounded-full after:bg-white after:transition-all peer-checked:bg-primary-container peer-checked:after:translate-x-full" />
          </label>
        </div>

        {error ? (
          <div
            className="mt-6 rounded-xl border border-error-container/40 bg-error-container/20 px-4 py-3 text-sm text-on-error-container"
            role="alert"
          >
            {error}
            <button type="submit" className="mt-2 block text-primary underline" disabled={pending}>
              Retry
            </button>
          </div>
        ) : null}

        {slowHint ? (
          <p className="mt-4 text-sm text-on-surface-variant">Still working… this can take a moment.</p>
        ) : null}

        <button
          type="submit"
          disabled={offline}
          className="btn-primary mt-lg w-full rounded-2xl py-5"
        >
          <Sparkles className={`h-5 w-5 ${pending ? "animate-spin" : ""}`} aria-hidden />
          Generate AI Itinerary
        </button>
      </form>

      <p className="mt-8 text-center text-sm text-on-surface-variant">
        <Link href="/" className="text-primary transition-colors hover:text-secondary">
          ← Back to explore
        </Link>
      </p>
    </div>
  );
}
