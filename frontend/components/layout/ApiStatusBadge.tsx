"use client";

import { useEffect, useState } from "react";

import { checkHealth, type HealthResponse } from "@/lib/api";

type Status = "loading" | "connected" | "disconnected";

type Props = {
  compact?: boolean;
};

export function ApiStatusBadge({ compact = false }: Props) {
  const [status, setStatus] = useState<Status>("loading");
  const [health, setHealth] = useState<HealthResponse | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function load() {
      try {
        const data = await checkHealth();
        if (!cancelled) {
          setHealth(data);
          setStatus("connected");
        }
      } catch {
        if (!cancelled) setStatus("disconnected");
      }
    }

    load();
    return () => {
      cancelled = true;
    };
  }, []);

  const dotClass =
    status === "connected"
      ? "bg-[#4ade80] pulsing-dot"
      : status === "loading"
        ? "bg-tertiary animate-pulse"
        : "bg-error";

  if (compact) {
    return (
      <div
        className="hidden items-center gap-2 rounded-full border border-outline-variant bg-surface-container-highest px-3 py-1.5 sm:inline-flex"
        role="status"
        aria-live="polite"
      >
        <span className={`h-2 w-2 shrink-0 rounded-full ${dotClass}`} aria-hidden />
        <span className="font-mono text-xs text-on-surface-variant">
          {status === "loading" && "Checking…"}
          {status === "connected" &&
            `API ready${health?.poi_count != null ? ` · ${health.poi_count.toLocaleString()} places` : ""}`}
          {status === "disconnected" && "API offline"}
        </span>
      </div>
    );
  }

  return (
    <div
      className="inline-flex items-center gap-2 rounded-full border border-outline-variant bg-surface-container-highest px-3 py-1.5"
      role="status"
      aria-live="polite"
    >
      <span className={`h-2 w-2 shrink-0 rounded-full ${dotClass}`} aria-hidden />
      <span className="font-mono text-xs text-on-surface-variant">
        {status === "loading" && "Checking API…"}
        {status === "connected" &&
          `API ready${health?.poi_count != null ? ` · ${health.poi_count.toLocaleString()} places` : ""}`}
        {status === "disconnected" && "API disconnected"}
      </span>
    </div>
  );
}
