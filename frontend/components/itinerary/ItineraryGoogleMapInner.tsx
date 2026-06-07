"use client";

import {
  APIProvider,
  Map,
  Marker,
  useMap,
  useMapsLibrary,
} from "@vis.gl/react-google-maps";
import { useEffect, useMemo } from "react";

import { GOOGLE_MAPS_API_KEY, collectRoutePoints } from "@/lib/googleMaps";
import type { ItineraryResponse } from "@/types/itinerary";

const DEFAULT_CENTER = { lat: 28.6129, lng: 77.2295 };

function FitRouteBounds({ positions }: { positions: google.maps.LatLngLiteral[] }) {
  const map = useMap();
  const core = useMapsLibrary("core");

  useEffect(() => {
    if (!map || !core || positions.length === 0) return;
    const timer = window.setTimeout(() => {
      if (positions.length === 1) {
        map.setCenter(positions[0]);
        map.setZoom(15);
        return;
      }
      const bounds = new core.LatLngBounds();
      for (const p of positions) bounds.extend(p);
      map.fitBounds(bounds, 48);
    }, 120);
    return () => window.clearTimeout(timer);
  }, [map, core, positions]);

  return null;
}

function RoutePolyline({ positions }: { positions: google.maps.LatLngLiteral[] }) {
  const map = useMap();
  const maps = useMapsLibrary("maps");

  useEffect(() => {
    if (!map || !maps || positions.length < 2) return;
    const line = new maps.Polyline({
      path: positions,
      strokeColor: "#a078ff",
      strokeOpacity: 0.9,
      strokeWeight: 4,
      geodesic: true,
    });
    line.setMap(map);
    return () => line.setMap(null);
  }, [map, maps, positions]);

  return null;
}

type Props = {
  data: ItineraryResponse;
};

export default function ItineraryGoogleMapInner({ data }: Props) {
  const routePoints = useMemo(() => collectRoutePoints(data), [data]);
  const mapPositions = useMemo(
    () => routePoints.map((p) => ({ lat: p.lat, lng: p.lon })),
    [routePoints],
  );
  const stopPositions = useMemo(
    () =>
      data.stops
        .filter((s) => Number.isFinite(s.lat) && Number.isFinite(s.lon))
        .map((s) => ({ lat: s.lat, lng: s.lon })),
    [data.stops],
  );

  const mapKey = data.stops.map((s) => s.poi_id).join("|");
  const center = mapPositions[0] ?? DEFAULT_CENTER;

  if (stopPositions.length === 0) {
    return (
      <p className="rounded-2xl border border-outline-variant bg-surface-container-highest p-4 text-center text-sm text-on-surface-variant">
        Map unavailable — no coordinates for stops.
      </p>
    );
  }

  return (
    <div className="itinerary-map-wrap">
      <APIProvider apiKey={GOOGLE_MAPS_API_KEY}>
        <Map
          key={mapKey}
          defaultCenter={center}
          defaultZoom={14}
          gestureHandling="greedy"
          disableDefaultUI={false}
          mapTypeControl={false}
          fullscreenControl
          className="itinerary-google-map"
          aria-label="Google Maps view of your itinerary route"
        >
          <FitRouteBounds positions={mapPositions} />
          <RoutePolyline positions={mapPositions} />
          {data.meta.start_point ? (
            <Marker
              position={{
                lat: data.meta.start_point.lat,
                lng: data.meta.start_point.lon,
              }}
              title={data.meta.start_point.label}
              label={{ text: "S", color: "#fff", fontWeight: "700" }}
            />
          ) : null}
          {data.stops.map((stop) => (
            <Marker
              key={stop.poi_id}
              position={{ lat: stop.lat, lng: stop.lon }}
              title={stop.name}
              label={{
                text: String(stop.order),
                color: "#fff",
                fontWeight: "700",
              }}
            />
          ))}
        </Map>
      </APIProvider>
      <p className="itinerary-map-legend">
        {data.summary.total_stops} stops · Google Maps · zoom/pan to explore your route
      </p>
    </div>
  );
}
