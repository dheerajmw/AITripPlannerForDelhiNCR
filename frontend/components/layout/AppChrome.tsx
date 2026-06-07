"use client";

import { usePathname } from "next/navigation";
import { useEffect, useRef } from "react";

import { AuroraBackground } from "@/components/layout/AuroraBackground";
import { pathnameToPage, trackEvent } from "@/lib/analytics";
import { MobileBottomNav } from "@/components/layout/MobileBottomNav";
import { TopNav } from "@/components/layout/TopNav";

type Props = {
  children: React.ReactNode;
};

/** Purple Aurora shell: cosmic backdrop + floating top nav. */
export function AppChrome({ children }: Props) {
  const pathname = usePathname();
  const lastTracked = useRef<string | null>(null);

  useEffect(() => {
    const page = pathnameToPage(pathname);
    if (!page || lastTracked.current === pathname) return;
    lastTracked.current = pathname;
    trackEvent({ event: "page_view", page });
  }, [pathname]);

  // Aerial Delhi backdrop is decorative only — hide on itinerary so the real OSM map is clear.
  const showAerialBackdrop = pathname !== "/itinerary";

  return (
    <div className="relative min-h-screen">
      <AuroraBackground showMap={showAerialBackdrop} />
      <TopNav />
      <main className="relative z-10 mx-auto max-w-7xl px-gutter pb-28 pt-[7.5rem] md:pb-16">
        {children}
      </main>
      <MobileBottomNav />
    </div>
  );
}
