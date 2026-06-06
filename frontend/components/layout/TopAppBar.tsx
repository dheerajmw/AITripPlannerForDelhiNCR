"use client";

import { Bell, Search, User } from "lucide-react";

import { ApiStatusBadge } from "@/components/layout/ApiStatusBadge";

type Props = {
  statusLabel?: string;
};

export function TopAppBar({ statusLabel = "Ready" }: Props) {
  return (
    <header className="sticky top-0 z-40 flex h-16 w-full items-center justify-between bg-gradient-to-b from-background to-transparent px-6 backdrop-blur-sm md:px-10">
      <div className="flex items-center gap-6">
        <span className="hidden text-label-md uppercase tracking-widest text-on-surface-variant sm:inline">
          Status
        </span>
        <span className="border-b-2 border-primary pb-1 text-label-md font-bold uppercase tracking-widest text-primary">
          {statusLabel}
        </span>
        <span className="hidden text-label-md uppercase tracking-widest text-on-surface-variant transition-colors hover:text-on-surface sm:inline">
          Updates
        </span>
      </div>

      <div className="flex items-center gap-4">
        <div className="relative hidden sm:block">
          <input
            type="search"
            placeholder="Search destinations…"
            className="w-48 rounded-full border border-outline-variant/30 bg-surface-container-low/60 py-1.5 pl-4 pr-10 text-sm text-on-surface outline-none transition-all focus:w-64 focus:border-primary focus:ring-2 focus:ring-primary/40"
            readOnly
            aria-label="Search destinations"
          />
          <Search
            className="pointer-events-none absolute right-3 top-1/2 h-4 w-4 -translate-y-1/2 text-on-surface-variant"
            aria-hidden
          />
        </div>
        <ApiStatusBadge compact />
        <button
          type="button"
          className="text-on-surface-variant transition-colors hover:text-primary"
          aria-label="Notifications"
        >
          <Bell className="h-5 w-5" />
        </button>
        <div className="glass-panel flex items-center gap-2 rounded-full px-3 py-1.5">
          <User className="h-5 w-5 text-primary" aria-hidden />
          <span className="hidden text-sm font-medium sm:inline">Explorer</span>
        </div>
      </div>
    </header>
  );
}
