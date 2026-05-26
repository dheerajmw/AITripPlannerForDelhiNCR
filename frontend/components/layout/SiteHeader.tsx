"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Compass } from "lucide-react";

import { ApiStatusBadge } from "@/components/layout/ApiStatusBadge";
import { APP_NAME } from "@/lib/constants";

const NAV = [
  { href: "/plan", label: "Plan" },
  { href: "/", label: "Home" },
] as const;

export function SiteHeader() {
  const pathname = usePathname();

  return (
    <header className="sticky top-0 z-50 flex h-16 w-full items-center justify-between border-b border-outline-variant glass-panel px-container-mobile md:px-container-desktop">
      <Link href="/" className="flex items-center gap-2">
        <Compass className="h-6 w-6 text-primary" aria-hidden />
        <span className="text-xl font-bold tracking-tight text-primary">{APP_NAME}</span>
      </Link>

      <nav className="hidden items-center gap-6 md:flex">
        {NAV.map(({ href, label }) => (
          <Link
            key={href}
            href={href}
            className={`font-mono text-label-mono transition-colors ${
              pathname === href
                ? "font-bold text-primary"
                : "text-on-surface-variant hover:text-on-surface"
            }`}
          >
            {label}
          </Link>
        ))}
      </nav>

      <ApiStatusBadge compact />
    </header>
  );
}
