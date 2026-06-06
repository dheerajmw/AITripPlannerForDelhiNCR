"use client";

import { Sparkles } from "lucide-react";

type Props = {
  useAi: boolean;
};

export function AiProcessingView({ useAi }: Props) {
  return (
    <div className="relative flex min-h-[420px] flex-col items-center justify-center py-16">
      <div className="absolute inset-0 opacity-20" aria-hidden>
        <div className="absolute left-1/4 top-1/4 h-1 w-1 rounded-full bg-white" />
        <div className="absolute left-1/3 top-3/4 h-1 w-1 rounded-full bg-primary" />
        <div className="absolute left-2/3 top-1/2 h-1 w-1 rounded-full bg-secondary" />
      </div>

      <div className="relative flex h-80 w-80 items-center justify-center">
        <div className="absolute inset-0 animate-pulse-ring rounded-full border-2 border-primary/30" />
        <div
          className="absolute inset-4 animate-pulse-ring rounded-full border-2 border-secondary/20"
          style={{ animationDelay: "1s" }}
        />
        <div className="glass-panel relative z-10 flex h-28 w-28 items-center justify-center rounded-full border border-primary/40 glow-cyan">
          <Sparkles className="h-12 w-12 animate-pulse text-primary" aria-hidden />
        </div>
      </div>

      <p className="mt-8 animate-pulse text-center font-bold text-primary">
        {useAi ? "AI Navigator processing…" : "Optimizing your route…"}
      </p>
      <p className="mt-2 text-center text-sm text-on-surface-variant">
        {useAi ? "Usually 5–20 seconds" : "Matching POIs and walking times"}
      </p>
    </div>
  );
}
