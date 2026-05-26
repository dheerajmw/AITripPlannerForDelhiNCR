import { AlertTriangle } from "lucide-react";

type WarningsBannerProps = {
  warnings?: string[];
  aiStatus?: string | null;
  fallbackReason?: string | null;
};

export function WarningsBanner({
  warnings = [],
  aiStatus,
  fallbackReason,
}: WarningsBannerProps) {
  const items = [...warnings];

  if (aiStatus === "fallback" && fallbackReason) {
    const hasMsg = items.some((w) => w.toLowerCase().includes("standard plan"));
    if (!hasMsg) {
      items.push(`AI enhancement unavailable (${fallbackReason.replace(/_/g, " ")}).`);
    }
  }

  if (items.length === 0) return null;

  return (
    <div className="flex items-start gap-4 rounded-xl border border-error-container/40 bg-error-container/20 p-4">
      <AlertTriangle className="h-5 w-5 shrink-0 text-error" aria-hidden />
      <div className="min-w-0 flex-1">
        <p className="text-sm font-medium text-on-error-container">Heads up</p>
        <ul className="mt-2 list-inside list-disc space-y-1 text-body-sm text-on-error-container/90">
          {items.map((w, i) => (
            <li key={`${i}-${w.slice(0, 24)}`}>{w}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}
