"use client";

import Link from "next/link";
import { Bell, PlaneTakeoff } from "lucide-react";

import { TabSegment } from "@/components/navigation/TabSegment";
import { ApiStatusBadge } from "@/components/layout/ApiStatusBadge";

export function TopNav() {
  return (
    <header className="fixed left-0 right-0 top-0 z-50 px-gutter pt-2">
      <div className="mx-auto w-full max-w-7xl space-y-2">
        <div className="tp-nav-bar rounded-full border border-on-surface-variant/10 bg-surface/55 px-4 shadow-nav-glow ring-1 ring-white/5 backdrop-blur-xl sm:px-6 lg:px-6">
          <Link
            href="/"
            className="tp-nav-brand flex shrink-0 items-center gap-2.5"
            scroll={false}
          >
            <span className="flex h-9 w-9 items-center justify-center rounded-full bg-primary/15 ring-1 ring-primary/25">
              <PlaneTakeoff className="h-4 w-4 text-primary" aria-hidden />
            </span>
            <span className="text-base font-bold leading-none tracking-tight text-on-surface sm:text-[1.05rem]">
              Trip Pilot
            </span>
          </Link>

          <div className="tp-nav-tabs hidden lg:block">
            <TabSegment embedded className="w-auto shrink-0" />
          </div>

          <div className="tp-nav-actions flex shrink-0 items-center justify-end gap-2 sm:gap-3">
            <ApiStatusBadge compact />
            <button
              type="button"
              className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full text-on-surface-variant transition-colors hover:bg-white/5 hover:text-primary"
              aria-label="Notifications"
            >
              <Bell className="h-[1.15rem] w-[1.15rem]" aria-hidden />
            </button>
            <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full border border-primary/25 bg-primary/10">
              <span className="text-xs font-bold leading-none text-primary">TP</span>
            </div>
          </div>
        </div>

        <div className="lg:hidden">
          <TabSegment compact />
        </div>
      </div>
    </header>
  );
}
