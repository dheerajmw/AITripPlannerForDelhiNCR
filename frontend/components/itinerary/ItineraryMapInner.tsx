"use client";

import { useEffect, useMemo, useState } from "react";
import L from "leaflet";
import { MapContainer, Marker, Polyline, Popup, TileLayer, useMap } from "react-leaflet";

import type { ItineraryResponse } from "@/types/itinerary";

import "leaflet/dist/leaflet.css";

function FitBounds({ positions }: { positions: [number, number][] }) {
  const map = useMap();
  useEffect(() => {
    if (positions.length === 0) return;
    if (positions.length === 1) {
      map.setView(positions[0], 14);
      return;
    }
    map.fitBounds(L.latLngBounds(positions), { padding: [40, 40] });
  }, [map, positions]);
  return null;
}

function numberedIcon(order: number, variant: "primary" | "secondary") {
  const bg = variant === "secondary" ? "#00a29a" : "#9d50bb";
  const fg = variant === "secondary" ? "#00302d" : "#fff3fd";
  return L.divIcon({
    className: "aitp-marker",
    html: `<span style="
      display:flex;align-items:center;justify-content:center;
      width:32px;height:32px;border-radius:50%;
      background:${bg};color:${fg};font-weight:700;font-size:13px;
      border:2px solid #151024;box-shadow:0 4px 12px rgba(0,0,0,.4);
    ">${order}</span>`,
    iconSize: [32, 32],
    iconAnchor: [16, 16],
  });
}

type Props = {
  data: ItineraryResponse;
};

export default function ItineraryMapInner({ data }: Props) {
  const [mapFailed, setMapFailed] = useState(false);

  const stopPositions = useMemo(
    () =>
      data.stops
        .filter((s) => Number.isFinite(s.lat) && Number.isFinite(s.lon))
        .map((s) => [s.lat, s.lon] as [number, number]),
    [data.stops],
  );

  const routePositions = useMemo(() => {
    const points: [number, number][] = [];
    if (data.meta.start_point) {
      points.push([data.meta.start_point.lat, data.meta.start_point.lon]);
    }
    points.push(...stopPositions);
    return points;
  }, [data.meta.start_point, stopPositions]);

  if (stopPositions.length === 0) {
    return (
      <p className="rounded-2xl border border-outline-variant bg-surface-container-highest p-4 text-center text-sm text-on-surface-variant">
        Map unavailable — no coordinates for stops.
      </p>
    );
  }

  if (mapFailed) {
    return (
      <p className="rounded-2xl border border-outline-variant bg-surface-container-highest p-4 text-center text-sm text-on-surface-variant">
        Map tiles could not load. Your timeline below is still complete.
      </p>
    );
  }

  const center = stopPositions[0] ?? ([28.6129, 77.2295] as [number, number]);

  return (
    <section className="relative h-64 overflow-hidden rounded-2xl border border-outline-variant bg-surface-container-highest md:h-80">
      <MapContainer
        center={center}
        zoom={13}
        scrollWheelZoom={false}
        className="h-full w-full"
        aria-label="Itinerary map"
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          eventHandlers={{ tileerror: () => setMapFailed(true) }}
        />
        <FitBounds positions={stopPositions} />
        {data.meta.start_point ? (
          <Marker
            position={[data.meta.start_point.lat, data.meta.start_point.lon]}
            icon={L.divIcon({
              className: "aitp-start",
              html: `<span style="font-size:10px;color:#5dd9d0;font-weight:600;">Start</span>`,
              iconAnchor: [20, 10],
            })}
          >
            <Popup>{data.meta.start_point.label}</Popup>
          </Marker>
        ) : null}
        {data.stops.map((stop, index) => (
          <Marker
            key={stop.poi_id}
            position={[stop.lat, stop.lon]}
            icon={numberedIcon(stop.order, index % 2 === 1 ? "secondary" : "primary")}
          >
            <Popup>
              <strong>{stop.name}</strong>
              <br />
              {stop.arrive_at}–{stop.depart_at}
            </Popup>
          </Marker>
        ))}
        {routePositions.length > 1 ? (
          <Polyline
            positions={routePositions}
            pathOptions={{ color: "#5dd9d0", weight: 3, opacity: 0.75, dashArray: "8 10" }}
          />
        ) : null}
      </MapContainer>
      <div className="pointer-events-none absolute inset-0 bg-gradient-to-t from-background/60 via-transparent to-transparent" />
    </section>
  );
}
