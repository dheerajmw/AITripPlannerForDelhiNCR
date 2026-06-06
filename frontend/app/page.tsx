import Image from "next/image";
import Link from "next/link";
import {
  Car,
  History,
  BarChart3,
  MapPin,
  Sparkles,
  Theater,
  UtensilsCrossed,
} from "lucide-react";

import { DEFAULT_CITY } from "@/lib/constants";

const HERO_IMAGE =
  "https://images.unsplash.com/photo-1587474260584-136574528ed5?q=80&w=1600&auto=format&fit=crop";

const BENTO = [
  {
    title: "Curated Dining at Taj",
    tag: "Exclusive Access",
    text: "AI identified lower wait times for window seats at Varq tonight.",
    span: "md:col-span-8",
    tall: true,
    accent: "secondary",
  },
  {
    title: "Live Insights",
    tag: "Crowd & traffic",
    span: "md:col-span-4",
    tall: true,
    stats: true,
  },
  {
    title: "Premium Transit",
    tag: "local_taxi",
    text: "Coordinate arrivals with your AI-generated itinerary for zero-wait travel.",
    span: "md:col-span-4",
    icon: Car,
    accent: "primary",
  },
  {
    title: "Historical Walk",
    tag: "history",
    text: "New AI audio guide available for Lodhi Gardens at your own pace.",
    span: "md:col-span-4",
    icon: History,
    accent: "secondary",
  },
  {
    title: "Late Night Arts",
    tag: "nightlife",
    text: "Immersive theater at Mandi House — AI recommends tickets.",
    span: "md:col-span-4",
    icon: Theater,
    accent: "tertiary",
  },
] as const;

