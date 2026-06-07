import { API_BASE_URL } from "./constants";

export type AnalyticsPage = "explore" | "plan" | "itinerary";

export type AnalyticsEvent =
  | { event: "page_view"; page: AnalyticsPage }
  | { event: "itinerary_generated"; properties?: { mode: "rule" | "ai" } }
  | { event: "itinerary_viewed" };

const SESSION_KEY = "aitp_analytics_session";

function getSessionId(): string {
  if (typeof sessionStorage === "undefined") return "";
  let id = sessionStorage.getItem(SESSION_KEY);
  if (!id) {
    id =
      typeof crypto !== "undefined" && "randomUUID" in crypto
        ? crypto.randomUUID()
        : `s-${Date.now()}-${Math.random().toString(36).slice(2)}`;
    sessionStorage.setItem(SESSION_KEY, id);
  }
  return id;
}

/** Fire-and-forget anonymous event — never blocks UI. */
export function trackEvent(payload: AnalyticsEvent): void {
  if (typeof window === "undefined") return;

  const body = {
    session_id: getSessionId(),
    ...payload,
    properties:
      "properties" in payload && payload.properties ? payload.properties : undefined,
  };

  const url = `${API_BASE_URL}/analytics/events`;
  const json = JSON.stringify(body);

  if (navigator.sendBeacon) {
    const blob = new Blob([json], { type: "application/json" });
    if (navigator.sendBeacon(url, blob)) return;
  }

  void fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: json,
    keepalive: true,
  }).catch(() => {
    /* analytics must not affect UX */
  });
}

export function pathnameToPage(pathname: string): AnalyticsPage | null {
  if (pathname === "/") return "explore";
  if (pathname === "/plan") return "plan";
  if (pathname === "/itinerary") return "itinerary";
  return null;
}
