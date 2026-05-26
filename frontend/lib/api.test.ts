import { afterEach, describe, expect, it, vi } from "vitest";

import { ApiError, checkHealth } from "./api";

describe("checkHealth", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("returns health payload when API is ok", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        status: 200,
        text: async () =>
          JSON.stringify({
            status: "ok",
            version: "0.1.0",
            city: "Delhi NCR",
            poi_count: null,
          }),
      }),
    );

    const health = await checkHealth();
    expect(health.status).toBe("ok");
    expect(health.city).toBe("Delhi NCR");
  });

  it("throws ApiError on failure response", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: false,
        status: 503,
        statusText: "Service Unavailable",
        text: async () =>
          JSON.stringify({
            error: {
              code: "SERVICE_UNAVAILABLE",
              message: "Planner temporarily unavailable",
            },
          }),
      }),
    );

    await expect(checkHealth()).rejects.toBeInstanceOf(ApiError);
    await expect(checkHealth()).rejects.toMatchObject({
      code: "SERVICE_UNAVAILABLE",
      status: 503,
    });
  });
});
