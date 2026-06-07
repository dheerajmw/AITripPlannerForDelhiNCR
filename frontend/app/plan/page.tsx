import { redirect } from "next/navigation";

/** Legacy route — all sections live on the home page. */
export default function PlanPage() {
  redirect("/?tab=plan");
}
