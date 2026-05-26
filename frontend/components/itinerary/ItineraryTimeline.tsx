import type { ItineraryStop } from "@/types/itinerary";

import { ItineraryStopCard } from "./ItineraryStopCard";
import { TravelLeg } from "./TravelLeg";

type Props = {
  stops: ItineraryStop[];
};

export function ItineraryTimeline({ stops }: Props) {
  return (
    <div className="space-y-0" aria-label="Itinerary stops">
      {stops.map((stop, index) => {
        const badgeVariant = index % 2 === 1 ? "secondary" : "primary";
        const isLast = index === stops.length - 1;

        return (
          <div key={stop.poi_id}>
            <div className="relative pb-8 pl-12">
              {!isLast && <div className="travel-line-dashed top-2" aria-hidden />}
              <div
                className={`absolute left-0 top-0 z-10 flex h-8 w-8 items-center justify-center rounded-full text-sm font-bold ${
                  badgeVariant === "secondary"
                    ? "bg-secondary-container text-on-secondary-container"
                    : "bg-primary-container text-on-primary-container"
                }`}
                aria-hidden
              >
                {stop.order}
              </div>
              <ItineraryStopCard stop={stop} badgeVariant={badgeVariant} />
            </div>
            {stop.travel_to_next_minutes != null && stop.travel_to_next_minutes > 0 ? (
              <TravelLeg minutes={stop.travel_to_next_minutes} />
            ) : null}
          </div>
        );
      })}
    </div>
  );
}
