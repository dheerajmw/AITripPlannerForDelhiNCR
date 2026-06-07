import { Suspense } from "react";

import { AppMain } from "@/components/AppMain";

export default function Home() {
  return (
    <Suspense fallback={null}>
      <AppMain />
    </Suspense>
  );
}
