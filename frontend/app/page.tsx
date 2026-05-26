import Image from "next/image";
import Link from "next/link";
import { Footprints, Map, Sparkles } from "lucide-react";

import { ApiStatusBadge } from "@/components/layout/ApiStatusBadge";
import { DEFAULT_CITY } from "@/lib/constants";

const FEATURES = [
  {
    icon: Map,
    title: "Real OSM venues",
    text: "Accurate geospatial data for every cafe, monument, and metro station in the NCR region.",
    accent: "primary",
  },
  {
    icon: Footprints,
    title: "Optimized walking route",
    text: "Smart pathfinding that accounts for Delhi's street layout and pedestrian shortcuts.",
    accent: "secondary",
  },
  {
    icon: Sparkles,
    title: "Optional AI tips",
    text: "Contextual advice on peak hours, local etiquette, and hidden spots from our LLM layer.",
    accent: "tertiary",
    beta: true,
  },
] as const;

const MAP_PREVIEW =
  "https://images.unsplash.com/photo-1587474260584-136574528ed5?q=80&w=1200&auto=format&fit=crop";

export default function Home() {
  return (
    <div className="flex flex-col gap-card-gap">
      {/* Hero */}
      <section className="relative mb-4 overflow-hidden rounded-3xl border border-outline-variant bg-surface-container bg-mesh-gradient p-8 md:p-12">
        <div className="relative z-10 flex flex-col items-center text-center">
          <ApiStatusBadge />
          <h1 className="mt-6 text-headline-mobile font-extrabold leading-tight text-on-surface md:text-display-lg">
            Plan your {DEFAULT_CITY} day in{" "}
            <span className="text-primary">minutes</span>
          </h1>
          <p className="mt-4 max-w-md text-body-md text-on-surface-variant">
            Real OSM places, walking routes, and optional AI tips.
          </p>
          <Link href="/plan" className="btn-primary mt-10">
            Start planning
          </Link>
        </div>
        <div
          className="pointer-events-none absolute -bottom-10 -right-10 h-64 w-64 rounded-full bg-primary opacity-10 blur-[80px]"
          aria-hidden
        />
      </section>

      {/* Capabilities */}
      <section className="relative space-y-card-gap">
        <h2 className="section-label text-xs">Capabilities</h2>
        {FEATURES.map((feature, index) => (
          <div key={feature.title} className="relative">
            {index < FEATURES.length - 1 && (
              <div className="travel-line-connector hidden sm:block" aria-hidden />
            )}
            <div className="glass-card glass-card-hover group relative z-10 flex gap-6 p-6">
              <div
                className={`flex h-12 w-12 shrink-0 items-center justify-center rounded-xl border border-outline-variant bg-surface-container-highest transition-colors ${
                  feature.accent === "primary"
                    ? "group-hover:border-primary"
                    : feature.accent === "secondary"
                      ? "group-hover:border-secondary"
                      : "group-hover:border-tertiary"
                }`}
              >
                <feature.icon
                  className={`h-6 w-6 ${
                    feature.accent === "primary"
                      ? "text-primary"
                      : feature.accent === "secondary"
                        ? "text-secondary"
                        : "text-tertiary"
                  }`}
                  aria-hidden
                />
              </div>
              <div className="flex min-w-0 flex-col gap-1">
                <div className="flex flex-wrap items-center gap-2">
                  <h3 className="text-xl font-bold text-on-surface">{feature.title}</h3>
                  {"beta" in feature && feature.beta ? (
                    <span className="rounded border border-tertiary/20 bg-tertiary/10 px-2 py-0.5 text-[10px] font-bold uppercase text-tertiary">
                      Beta
                    </span>
                  ) : null}
                </div>
                <p className="text-sm text-on-surface-variant">{feature.text}</p>
              </div>
            </div>
          </div>
        ))}
      </section>

      {/* Map preview */}
      <section className="mt-8 overflow-hidden rounded-3xl border border-outline-variant bg-surface-container p-4">
        <div className="group relative h-64 w-full overflow-hidden rounded-2xl border border-outline-variant">
          <Image
            src={MAP_PREVIEW}
            alt="Stylized map of Delhi NCR"
            fill
            className="object-cover opacity-50 grayscale transition-all duration-700 group-hover:scale-105 group-hover:opacity-80"
            sizes="(max-width: 896px) 100vw, 896px"
            unoptimized
          />
          <div className="absolute inset-0 bg-gradient-to-t from-background via-transparent to-transparent" />
          <div className="absolute bottom-6 left-6 flex flex-col">
            <span className="font-mono text-xs font-bold text-primary">LIVE VIEW</span>
            <span className="text-2xl font-bold text-on-surface">Connaught Place</span>
          </div>
        </div>
      </section>

      <p className="text-center font-mono text-mono-xs uppercase tracking-widest text-on-surface-variant/60">
        Estimates only · MVP · No bookings or tickets
      </p>
    </div>
  );
}
