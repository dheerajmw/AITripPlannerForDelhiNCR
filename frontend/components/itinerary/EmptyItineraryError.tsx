import Link from "next/link";
import { Bookmark, MapPinOff } from "lucide-react";

type Props = {
  message?: string;
};

export function EmptyItineraryError({
  message = "Generate a plan to see your saved expedition.",
}: Props) {
  return (
    <div className="page-narrow flex flex-col items-center gap-6 py-16 text-center">
      <div className="glass-panel w-full rounded-2xl p-12">
        <MapPinOff className="mx-auto h-12 w-12 text-on-surface-variant" aria-hidden />
        <h1 className="mt-4 text-headline-md font-bold text-on-surface">No saved trips yet</h1>
        <p className="mx-auto mt-2 max-w-sm text-on-surface-variant">{message}</p>
        <Link href="/plan" className="btn-primary mt-8 inline-flex px-8 py-3">
          <Bookmark className="h-4 w-4" aria-hidden />
          New Expedition
        </Link>
      </div>
    </div>
  );
}
