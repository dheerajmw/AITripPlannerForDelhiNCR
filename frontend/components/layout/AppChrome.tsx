"use client";

import { usePathname } from "next/navigation";

import { AppSidebar } from "@/components/layout/AppSidebar";
import { MobileBottomNav } from "@/components/layout/MobileBottomNav";
import { TopAppBar } from "@/components/layout/TopAppBar";

type Props = {
  children: React.ReactNode;
};

function statusForPath(pathname: string): string {
  if (pathname === "/plan") return "Planning";
  if (pathname === "/itinerary") return "Itinerary";
  return "Ready";
}

/** Night Explorer shell: sidebar + top bar + main canvas. */
export function AppChrome({ children }: Props) {
  const pathname = usePathname();
  const fullBleed = pathname === "/" || pathname === "/plan";

  return (
    <div className="min-h-screen bg-background">
      <AppSidebar />
      <div className="flex min-h-screen flex-col md:ml-64">
        <TopAppBar statusLabel={statusForPath(pathname)} />
        <main
          className={
            fullBleed
              ? "relative flex-1 overflow-hidden pb-24 md:pb-0"
              : "mx-auto w-full max-w-6xl flex-1 px-container-mobile pb-24 pt-4 md:px-container-margin md:pb-12"
          }
        >
          {children}
        </main>
      </div>
      <MobileBottomNav />
    </div>
  );
}
