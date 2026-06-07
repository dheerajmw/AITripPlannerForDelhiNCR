import type { AnalyticsPage } from "./analytics";

export type AppTab = "explore" | "plan" | "itinerary";

export const APP_TABS: { id: AppTab; label: string; shortLabel: string }[] = [
  { id: "explore", label: "Explore", shortLabel: "Explore" },
  { id: "plan", label: "Generate Trip", shortLabel: "Generate" },
  { id: "itinerary", label: "Saved Trips", shortLabel: "Saved" },
];

export const DEFAULT_TAB: AppTab = "explore";

export function tabFromSearchParam(value: string | null | undefined): AppTab {
  if (value === "plan" || value === "itinerary") return value;
  return DEFAULT_TAB;
}

/** Same-page URL — all sections live on `/` with an optional `tab` query. */
export function tabHref(tab: AppTab): string {
  if (tab === DEFAULT_TAB) return "/";
  return `/?tab=${tab}`;
}

export function tabToAnalyticsPage(tab: AppTab): AnalyticsPage {
  if (tab === "explore") return "explore";
  return tab;
}
