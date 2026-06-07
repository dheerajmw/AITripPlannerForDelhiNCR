import { describe, expect, it } from "vitest";

import { DEFAULT_START_LOCATION } from "./locations";
import { validatePlanForm } from "./validation";

const validLocation = DEFAULT_START_LOCATION;

describe("validatePlanForm", () => {
  it("accepts valid form", () => {
    const result = validatePlanForm({
      budget: "medium",
      interests: ["history", "nature"],
      duration: "8h",
      location: validLocation,
    });
    expect(result.ok).toBe(true);
    if (result.ok) {
      expect(result.value.interests).toEqual(["history", "nature"]);
      expect(result.value.start_label).toBe(validLocation.label);
      expect(result.value.start_lat).toBe(validLocation.lat);
      expect(result.value.start_lon).toBe(validLocation.lon);
    }
  });

  it("rejects empty interests", () => {
    const result = validatePlanForm({
      budget: "low",
      interests: [],
      duration: "4h",
      location: validLocation,
    });
    expect(result.ok).toBe(false);
  });

  it("rejects invalid budget", () => {
    const result = validatePlanForm({
      budget: "luxury",
      interests: ["food"],
      duration: "8h",
      location: validLocation,
    });
    expect(result.ok).toBe(false);
  });

  it("rejects invalid duration", () => {
    const result = validatePlanForm({
      budget: "high",
      interests: ["food"],
      duration: "2h",
      location: validLocation,
    });
    expect(result.ok).toBe(false);
  });

  it("filters unknown interests", () => {
    const result = validatePlanForm({
      budget: "medium",
      interests: ["history", "invalid"],
      duration: "1d",
      location: validLocation,
    });
    expect(result.ok).toBe(true);
    if (result.ok) {
      expect(result.value.interests).toEqual(["history"]);
    }
  });

  it("rejects unselected location", () => {
    const result = validatePlanForm({
      budget: "medium",
      interests: ["history"],
      duration: "8h",
      location: { ...validLocation, id: "" },
    });
    expect(result.ok).toBe(false);
    if (!result.ok) {
      expect(result.message).toMatch(/Delhi NCR/i);
    }
  });

  it("rejects location outside NCR bounds", () => {
    const result = validatePlanForm({
      budget: "medium",
      interests: ["history"],
      duration: "8h",
      location: {
        id: "landmark:mumbai",
        label: "Gateway of India",
        lat: 18.922,
        lon: 72.8347,
        source: "landmark",
      },
    });
    expect(result.ok).toBe(false);
    if (!result.ok) {
      expect(result.message).toMatch(/outside Delhi NCR/i);
    }
  });
});
