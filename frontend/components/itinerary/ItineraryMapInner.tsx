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
    const timer = window.setTimeout(() => {
      map.invalidateSize();
      if (positions.length === 1) {
        map.setView(positions[0], 15);
        return;
      }
      map.fitBounds(L.latLngBounds(positions), { padding: [48, 48], maxZoom: 15 });
    }, 100);
    return () => window.clearTimeout(timer);
  }, [map, positions]);
  return null;
}

function numberedIcon(order: number) {
  return L.divIcon({
    className: "aitp-marker",
    html: `<span class="aitp-marker-pin">${order}</span>`,
    iconSize: [36, 36],
    iconAnchor: [18, 18],
  });
}

type Props = {
  data: ItineraryResponse;
};

export default function ItineraryMapInner({ data }: Props) {
  const [tileErrors, setTileErrors] = useState(0);

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

  const mapKey = data.stops.map((s) => s.poi_id).join("|");

  if (stopPositions.length === 0) {
    return (
      <p className="rounded-2xl border border-outline-variant bg-surface-container-highest p-4 text-center text-sm text-on-surface-variant">
        Map unavailable — no coordinates for stops.
      </p>
    );
  }

  if (tileErrors > 8) {
    return (
      <p className="rounded-2xl border border-outline-variant bg-surface-container-highest p-4 text-center text-sm text-on-surface-variant">
        Map tiles could not load. Your timeline below is still complete.
      </p>
    );
  }

  const center = stopPositions[0] ?? ([28.6129, 77.2295] as [number, number]);

  return (
    <div className="itinerary-map-wrap -mx-0">
      <MapContainer
        key={mapKey}
        center={center}
        zoom={14}
        scrollWheelZoom
        className="itinerary-leaflet-map"
        aria-label="Itinerary map with your stop locations"
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          eventHandlers={{
            tileerror: () => setTileErrors((n) => n + 1),
          }}
        />
        <FitBounds positions={stopPositions} />
        {data.meta.start_point ? (
          <Marker
            position={[data.meta.start_point.lat, data.meta.start_point.lon]}
            icon={L.divIcon({
              className: "aitp-marker",
              html: `<span class="aitp-marker-start">Start</span>`,
              iconAnchor: [24, 12],
            })}
          >
            <Popup>{data.meta.start_point.label}</Popup>
          </Marker>
        ) : null}
        {data.stops.map((stop) => (
          <Marker
            key={stop.poi_id}
            position={[stop.lat, stop.lon]}
            icon={numberedIcon(stop.order)}
          >
            <Popup>
              <strong>
                {stop.order}. {stop.name}
              </strong>
              <br />
              {stop.arrive_at}–{stop.depart_at}
              <br />
              {stop.category}
            </Popup>
          </Marker>
        ))}
        {routePositions.length > 1 ? (
          <Polyline
            positions={routePositions}
            pathOptions={{
              color: "#a078ff",
              weight: 4,
              opacity: 0.9,
              dashArray: "10 8",
            }}
          />
        ) : null}
      </MapContainer>
      <p className="itinerary-map-legend">
        {data.summary.total_stops} stops · OpenStreetMap · zoom/pan to explore your route
      </p>
    </div>
  );
}
