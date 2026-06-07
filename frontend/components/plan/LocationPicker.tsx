"use client";

import { MapPin, Search } from "lucide-react";
import { useCallback, useEffect, useId, useRef, useState } from "react";

import {
  DEFAULT_START_LOCATION,
  POPULAR_START_LOCATIONS,
  sameLocation,
  searchLocations,
} from "@/lib/locations";
import type { TripLocation } from "@/types/itinerary";

type Props = {
  value: TripLocation;
  onChange: (location: TripLocation) => void;
  error?: string | null;
};

export function LocationPicker({ value, onChange, error }: Props) {
  const listId = useId();
  const [query, setQuery] = useState(value.label);
  const [suggestions, setSuggestions] = useState<TripLocation[]>([]);
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [localError, setLocalError] = useState<string | null>(null);
  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const wrapRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setQuery(value.label);
  }, [value]);

  useEffect(() => {
    function onDocClick(e: MouseEvent) {
      if (wrapRef.current && !wrapRef.current.contains(e.target as Node)) {
        setOpen(false);
      }
    }
    document.addEventListener("mousedown", onDocClick);
    return () => document.removeEventListener("mousedown", onDocClick);
  }, []);

  const runSearch = useCallback(async (text: string) => {
    const q = text.trim();
    if (q.length < 2) {
      setSuggestions([]);
      return;
    }
    setLoading(true);
    try {
      const items = await searchLocations(q, 8);
      setSuggestions(items);
      setOpen(items.length > 0);
    } finally {
      setLoading(false);
    }
  }, []);

  function onInputChange(text: string) {
    setQuery(text);
    setLocalError(null);
    if (text.trim().toLowerCase() !== value.label.toLowerCase()) {
      onChange({ ...value, label: text, id: "" });
    }
    if (debounceRef.current) clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(() => runSearch(text), 280);
  }

  function selectLocation(loc: TripLocation) {
    onChange(loc);
    setQuery(loc.label);
    setSuggestions([]);
    setOpen(false);
    setLocalError(null);
  }

  function onBlurValidate() {
    if (query.trim().length === 0) {
      setLocalError("Choose a starting location in Delhi NCR.");
      return;
    }
    if (query.trim().toLowerCase() === value.label.toLowerCase() && value.id) {
      setLocalError(null);
      return;
    }
    setLocalError("Select a location from the list — only Delhi NCR places are supported.");
  }

  const displayError = error ?? localError;

  return (
    <div ref={wrapRef} className="space-y-md">
      <div>
        <label htmlFor={`${listId}-input`} className="section-label mb-xs flex items-center gap-2">
          <MapPin className="h-4 w-4" aria-hidden />
          Starting location
        </label>
        <p className="mb-xs text-caption text-on-surface-variant">
          Search landmarks and venues within Delhi NCR only
        </p>
        <div className="relative">
          <Search
            className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-on-surface-variant"
            aria-hidden
          />
          <input
            id={`${listId}-input`}
            type="text"
            role="combobox"
            aria-expanded={open}
            aria-controls={`${listId}-listbox`}
            aria-autocomplete="list"
            autoComplete="off"
            value={query}
            placeholder="e.g. India Gate, Connaught Place…"
            onChange={(e) => onInputChange(e.target.value)}
            onFocus={() => {
              if (suggestions.length > 0) setOpen(true);
            }}
            onBlur={() => {
              window.setTimeout(onBlurValidate, 150);
            }}
            className="w-full rounded-xl border border-outline-variant/40 bg-surface-container-highest/50 py-3 pl-10 pr-4 text-on-surface outline-none transition-colors placeholder:text-on-surface-variant/60 focus:border-primary/50 focus:ring-2 focus:ring-primary/25"
          />
          {loading ? (
            <span className="absolute right-3 top-1/2 -translate-y-1/2 text-caption text-on-surface-variant">
              …
            </span>
          ) : null}
          {open && suggestions.length > 0 ? (
            <ul
              id={`${listId}-listbox`}
              role="listbox"
              className="absolute z-20 mt-1 max-h-56 w-full overflow-auto rounded-xl border border-outline-variant/30 bg-surface-container shadow-glow"
            >
              {suggestions.map((loc) => (
                <li key={loc.id} role="option">
                  <button
                    type="button"
                    className="flex w-full items-start gap-2 px-4 py-3 text-left text-sm text-on-surface transition-colors hover:bg-primary/10"
                    onMouseDown={(e) => e.preventDefault()}
                    onClick={() => selectLocation(loc)}
                  >
                    <MapPin className="mt-0.5 h-4 w-4 shrink-0 text-primary" aria-hidden />
                    <span>
                      {loc.label}
                      <span className="mt-0.5 block text-caption text-on-surface-variant">
                        {loc.source === "landmark" ? "Landmark" : "Venue"} · Delhi NCR
                      </span>
                    </span>
                  </button>
                </li>
              ))}
            </ul>
          ) : null}
        </div>
        {displayError ? (
          <p className="mt-2 text-sm text-error" role="alert">
            {displayError}
          </p>
        ) : null}
      </div>

      <div>
        <span className="section-label mb-xs block">Popular starts</span>
        <div className="flex flex-wrap gap-2">
          {POPULAR_START_LOCATIONS.map((loc) => {
            const active = sameLocation(loc, value);
            return (
              <button
                key={loc.id}
                type="button"
                onClick={() => selectLocation(loc)}
                className={`interest-chip ${
                  active
                    ? "border-primary/30 bg-primary/20 text-primary"
                    : "border-outline-variant/30 bg-surface-container-highest/60 text-on-surface-variant hover:border-primary/40"
                }`}
              >
                {loc.label}
              </button>
            );
          })}
        </div>
      </div>

      {value.id ? (
        <p className="text-caption text-on-surface-variant">
          Route will begin near <span className="text-primary">{value.label}</span>
          {!sameLocation(value, DEFAULT_START_LOCATION) ? "" : " (default)"}
        </p>
      ) : null}
    </div>
  );
}
