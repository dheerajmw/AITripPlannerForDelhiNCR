"use client";

import { Bookmark, Compass, Sparkles, type LucideIcon } from "lucide-react";

import { useAppTab } from "@/components/navigation/useAppTab";
import { APP_TABS, type AppTab } from "@/lib/navigation";

const TAB_ICONS: Record<AppTab, LucideIcon> = {
  explore: Compass,
  plan: Sparkles,
  itinerary: Bookmark,
};

type Props = {
  className?: string;
  compact?: boolean;
  /** Flush inside the top nav bar — no inner capsule */
  embedded?: boolean;
};

export function TabSegment({
  className = "",
  compact = false,
  embedded = false,
}: Props) {
  const { tab, setTab } = useAppTab();

  return (
    <div
      className={`tab-segment ${embedded ? "tab-segment-embedded" : ""} ${className}`}
      role="tablist"
      aria-label="Trip Pilot sections"
    >
      {APP_TABS.map(({ id, label, shortLabel }) => {
        const active = tab === id;
        const text = compact ? shortLabel : label;
        const Icon = TAB_ICONS[id];
        return (
          <button
            key={id}
            type="button"
            role="tab"
            aria-selected={active}
            onClick={() => setTab(id)}
            className={`tab-segment-btn ${active ? "tab-segment-btn-active" : ""}`}
          >
            <Icon className="tab-segment-icon" aria-hidden />
            <span className="tab-segment-label">{text}</span>
          </button>
        );
      })}
    </div>
  );
}
