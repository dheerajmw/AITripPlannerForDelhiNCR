"use client";

import { MobileBottomNav } from "@/components/layout/MobileBottomNav";
import { SiteHeader } from "@/components/layout/SiteHeader";

type Props = {
  children: React.ReactNode;
};

/** Client shell: header + nav (keeps root layout as a thin server chunk). */
export function AppChrome({ children }: Props) {
  return (
    <>
      <SiteHeader />
      <div className="mx-auto w-full max-w-4xl px-container-mobile pb-28 pt-8 md:px-container-desktop md:pb-12">
        {children}
      </div>
      <MobileBottomNav />
    </>
  );
}
