import Link from "next/link";
import { MapPinOff } from "lucide-react";

type Props = {
  message?: string;
};

export function EmptyItineraryError({
  message = "Generate a plan to see your day itinerary.",
}: Props) {
  return (
    <div className="flex flex-col items-center gap-4 py-16 text-center">
      <MapPinOff className="h-12 w-12 text-on-surface-variant" aria-hidden />
      <h1 className="text-headline-md font-bold text-on-surface">No itinerary yet</h1>
      <p className="max-w-sm text-on-surface-variant">{message}</p>
      <Link href="/plan" className="btn-primary mt-2 px-6 py-3">
        Plan your day
      </Link>
    </div>
  );
}
