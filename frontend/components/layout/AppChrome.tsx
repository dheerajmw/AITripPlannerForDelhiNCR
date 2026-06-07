"use client";

import { Suspense, useEffect, useRef } from "react";

import { AuroraBackground } from "@/components/layout/AuroraBackground";
import { TopNav } from "@/components/layout/TopNav";
import { useAppTab } from "@/components/navigation/useAppTab";
import { trackEvent } from "@/lib/analytics";
import { type AppTab, tabToAnalyticsPage } from "@/lib/navigation";

type Props = {
  children: React.ReactNode;
};

function AppChromeInner({ children }: Props) {
  const { tab } = useAppTab();
  const lastTracked = useRef<AppTab | null>(null);

  useEffect(() => {
    if (lastTracked.current === tab) return;
    lastTracked.current = tab;
    trackEvent({ event: "page_view", page: tabToAnalyticsPage(tab) });
  }, [tab]);

  const showAerialBackdrop = tab !== "itinerary";

  return (
    <div className="relative min-h-screen">
      <AuroraBackground showMap={showAerialBackdrop} />
      <TopNav />
      <main className="relative z-10 mx-auto w-full max-w-7xl px-gutter pb-16 pt-[9.25rem] lg:pt-[5.25rem]">
        <div className="page-shell">{children}</div>
      </main>
    </div>
  );
}

/** Purple Aurora shell: cosmic backdrop + floating top nav. */
export function AppChrome({ children }: Props) {
  return (
    <Suspense fallback={null}>
      <AppChromeInner>{children}</AppChromeInner>
    </Suspense>
  );
}
