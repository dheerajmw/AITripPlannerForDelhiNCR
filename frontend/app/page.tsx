import Link from "next/link";
import {
  Car,
  History,
  MapPin,
  Sparkles,
  Theater,
  UtensilsCrossed,
  Wallet,
} from "lucide-react";

import { DEFAULT_CITY } from "@/lib/constants";

const BENTO = [
  {
    title: "Curated Dining at Taj",
    tag: "Exclusive Access",
    text: "AI identified lower wait times for window seats at Varq tonight.",
    span: "md:col-span-8",
    tall: true,
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
    text: "Zero-wait travel coordinated with your AI itinerary.",
    span: "md:col-span-4",
    icon: Car,
  },
  {
    title: "Historical Walk",
    text: "AI audio guide for Lodhi Gardens at your pace.",
    span: "md:col-span-4",
    icon: History,
  },
  {
    title: "Late Night Arts",
    text: "Immersive theater — AI recommends tickets.",
    span: "md:col-span-4",
    icon: Theater,
  },
] as const;

export default function Home() {
  return (
    <>
      {/* Hero */}
      <section className="mb-xl flex flex-col items-center text-center">
        <div className="relative mb-lg">
          <div className="relative z-10 flex h-24 w-24 items-center justify-center rounded-full bg-gradient-to-br from-primary to-secondary orb-glow">
            <Sparkles className="h-12 w-12 text-on-primary" aria-hidden />
          </div>
          <div className="absolute inset-0 scale-150 rounded-full bg-primary/30 blur-3xl" />
        </div>

        <h1 className="max-w-3xl text-display-lg-mobile font-extrabold md:text-display-lg">
          Explore{" "}
          <span className="aurora-text">{DEFAULT_CITY}</span>
          <br />
          with AI
        </h1>
        <p className="mt-md max-w-2xl text-body-lg text-on-surface-variant">
          Experience the fusion of historic majesty and futuristic convenience. Our AI crafts
          seamless itineraries tailored to your unique pace and passions.
        </p>
      </section>

      {/* Quick plan preview — chips only, not inputs; full form is on /plan */}
      <section className="mx-auto max-w-4xl">
        <div className="glass-panel rounded-4xl p-6 shadow-2xl shadow-primary/5 md:p-10">
          <p className="mb-md text-center text-caption text-on-surface-variant">
            Example trip preferences · customize on the next step
          </p>
          <div className="grid grid-cols-1 gap-lg sm:grid-cols-2">
            <div className="space-y-md">
              <div>
                <span className="section-label mb-xs flex items-center gap-2">
                  <MapPin className="h-4 w-4" aria-hidden />
                  Destination
                </span>
                <span className="preview-chip preview-chip-active inline-flex items-center gap-2">
                  <MapPin className="h-3.5 w-3.5" aria-hidden />
                  {DEFAULT_CITY}
                </span>
              </div>
              <div>
                <span className="section-label mb-xs block">Duration</span>
                <div className="flex flex-wrap gap-2">
                  {(["4h", "8h", "1 day"] as const).map((d) => (
                    <span
                      key={d}
                      className={`preview-chip ${d === "8h" ? "preview-chip-active" : "preview-chip-muted"}`}
                    >
                      {d}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            <div className="space-y-md">
              <div>
                <span className="section-label mb-xs flex items-center gap-2">
                  <UtensilsCrossed className="h-4 w-4" aria-hidden />
                  Interests
                </span>
                <div className="flex flex-wrap gap-2">
                  {["Food", "History", "Nature"].map((tag) => (
                    <span key={tag} className="preview-chip preview-chip-active">
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
              <div>
                <span className="section-label mb-xs flex items-center gap-2">
                  <Wallet className="h-4 w-4" aria-hidden />
                  Budget
                </span>
                <div className="flex flex-wrap gap-2">
                  {(["Low", "Medium", "High"] as const).map((tier) => (
                    <span
                      key={tier}
                      className={`preview-chip ${tier === "Medium" ? "preview-chip-active" : "preview-chip-muted"}`}
                    >
                      {tier}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>

          <Link href="/plan" className="btn-primary mt-lg w-full rounded-2xl py-5">
            <Sparkles className="h-5 w-5" aria-hidden />
            Generate AI Itinerary
          </Link>
        </div>

        <p className="mt-lg text-center text-caption text-on-surface-variant">
          Estimates only · MVP · No bookings or tickets
        </p>
      </section>

      {/* Bento grid */}
      <section className="mt-xl grid grid-cols-1 gap-md md:grid-cols-12">
        {BENTO.map((card) => (
          <div
            key={card.title}
            className={`glass-card glass-card-hover rounded-2xl p-6 ${card.span} ${
              "tall" in card && card.tall ? "min-h-[240px]" : "min-h-[200px]"
            } flex flex-col ${"stats" in card && card.stats ? "justify-between" : "justify-end"}`}
          >
            {"stats" in card && card.stats ? (
              <>
                <Sparkles className="h-8 w-8 text-primary" aria-hidden />
                <div>
                  <h4 className="text-headline-md font-semibold text-on-surface">{card.title}</h4>
                  <div className="mt-4 space-y-3 text-sm">
                    <div className="flex justify-between text-on-surface-variant">
                      <span>Crowd: GK-II</span>
                      <span className="text-secondary">Low</span>
                    </div>
                    <div className="h-1 overflow-hidden rounded-full bg-white/5">
                      <div className="h-full w-[30%] bg-secondary shadow-[0_0_8px_#ddb7ff]" />
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
                  <card.icon className="mb-3 h-8 w-8 text-primary" aria-hidden />
                ) : null}
                <div>
                  {"tag" in card ? (
                    <span className="mb-2 block text-caption font-bold uppercase tracking-widest text-secondary">
                      {card.tag}
                    </span>
                  ) : null}
                  <h3 className="text-headline-md font-semibold text-on-surface">{card.title}</h3>
                  {"text" in card && card.text ? (
                    <p className="mt-2 text-body-sm text-on-surface-variant">{card.text}</p>
                  ) : null}
                </div>
              </>
            )}
          </div>
        ))}
      </section>
    </>
  );
}