export default function Home() {
  return (
    <>
      {/* Hero */}
      <section className="relative flex h-[min(520px,70vh)] flex-col items-center justify-center px-6 text-center">
        <div className="absolute inset-0 z-0">
          <Image
            src={HERO_IMAGE}
            alt="Delhi nightscape"
            fill
            className="object-cover opacity-40 mix-blend-screen"
            priority
            unoptimized
          />
          <div className="absolute inset-0 z-10 bg-gradient-to-b from-transparent via-background/20 to-background" />
        </div>
        <div
          className="ai-orbit left-1/2 top-1/2 h-[500px] w-[500px] -translate-x-1/2 -translate-y-1/2 opacity-20"
          aria-hidden
        />
        <div
          className="ai-orbit left-1/2 top-1/2 h-[700px] w-[700px] -translate-x-1/2 -translate-y-1/2 opacity-10"
          style={{ animationDirection: "reverse", animationDuration: "35s" }}
          aria-hidden
        />
        <div className="relative z-20 max-w-4xl">
          <h1 className="text-display-lg font-bold text-white drop-shadow-2xl">
            Explore {DEFAULT_CITY}
            <br />
            <span className="italic text-primary">with AI</span>
          </h1>
          <p className="mx-auto mt-4 max-w-2xl text-body-lg text-on-surface-variant opacity-90">
            Your luxury digital concierge. Craft a personalized expedition across the National
            Capital Region using real OSM data and optional Groq tips.
          </p>
          <Link href="/plan" className="btn-primary mt-10 inline-flex">
            <Sparkles className="h-5 w-5" aria-hidden />
            Generate My Trip
          </Link>
        </div>
      </section>

      {/* Quick planning card */}
      <section className="relative z-30 -mt-16 px-6 pb-12 md:px-10">
        <div className="glass-panel relative mx-auto max-w-5xl overflow-hidden rounded-2xl p-8 shadow-2xl md:p-10">
          <div className="absolute left-0 top-0 h-1 w-full bg-gradient-to-r from-transparent via-primary/40 to-transparent" />
          <div className="grid grid-cols-1 gap-8 md:grid-cols-4">
            <div className="space-y-3">
              <span className="section-label flex items-center gap-2 text-xs">
                <MapPin className="h-4 w-4" aria-hidden />
                Destination
              </span>
              <p className="rounded-lg bg-surface-container-lowest/50 p-3 text-on-surface">
                India Gate, Delhi
              </p>
            </div>
            <div className="space-y-3">
              <span className="section-label flex items-center gap-2 text-xs">
                Duration
              </span>
              <p className="rounded-lg bg-surface-container-lowest/50 p-3 text-on-surface">
                Half day · Full day
              </p>
            </div>
            <div className="space-y-3">
              <span className="section-label flex items-center gap-2 text-xs">
                <UtensilsCrossed className="h-4 w-4" aria-hidden />
                Interests
              </span>
              <div className="flex flex-wrap gap-2">
                {["Food", "History", "Nature"].map((tag) => (
                  <span
                    key={tag}
                    className="interest-chip border-primary/20 bg-primary/10 text-primary"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            </div>
            <div className="flex items-end">
              <Link href="/plan" className="btn-primary w-full rounded-xl py-4">
                Customize
              </Link>
            </div>
          </div>
        </div>

        {/* Bento grid */}
        <div className="mx-auto mt-16 grid max-w-6xl grid-cols-1 gap-6 md:grid-cols-12">
          {BENTO.map((card) => (
            <div
              key={card.title}
              className={`glass-panel glass-card-hover group cursor-pointer rounded-2xl p-6 ${card.span} ${
                "tall" in card && card.tall ? "min-h-[280px]" : "min-h-[220px]"
              } flex flex-col ${"stats" in card && card.stats ? "justify-between border-primary/20" : "justify-end"}`}
            >
              {"stats" in card && card.stats ? (
                <>
                  <div className="flex h-12 w-12 items-center justify-center rounded-full bg-primary/20">
                    <BarChart3 className="h-6 w-6 text-primary" aria-hidden />
                  </div>
                  <div>
                    <h4 className="text-headline-md font-semibold text-white">{card.title}</h4>
                    <div className="mt-4 space-y-3 text-sm">
                      <div className="flex justify-between text-on-surface-variant">
                        <span>Crowd: GK-II</span>
                        <span className="text-secondary">Low</span>
                      </div>
                      <div className="h-1 overflow-hidden rounded-full bg-white/5">
                        <div className="h-full w-[30%] bg-secondary shadow-[0_0_8px_#4fdbc8]" />
                      </div>
                      <div className="flex justify-between text-on-surface-variant">
                        <span>Traffic: Cyber Hub</span>
                        <span className="text-error">High</span>
                      </div>
                      <div className="h-1 overflow-hidden rounded-full bg-white/5">
                        <div className="h-full w-[85%] bg-error shadow-[0_0_8px_#ffb4ab]" />
                      </div>
                    </div>
                  </div>
                </>
              ) : (
                <>
                  {"icon" in card && card.icon ? (
                    <card.icon
                      className={`mb-4 h-8 w-8 transition-transform group-hover:scale-110 ${
                        card.accent === "primary"
                          ? "text-primary"
                          : card.accent === "secondary"
                            ? "text-secondary"
                            : "text-tertiary"
                      }`}
                      aria-hidden
                    />
                  ) : null}
                  <div>
                    {"tag" in card && !("stats" in card) ? (
                      <span className="mb-2 block text-[10px] font-bold uppercase tracking-widest text-secondary">
                        {card.tag}
                      </span>
                    ) : null}
                    <h3 className="text-xl font-bold text-white">{card.title}</h3>
                    {"text" in card && card.text ? (
                      <p className="mt-2 text-sm text-on-surface-variant">{card.text}</p>
                    ) : null}
                  </div>
                </>
              )}
            </div>
          ))}
        </div>

        <p className="mt-12 text-center text-[10px] uppercase tracking-[0.2em] text-on-surface-variant/50">
          Estimates only · MVP · No bookings or tickets
        </p>
      </section>
    </>
  );
}
