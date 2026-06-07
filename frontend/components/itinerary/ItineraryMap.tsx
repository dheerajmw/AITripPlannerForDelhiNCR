"use client";

import dynamic from "next/dynamic";

import { hasGoogleMapsApiKey } from "@/lib/googleMaps";
import type { ItineraryResponse } from "@/types/itinerary";

import { GoogleMapsRouteButton } from "./GoogleMapsRouteButton";

const ItineraryGoogleMapInner = dynamic(() => import("./ItineraryGoogleMapInner"), {
  ssr: false,
  loading: () => (
    <div className="flex h-[320px] items-center justify-center bg-surface-container-highest text-sm text-on-surface-variant">
      Loading Google Maps…
    </div>
  ),
});

const ItineraryMapInner = dynamic(() => import("./ItineraryMapInner"), {
  ssr: false,
  loading: () => (
    <div className="flex h-[320px] items-center justify-center bg-surface-container-highest text-sm text-on-surface-variant">
      Loading your route map…
    </div>
  ),
});

type Props = {
  data: ItineraryResponse;
};

export function ItineraryMap({ data }: Props) {
  const useGoogleEmbed = hasGoogleMapsApiKey();

  return (
    <div className="flex flex-col gap-3 p-4">
      <GoogleMapsRouteButton data={data} />
      {useGoogleEmbed ? (
        <ItineraryGoogleMapInner data={data} />
      ) : (
        <>
          <ItineraryMapInner data={data} />
          <p className="text-center text-caption text-on-surface-variant">
            Add{" "}
            <code className="rounded bg-surface-container-highest px-1 py-0.5 text-[10px]">
              NEXT_PUBLIC_GOOGLE_MAPS_API_KEY
            </code>{" "}
            to enable the embedded Google Map.
          </p>
        </>
      )}
    </div>
  );
}
