"use client";

import Image from "next/image";
import {
  ArrowRight,
  Diamond,
  Footprints,
  History,
  Loader2,
  Moon,
  Wallet,
  Sparkles,
  UtensilsCrossed,
  WifiOff,
  type LucideIcon,
} from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useRef, useState, useTransition } from "react";

import { ApiError, generateItinerary } from "@/lib/api";
import { loadPlanForm, saveItinerary, savePlanForm } from "@/lib/storage";
import { validatePlanForm } from "@/lib/validation";
import type { BudgetTier, DurationKey, Interest } from "@/types/itinerary";

const HERO_IMAGE =
  "https://images.unsplash.com/photo-1587474260584-136574528ed5?q=80&w=1600&auto=format&fit=crop";

const INTERESTS: { id: Interest; label: string; icon: LucideIcon }[] = [
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
  { id: "1d", label: "1d" },
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

  useEffect(() => {
    const saved = loadPlanForm();
    if (saved) {
      setBudget(saved.budget);
      setDuration(saved.duration);
      setSelected(saved.interests);
      setUseAi(saved.useAi);
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

    const validation = validatePlanForm({ budget, interests: selected, duration });
    if (!validation.ok) {
      setError(validation.message);
      return;
    }

    const body = validation.value;
    const savedForm = { ...body, useAi };
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

  return (
    <div className="-mx-container-mobile md:-mx-container-desktop">
      {/* Hero */}
      <section className="relative flex h-[265px] w-full items-end overflow-hidden px-container-mobile pb-8 md:px-container-desktop">
        <Image
          src={HERO_IMAGE}
          alt="India Gate at dusk"
          fill
          className="object-cover brightness-50 grayscale"
          priority
          unoptimized
        />
        <div className="absolute inset-0 bg-gradient-to-t from-background via-background/40 to-transparent" />
        <div className="relative z-10 max-w-3xl">
          <h1 className="text-display-lg font-bold text-on-surface">Customize Your Trip</h1>
          <p className="mt-2 max-w-xl text-body-md text-on-surface-variant">
            Tailor your Delhi experience with AI-driven precision. Every route is optimized for
            walking times and your interests.
          </p>
        </div>
      </section>

      <section className="mx-auto mt-8 max-w-3xl px-container-mobile md:px-0">
        {offline ? (
          <div className="mb-6 flex items-center gap-2 rounded-xl border border-error-container/40 bg-error-container/20 px-4 py-3 text-sm text-on-error-container">
            <WifiOff className="h-4 w-4 shrink-0" aria-hidden />
            Internet required to generate a plan.
          </div>
        ) : null}

        <form
          onSubmit={onSubmit}
          className="space-y-10 rounded-xl border border-outline-variant bg-surface-container p-8 shadow-2xl"
        >
          {/* Budget */}
          <div className="space-y-4">
            <span className="section-label">Estimated Budget</span>
            <div className="grid grid-cols-3 gap-3">
              {BUDGETS.map(({ id, label, icon: Icon }) => (
                <button
                  key={id}
                  type="button"
                  onClick={() => setBudget(id)}
                  className={`flex flex-col items-center justify-center rounded-xl border py-4 text-sm transition-all ${
                    budget === id
                      ? "border-primary-container bg-primary-container text-on-primary-container shadow-glow"
                      : "border-outline-variant text-on-surface-variant hover:bg-surface-container-high"
                  }`}
                >
                  <Icon className="mb-1 h-5 w-5" aria-hidden />
                  {label}
                </button>
              ))}
            </div>
          </div>

          {/* Interests */}
          <div className="space-y-4">
            <span className="section-label">Primary Interests</span>
            <div className="flex flex-wrap gap-3">
              {INTERESTS.map(({ id, label, icon: Icon }) => {
                const on = selected.includes(id);
                return (
                  <button
                    key={id}
                    type="button"
                    onClick={() => toggleInterest(id)}
                    className={`flex items-center gap-2 rounded-full border px-6 py-3 text-body-md transition-all ${
                      on
                        ? "border-primary-container bg-primary-container/15 text-primary"
                        : "border-outline-variant text-on-surface-variant hover:bg-surface-container-high"
                    }`}
                  >
                    <Icon className="h-4 w-4" aria-hidden />
                    {label}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Duration */}
          <div className="space-y-4">
            <span className="section-label">Travel Duration</span>
            <div className="flex gap-4">
              {DURATIONS.map(({ id, label }) => (
                <button
                  key={id}
                  type="button"
                  onClick={() => setDuration(id)}
                  className={`flex-1 rounded-xl border py-3 text-center text-sm transition-all ${
                    duration === id
                      ? "border-primary-container bg-primary-container text-on-primary-container"
                      : "border-outline-variant text-on-surface-variant hover:bg-surface-container-high"
                  }`}
                >
                  {label}
                </button>
              ))}
            </div>
          </div>

          {/* AI toggle */}
          <div className="flex items-center justify-between rounded-xl border border-outline-variant/30 bg-surface-container-low p-4">
            <div className="flex items-center gap-3">
              <div className="rounded-lg bg-primary-container/20 p-2">
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
              className="rounded-xl border border-error-container/40 bg-error-container/20 px-4 py-3 text-sm text-on-error-container"
              role="alert"
            >
              {error}
              <button type="submit" className="mt-2 block text-primary underline" disabled={pending}>
                Retry
              </button>
            </div>
          ) : null}

          {pending && slowHint ? (
            <p className="text-sm text-on-surface-variant">Still working… this can take a moment.</p>
          ) : null}

          <div className="pt-2">
            {pending ? (
              <div className="flex flex-col items-center justify-center space-y-4 py-4">
                <Loader2 className="h-12 w-12 animate-spin text-primary" aria-hidden />
                <div className="text-center">
                  <p className="animate-pulse font-bold text-primary">
                    {useAi ? "Generating with AI tips…" : "Building your itinerary…"}
                  </p>
                  {useAi ? (
                    <p className="mt-1 font-mono text-label-mono text-on-surface-variant">
                      Usually 5–20 seconds
                    </p>
                  ) : null}
                </div>
              </div>
            ) : (
              <button type="submit" disabled={offline} className="btn-primary w-full rounded-xl py-5">
                Generate Itinerary
                <ArrowRight className="h-5 w-5" aria-hidden />
              </button>
            )}
          </div>
        </form>

        <p className="mt-8 text-center text-sm text-on-surface-variant">
          <Link href="/" className="text-primary hover:underline">
            Back to home
          </Link>
        </p>
      </section>
    </div>
  );
}
