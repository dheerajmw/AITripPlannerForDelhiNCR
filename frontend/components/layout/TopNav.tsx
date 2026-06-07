"use client";

import Link from "next/link";
import { Bell, PlaneTakeoff } from "lucide-react";

import { useAppTab } from "@/components/navigation/useAppTab";
import { ApiStatusBadge } from "@/components/layout/ApiStatusBadge";
import { APP_TABS } from "@/lib/navigation";

export function TopNav() {
  const { tab, setTab } = useAppTab();

  return (
    <nav className="fixed left-0 right-0 top-0 z-50 px-gutter pt-2">
      <div className="mx-auto w-full max-w-7xl">
        <div className="flex w-full items-center justify-between rounded-full border border-on-surface-variant/10 bg-surface/40 px-6 py-3 shadow-nav-glow backdrop-blur-xl md:px-10">
          <Link href="/" className="flex items-center gap-2" scroll={false}>
            <PlaneTakeoff className="h-5 w-5 text-primary" aria-hidden />
            <span className="text-headline-md font-bold text-primary">Trip Pilot</span>
          </Link>

          <div className="hidden items-center gap-8 md:flex">
            {APP_TABS.map(({ id, label }) => {
              const active = tab === id;
              return (
                <button
                  key={id}
                  type="button"
                  onClick={() => setTab(id)}
                  className={active ? "nav-link-active" : "nav-link"}
                >
                  {label}
                </button>
              );
            })}
          </div>

          <div className="flex items-center gap-3">
            <ApiStatusBadge compact />
            <button
              type="button"
              className="hidden text-on-surface-variant transition-colors hover:text-primary sm:block"
              aria-label="Notifications"
            >
              <Bell className="h-5 w-5" />
            </button>
            <div className="flex h-10 w-10 items-center justify-center overflow-hidden rounded-full border-2 border-primary/30 bg-surface-container-high">
              <span className="text-sm font-bold text-primary">TP</span>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}
