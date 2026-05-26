import type {
  ItineraryGenerateBody,
  ItineraryResponse,
} from "@/types/itinerary";

import { API_BASE_URL } from "./constants";

export type { ItineraryGenerateBody, ItineraryResponse } from "@/types/itinerary";

export type HealthResponse = {
  status: string;
  version: string;
  city: string;
  poi_count: number | null;
};

export type ApiErrorBody = {
  error: {
    code: string;
    message: string;
    details?: Record<string, unknown>;
  };
};

export class ApiError extends Error {
  constructor(
    public readonly code: string,
    message: string,
    public readonly status: number,
    public readonly details?: Record<string, unknown>,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

async function parseResponse<T>(response: Response): Promise<T> {
  const text = await response.text();
  const data = text ? (JSON.parse(text) as T | ApiErrorBody) : null;

  if (!response.ok) {
    const err = data as ApiErrorBody | null;
    if (err?.error) {
      throw new ApiError(
        err.error.code,
        err.error.message,
        response.status,
        err.error.details,
      );
    }
    throw new ApiError("HTTP_ERROR", response.statusText, response.status);
  }

  return data as T;
}

export async function checkHealth(): Promise<HealthResponse> {
  const response = await fetch(`${API_BASE_URL}/health`, {
    method: "GET",
    headers: { Accept: "application/json" },
    cache: "no-store",
  });
  return parseResponse<HealthResponse>(response);
}

export async function generateItinerary(
  body: ItineraryGenerateBody,
  mode: "rule" | "ai" = "rule",
): Promise<ItineraryResponse> {
  const params = new URLSearchParams({ mode });
  const response = await fetch(`${API_BASE_URL}/itinerary/generate?${params}`, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });
  return parseResponse<ItineraryResponse>(response);
}
