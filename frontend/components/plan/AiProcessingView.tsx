"use client";

import { Sparkles } from "lucide-react";

type Props = {
  useAi: boolean;
};

export function AiProcessingView({ useAi }: Props) {
  return (
    <div className="relative flex min-h-[480px] flex-col items-center justify-center py-16">
      <div className="absolute -left-[10%] -top-[10%] h-[40%] w-[40%] animate-pulse-glow rounded-full bg-primary/20 blur-[100px]" />
      <div
        className="absolute -bottom-[10%] -right-[10%] h-[35%] w-[35%] animate-pulse-glow rounded-full bg-secondary/15 blur-[100px]"
        style={{ animationDelay: "2s" }}
      />

      <div className="relative flex h-80 w-80 items-center justify-center">
        <div className="absolute inset-0 animate-pulse-ring rounded-full border-2 border-primary/30" />
        <div
          className="absolute inset-4 animate-pulse-ring rounded-full border-2 border-secondary/20"
          style={{ animationDelay: "1s" }}
        />
        <div className="glass-panel relative z-10 flex h-28 w-28 items-center justify-center rounded-full border border-primary/40 orb-glow">
          <Sparkles className="h-12 w-12 animate-pulse text-primary" aria-hidden />
        </div>
      </div>

      <p className="mt-8 text-center text-headline-md font-bold text-primary">
        {useAi ? "AI Navigator processing…" : "Optimizing your route…"}
      </p>
      <p className="mt-2 text-center text-body-md text-on-surface-variant">
        {useAi ? "Usually 5–20 seconds" : "Matching POIs and walking times"}
      </p>
    </div>
  );
}
