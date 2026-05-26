import { describe, expect, it } from "vitest";

import { validatePlanForm } from "./validation";

describe("validatePlanForm", () => {
  it("accepts valid form", () => {
    const result = validatePlanForm({
      budget: "medium",
      interests: ["history", "nature"],
      duration: "8h",
    });
    expect(result.ok).toBe(true);
    if (result.ok) {
      expect(result.value.interests).toEqual(["history", "nature"]);
    }
  });

  it("rejects empty interests", () => {
    const result = validatePlanForm({
      budget: "low",
      interests: [],
      duration: "4h",
    });
    expect(result.ok).toBe(false);
  });

  it("rejects invalid budget", () => {
    const result = validatePlanForm({
      budget: "luxury",
      interests: ["food"],
      duration: "8h",
    });
    expect(result.ok).toBe(false);
  });

  it("rejects invalid duration", () => {
    const result = validatePlanForm({
      budget: "high",
      interests: ["food"],
      duration: "2h",
    });
    expect(result.ok).toBe(false);
  });

  it("filters unknown interests", () => {
    const result = validatePlanForm({
      budget: "medium",
      interests: ["history", "invalid"],
      duration: "1d",
    });
    expect(result.ok).toBe(true);
    if (result.ok) {
      expect(result.value.interests).toEqual(["history"]);
    }
  });
});
