"use client";

import { ExternalLink, MapPin } from "lucide-react";

import { buildGoogleMapsRouteUrl } from "@/lib/googleMaps";
import type { ItineraryResponse } from "@/types/itinerary";

type Props = {
  data: ItineraryResponse;
  variant?: "primary" | "compact";
};

export function GoogleMapsRouteButton({ data, variant = "primary" }: Props) {
  const url = buildGoogleMapsRouteUrl(data);
  if (!url) return null;

  if (variant === "compact") {
    return (
      <a
        href={url}
        target="_blank"
        rel="noopener noreferrer"
        className="inline-flex items-center gap-1.5 text-xs font-semibold text-primary transition-colors hover:text-secondary"
      >
        <MapPin className="h-3.5 w-3.5" aria-hidden />
        Google Maps
        <ExternalLink className="h-3 w-3 opacity-70" aria-hidden />
      </a>
    );
  }

  return (
    <a
      href={url}
      target="_blank"
      rel="noopener noreferrer"
      className="inline-flex w-full items-center justify-center gap-2 rounded-xl border border-primary/30 bg-primary/10 px-4 py-3 text-sm font-semibold text-primary transition-colors hover:border-primary/50 hover:bg-primary/20"
    >
      <MapPin className="h-4 w-4" aria-hidden />
      Open full route in Google Maps
      <ExternalLink className="h-4 w-4 opacity-80" aria-hidden />
    </a>
  );
}
