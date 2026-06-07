import { redirect } from "next/navigation";

/** Legacy route — all sections live on the home page. */
export default function ItineraryPage() {
  redirect("/?tab=itinerary");
}
