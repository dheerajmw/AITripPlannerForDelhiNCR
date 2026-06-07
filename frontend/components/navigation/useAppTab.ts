"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { useCallback } from "react";

import {
  type AppTab,
  tabFromSearchParam,
  tabHref,
} from "@/lib/navigation";

export function useAppTab() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const tab = tabFromSearchParam(searchParams.get("tab"));

  const setTab = useCallback(
    (next: AppTab) => {
      router.push(tabHref(next), { scroll: false });
    },
    [router],
  );

  return { tab, setTab };
}
