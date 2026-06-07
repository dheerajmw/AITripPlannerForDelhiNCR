"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Bell, PlaneTakeoff } from "lucide-react";

import { ApiStatusBadge } from "@/components/layout/ApiStatusBadge";

const NAV = [
  { href: "/", label: "Explore" },
  { href: "/plan", label: "Generate Trip" },
  { href: "/itinerary", label: "Saved Trips" },
] as const;

export function TopNav() {
  const pathname = usePathname();

  return (
    <nav className="fixed left-0 right-0 top-0 z-50 px-gutter pt-2">
      <div className="mx-auto flex max-w-7xl items-center justify-between rounded-full border border-on-surface-variant/10 bg-surface/40 px-6 py-3 shadow-nav-glow backdrop-blur-xl md:px-10">
        <Link href="/" className="flex items-center gap-2">
          <PlaneTakeoff className="h-5 w-5 text-primary" aria-hidden />
          <span className="text-headline-md font-bold text-primary">Trip Pilot</span>
        </Link>

        <div className="hidden items-center gap-8 md:flex">
          {NAV.map(({ href, label }) => {
            const active =
              pathname === href ||
              (href === "/itinerary" && pathname.startsWith("/itinerary"));
            return (
              <Link
                key={href}
                href={href}
                className={active ? "nav-link-active" : "nav-link"}
              >
                {label}
              </Link>
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
    </nav>
  );
}
