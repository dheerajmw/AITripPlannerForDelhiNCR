"use client";

import { Bookmark, Compass, Sparkles } from "lucide-react";

import { useAppTab } from "@/components/navigation/useAppTab";
import { APP_TABS } from "@/lib/navigation";

const ICONS = {
  explore: Compass,
  plan: Sparkles,
  itinerary: Bookmark,
} as const;

export function MobileBottomNav() {
  const { tab, setTab } = useAppTab();

  return (
    <nav className="fixed bottom-0 left-0 right-0 z-50 border-t border-on-surface-variant/10 bg-surface/80 backdrop-blur-xl md:hidden">
      <div className="mx-auto flex h-16 w-full max-w-7xl items-center justify-around px-gutter">
        {APP_TABS.map(({ id, shortLabel }) => {
          const Icon = ICONS[id];
          const active = tab === id;
          return (
            <button
              key={id}
              type="button"
              onClick={() => setTab(id)}
              className={`flex flex-col items-center justify-center rounded-xl px-4 py-1 transition-all active:scale-95 ${
                active ? "text-primary" : "text-on-surface-variant hover:text-primary"
              }`}
            >
              <Icon
                className={`h-5 w-5 ${active ? "drop-shadow-[0_0_8px_rgba(208,188,255,0.6)]" : ""}`}
                aria-hidden
              />
              <span className="text-[10px] font-medium">{shortLabel}</span>
            </button>
          );
        })}
      </div>
    </nav>
  );
}
