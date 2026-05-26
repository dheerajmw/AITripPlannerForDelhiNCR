"use client";

import dynamic from "next/dynamic";

import type { ItineraryResponse } from "@/types/itinerary";

const ItineraryMapInner = dynamic(() => import("./ItineraryMapInner"), {
  ssr: false,
  loading: () => (
    <div className="flex h-64 items-center justify-center rounded-2xl border border-[#2a3441] bg-[#12181f] text-sm text-[#9aa8b8] sm:h-72">
      Loading map…
    </div>
  ),
});

type Props = {
  data: ItineraryResponse;
};

export function ItineraryMap({ data }: Props) {
  return <ItineraryMapInner data={data} />;
}
