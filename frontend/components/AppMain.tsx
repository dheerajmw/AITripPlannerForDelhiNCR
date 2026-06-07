"use client";

import { HomeView } from "@/components/home/HomeView";
import { ItineraryView } from "@/components/itinerary/ItineraryView";
import { useAppTab } from "@/components/navigation/useAppTab";
import { PlanForm } from "@/components/plan/PlanForm";

export function AppMain() {
  const { tab } = useAppTab();

  switch (tab) {
    case "plan":
      return <PlanForm />;
    case "itinerary":
      return <ItineraryView />;
    default:
      return <HomeView />;
  }
}
