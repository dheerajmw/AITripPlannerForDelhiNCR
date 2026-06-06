"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Bookmark,
  Compass,
  HelpCircle,
  LayoutDashboard,
  PlusCircle,
  Settings,
  Sparkles,
  TrendingUp,
} from "lucide-react";

const NAV = [
  { href: "/", label: "Dashboard", icon: LayoutDashboard, match: (p: string) => p === "/" },
  {
    href: "/plan",
    label: "Generate Trip",
    icon: Sparkles,
    match: (p: string) => p === "/plan",
  },
  {
    href: "/itinerary",
    label: "Saved Trips",
    icon: Bookmark,
    match: (p: string) => p === "/itinerary",
  },
  {
    href: "/",
    label: "Explore Delhi NCR",
    icon: Compass,
    match: () => false,
  },
  {
    href: "/plan",
    label: "AI Insights",
    icon: TrendingUp,
    match: () => false,
  },
] as const;

export function AppSidebar() {
  const pathname = usePathname();

  return (
    <aside className="fixed left-0 top-0 z-50 hidden h-screen w-64 flex-col border-r border-white/10 bg-surface/60 p-6 shadow-sidebar-glow backdrop-blur-xl md:flex">
      <div className="mb-10">
        <h1 className="text-headline-md font-bold tracking-tight text-primary">Trip Pilot</h1>
        <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-on-surface-variant opacity-70">
          AI Navigator
        </p>
      </div>

      <nav className="flex-1 space-y-2">
        {NAV.map(({ href, label, icon: Icon, match }) => {
          const active = match(pathname);
          return (
            <Link
              key={label}
              href={href}
              className={`nav-item active:scale-95 ${active ? "nav-item-active" : ""}`}
            >
              <Icon className="h-5 w-5 shrink-0" aria-hidden />
              <span>{label}</span>
            </Link>
          );
        })}
      </nav>

      <div className="mt-auto space-y-2 border-t border-white/5 pt-6">
        <Link
          href="/plan"
          className="btn-primary mb-4 w-full rounded-lg py-3 text-sm active:scale-95"
        >
          <PlusCircle className="h-4 w-4" aria-hidden />
          New Expedition
        </Link>
        <span className="nav-item cursor-default opacity-60">
          <Settings className="h-5 w-5" aria-hidden />
          <span>Settings</span>
        </span>
        <span className="nav-item cursor-default opacity-60">
          <HelpCircle className="h-5 w-5" aria-hidden />
          <span>Support</span>
        </span>
      </div>
    </aside>
  );
}
