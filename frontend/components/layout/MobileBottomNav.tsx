"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Bookmark, Map, Search, User } from "lucide-react";

const ITEMS = [
  { href: "/plan", label: "Plan", icon: Map },
  { href: "/", label: "Home", icon: Search },
] as const;

export function MobileBottomNav() {
  const pathname = usePathname();

  return (
    <nav className="fixed bottom-0 left-0 right-0 z-50 flex h-16 items-center justify-around border-t border-outline-variant bg-surface/80 px-4 backdrop-blur-lg md:hidden">
      {ITEMS.map(({ href, label, icon: Icon }) => {
        const active = pathname === href || (href === "/plan" && pathname === "/itinerary");
        return (
          <Link
            key={href}
            href={href}
            className={`flex flex-col items-center justify-center rounded-xl px-4 py-1 transition-all ${
              active
                ? "scale-95 bg-primary-container text-on-primary-container"
                : "text-on-surface-variant hover:text-primary"
            }`}
          >
            <Icon className="h-5 w-5" aria-hidden />
            <span className="text-xs font-medium">{label}</span>
          </Link>
        );
      })}
      <span className="flex flex-col items-center justify-center text-on-surface-variant/50">
        <Bookmark className="h-5 w-5" aria-hidden />
        <span className="text-xs">Saved</span>
      </span>
      <span className="flex flex-col items-center justify-center text-on-surface-variant/50">
        <User className="h-5 w-5" aria-hidden />
        <span className="text-xs">Profile</span>
      </span>
    </nav>
  );
}
