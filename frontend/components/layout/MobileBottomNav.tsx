"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Bookmark, Compass, Sparkles } from "lucide-react";

const ITEMS = [
  { href: "/", label: "Explore", icon: Compass },
  { href: "/plan", label: "Generate", icon: Sparkles },
  { href: "/itinerary", label: "Saved", icon: Bookmark },
] as const;

export function MobileBottomNav() {
  const pathname = usePathname();

  return (
    <nav className="fixed bottom-0 left-0 right-0 z-50 flex h-16 items-center justify-around border-t border-on-surface-variant/10 bg-surface/80 px-4 backdrop-blur-xl md:hidden">
      {ITEMS.map(({ href, label, icon: Icon }) => {
        const active = pathname === href;
        return (
          <Link
            key={href}
            href={href}
            className={`flex flex-col items-center justify-center rounded-xl px-4 py-1 transition-all active:scale-95 ${
              active ? "text-primary" : "text-on-surface-variant hover:text-primary"
            }`}
          >
            <Icon
              className={`h-5 w-5 ${active ? "drop-shadow-[0_0_8px_rgba(208,188,255,0.6)]" : ""}`}
              aria-hidden
            />
            <span className="text-[10px] font-medium">{label}</span>
          </Link>
        );
      })}
    </nav>
  );
}
