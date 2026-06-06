"use client";

import Image from "next/image";
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
  Zap,
  type LucideIcon,
} from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useRef, useState, useTransition } from "react";

import { AiProcessingView } from "@/components/plan/AiProcessingView";
import { ApiError, generateItinerary } from "@/lib/api";
import { loadPlanForm, saveItinerary, savePlanForm } from "@/lib/storage";
import { validatePlanForm } from "@/lib/validation";
import type { BudgetTier, DurationKey, Interest } from "@/types/itinerary";

const HERO_IMAGE =
  "https://images.unsplash.com/photo-1587474260584-136574528ed5?q=80&w=1600&auto=format&fit=crop";

const INTERESTS: {
  id: Interest;
  label: string;
  icon: LucideIcon;
  chipClass: string;
}[] = [
  {
    id: "food",
    label: "Food",
    icon: UtensilsCrossed,
    chipClass: "border-secondary/20 bg-secondary/10 text-secondary",
  },
  {
    id: "history",
    label: "History",
    icon: History,
    chipClass: "border-primary/20 bg-primary/10 text-primary",
  },
  {
    id: "nature",
    label: "Nature",
    icon: Footprints,
    chipClass: "border-secondary/20 bg-secondary/10 text-secondary",
  },
  {
    id: "nightlife",
    label: "Nightlife",
    icon: Moon,
    chipClass: "border-tertiary/20 bg-tertiary/10 text-tertiary",
  },
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

  if (pending) {
    return <AiProcessingView useAi={useAi} />;
  }

  return (
    <div>
      <section className="relative flex h-[240px] w-full items-end overflow-hidden px-6 pb-8 md:px-10">
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
          <h1 className="text-headline-lg font-bold text-on-surface">Generate Your Expedition</h1>
          <p className="mt-2 max-w-xl text-body-md text-on-surface-variant">
            Tailor your Delhi experience with AI-driven precision. Every route is optimized for
            walking times and your interests.
          </p>
        </div>
      </section>

      <section className="relative z-10 -mt-8 px-6 pb-16 md:px-10">
        {offline ? (
          <div className="mb-6 flex items-center gap-2 rounded-xl border border-error-container/40 bg-error-container/20 px-4 py-3 text-sm text-on-error-container">
            <WifiOff className="h-4 w-4 shrink-0" aria-hidden />
            Internet required to generate a plan.
          </div>
        ) : null}

        <form
          onSubmit={onSubmit}
          className="glass-panel relative mx-auto max-w-4xl overflow-hidden rounded-2xl p-8 shadow-2xl md:p-10"
        >
          <div className="absolute left-0 top-0 h-1 w-full bg-gradient-to-r from-transparent via-primary/40 to-transparent" />

          <div className="grid grid-cols-1 gap-10 md:grid-cols-2">
            {/* Budget */}
            <div className="space-y-4">
              <span className="section-label flex items-center gap-2">
                <Wallet className="h-4 w-4" aria-hidden />
                Estimated Budget
              </span>
              <div className="grid grid-cols-3 gap-3">
                {BUDGETS.map(({ id, label, icon: Icon }) => (
                  <button
                    key={id}
                    type="button"
                    onClick={() => setBudget(id)}
                    className={`flex flex-col items-center justify-center rounded-xl border py-4 text-sm transition-all active:scale-95 ${
                      budget === id
                        ? "border-primary bg-primary/15 text-primary shadow-glow"
                        : "border-outline-variant text-on-surface-variant hover:border-primary/30 hover:bg-white/5"
                    }`}
                  >
                    <Icon className="mb-1 h-5 w-5" aria-hidden />
                    {label}
                  </button>
                ))}
              </div>
            </div>

            {/* Duration */}
            <div className="space-y-4">
              <span className="section-label flex items-center gap-2">
                <Calendar className="h-4 w-4" aria-hidden />
                Travel Duration
              </span>
              <div className="flex gap-3">
                {DURATIONS.map(({ id, label }) => (
                  <button
                    key={id}
                    type="button"
                    onClick={() => setDuration(id)}
                    className={`flex-1 rounded-xl border py-3 text-center text-sm transition-all active:scale-95 ${
                      duration === id
                        ? "border-primary bg-primary text-on-primary-container shadow-glow"
                        : "border-outline-variant text-on-surface-variant hover:border-primary/30 hover:bg-white/5"
                    }`}
                  >
                    {label}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Interests */}
          <div className="mt-10 space-y-4">
            <span className="section-label flex items-center gap-2">
              <MapPin className="h-4 w-4" aria-hidden />
              Primary Interests
            </span>
            <div className="flex flex-wrap gap-3">
              {INTERESTS.map(({ id, label, icon: Icon, chipClass }) => {
                const on = selected.includes(id);
                return (
                  <button
                    key={id}
                    type="button"
                    onClick={() => toggleInterest(id)}
                    className={`interest-chip flex items-center gap-2 px-4 py-2 text-xs ${
                      on ? chipClass : "border-outline-variant bg-surface-container-low text-on-surface-variant hover:bg-white/5"
                    }`}
                  >
                    <Icon className="h-3.5 w-3.5" aria-hidden />
                    {label}
                  </button>
                );
              })}
            </div>
          </div>

          {/* AI toggle */}
          <div className="ai-toggle-box mt-10 flex items-center justify-between rounded-xl border border-outline-variant/30 bg-surface-container-low p-4 transition-colors hover:border-primary/30">
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
              <div className="peer h-6 w-11 rounded-full bg-surface-container-highest after:absolute after:left-[2px] after:top-[2px] after:h-5 after:w-5 after:rounded-full after:bg-white after:transition-all peer-checked:bg-primary peer-checked:after:translate-x-full" />
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
            className="btn-primary mt-8 w-full rounded-xl py-5"
          >
            Generate My Trip
            <Zap className="h-5 w-5" aria-hidden />
          </button>
        </form>

        <p className="mt-8 text-center text-sm text-on-surface-variant">
          <Link href="/" className="text-primary transition-colors hover:text-secondary">
            ← Back to dashboard
          </Link>
        </p>
      </section>
    </div>
  );
}
