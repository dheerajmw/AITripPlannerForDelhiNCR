/** Public configuration — no secrets in this file. */

/**
 * Default `/api/v1` uses Next.js rewrite → backend (see next.config.ts).
 * Override with NEXT_PUBLIC_API_URL if the API is on another host.
 */
export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "/api/v1";

export const APP_NAME = "TripPilot AI";
export const DEFAULT_CITY = "Delhi NCR";
