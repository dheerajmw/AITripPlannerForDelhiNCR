"""HTML layout helpers for Streamlit (Purple Aurora — matches Next.js frontend)."""

from __future__ import annotations

import html
from typing import Any
from urllib.parse import urlencode

from trippilot_deploy.theme import HERO_IMAGE

def aurora_background_html(*, show_map: bool = True) -> str:
    map_div = ""
    if show_map:
        map_div = (
            f'<div class="tp-aurora-map" style="background-image:url(\'{HERO_IMAGE}\')"></div>'
        )
    return f"""
    <div class="tp-aurora" aria-hidden="true">
      <div class="tp-aurora-blob-1"></div>
      <div class="tp-aurora-blob-2"></div>
      {map_div}
    </div>
    """


def top_nav_html(poi_count: int | None = None) -> str:
    badge = ""
    if poi_count is not None and poi_count > 0:
        badge = (
            f'<span class="tp-nav-badge"><span class="dot"></span>'
            f'{poi_count:,} POIs</span>'
        )

    return f"""
    <div class="tp-header-fixed" aria-hidden="false">
      <div class="tp-header-inner">
        <div class="tp-topnav">
          <span class="tp-brand">✈ Trip Pilot</span>
          <div class="tp-nav-actions">
            {badge}
            <div class="tp-avatar">TP</div>
          </div>
        </div>
      </div>
    </div>
    """


def home_page_html(city: str = "Delhi NCR") -> str:
    return f"""
    <div class="tp-page-shell">
      <div class="hero-center">
        <div class="hero-orb"><span class="hero-orb-glow"></span>✨</div>
        <h1>Explore <span class="aurora-text">{html.escape(city)}</span><br/>with AI</h1>
        <p>Experience the fusion of historic majesty and futuristic convenience. Our AI crafts
        seamless itineraries tailored to your unique pace and passions.</p>
      </div>
      <div class="tp-page-narrow">
        {quick_plan_card()}
      </div>
      {bento_grid_html()}
      <p class="footer-note">Estimates only · MVP · No bookings or tickets</p>
    </div>
    """


def hero_plan() -> str:
    return """
    <div class="hero-plan-compact">
      <div class="hero-orb hero-orb-sm" aria-hidden="true">✨</div>
      <h1>Generate Your <span class="aurora-text">Expedition</span></h1>
      <p>Tailor your Delhi NCR experience with AI-driven precision. Every route is optimized
      for walking times and your interests.</p>
    </div>
    """


def quick_plan_card() -> str:
    return """
    <div class="glass-panel quick-plan-card">
      <p class="preview-note">Example trip preferences · customize on the next step</p>
      <div class="quick-plan-grid">
        <div>
          <span class="field-label">📍 Destination</span>
          <span class="preview-chip preview-chip-active">Delhi NCR</span>
        </div>
        <div>
          <span class="field-label">Duration</span>
          <div class="chip-row">
            <span class="preview-chip preview-chip-muted">4h</span>
            <span class="preview-chip preview-chip-active">8h</span>
            <span class="preview-chip preview-chip-muted">1 day</span>
          </div>
        </div>
        <div>
          <span class="field-label">Interests</span>
          <div class="chip-row">
            <span class="preview-chip preview-chip-active">Food</span>
            <span class="preview-chip preview-chip-active">History</span>
            <span class="preview-chip preview-chip-active">Nature</span>
          </div>
        </div>
        <div>
          <span class="field-label">Budget</span>
          <div class="chip-row">
            <span class="preview-chip preview-chip-muted">Low</span>
            <span class="preview-chip preview-chip-active">Medium</span>
            <span class="preview-chip preview-chip-muted">High</span>
          </div>
        </div>
      </div>
    </div>
    """


def bento_grid_html() -> str:
    return """
    <div class="bento-grid">
      <div class="glass-card bento-card bento-wide">
        <span class="bento-tag">Exclusive Access</span>
        <h3>Curated Dining at Taj</h3>
        <p>AI identified lower wait times for window seats at Varq tonight.</p>
      </div>
      <div class="glass-card bento-card bento-stats">
        <div class="bento-icon">✨</div>
        <h3>Live Insights</h3>
        <div class="stat-row"><span>Crowd: GK-II</span><span class="secondary">Low</span></div>
        <div class="stat-bar"><div class="stat-fill secondary" style="width:30%"></div></div>
        <div class="stat-row"><span>Traffic: Cyber Hub</span><span class="error">High</span></div>
        <div class="stat-bar"><div class="stat-fill error" style="width:85%"></div></div>
      </div>
      <div class="glass-card bento-card bento-sm">
        <span class="bento-icon">🚕</span>
        <h4>Premium Transit</h4>
        <p>Zero-wait travel coordinated with your AI itinerary.</p>
      </div>
      <div class="glass-card bento-card bento-sm">
        <span class="bento-icon">🏛️</span>
        <h4>Historical Walk</h4>
        <p>AI audio guide for Lodhi Gardens at your pace.</p>
      </div>
      <div class="glass-card bento-card bento-sm">
        <span class="bento-icon">🎭</span>
        <h4>Late Night Arts</h4>
        <p>Immersive theater — AI recommends tickets.</p>
      </div>
    </div>
    """


def google_maps_route_url(data: dict[str, Any]) -> str | None:
    points: list[tuple[float, float]] = []
    start = data.get("meta", {}).get("start_point")
    if start:
        points.append((float(start["lat"]), float(start["lon"])))
    for stop in data.get("stops") or []:
        if stop.get("lat") is not None and stop.get("lon") is not None:
            points.append((float(stop["lat"]), float(stop["lon"])))
    if not points:
        return None
    if len(points) == 1:
        lat, lon = points[0]
        params = urlencode({"api": "1", "query": f"{lat},{lon}"})
        return f"https://www.google.com/maps/search/?{params}"
    origin = f"{points[0][0]},{points[0][1]}"
    dest = f"{points[-1][0]},{points[-1][1]}"
    middle = points[1:-1][:9]
    params: dict[str, str] = {
        "api": "1",
        "origin": origin,
        "destination": dest,
        "travelmode": "walking",
    }
    if middle:
        params["waypoints"] = "|".join(f"{lat},{lon}" for lat, lon in middle)
    return f"https://www.google.com/maps/dir/?{urlencode(params)}"


def expedition_hero_html(meta: dict, summary: dict) -> str:
    hours = round(meta.get("duration_minutes", 0) / 60 * 10) / 10
    cost = summary.get("total_cost_inr", {})
    low = cost.get("low", 0)
    high = cost.get("high", 0)
    budget = html.escape(str(meta.get("budget_tier", "medium")))
    city = html.escape(str(meta.get("city", "Delhi NCR")))
    start = meta.get("start_point", {})
    start_label = html.escape(str(start.get("label", meta.get("city", "Delhi NCR"))))

    ai_pill = ""
    if meta.get("planner_mode") == "ai":
        status = "AI enhanced" if meta.get("ai_status") == "success" else "AI fallback"
        ai_pill = f'<span class="expedition-ai-pill">✨ {status}</span>'

    return f"""
    <div class="itinerary-shell">
      <div class="expedition-hero glass-panel">
        <div class="expedition-hero-top">
          <span class="expedition-location-pill">📍 {start_label}</span>
          {ai_pill}
        </div>
        <h1 class="expedition-title">Your expedition</h1>
        <div class="expedition-metrics">
          <div class="expedition-metric">
            <span class="expedition-metric-icon">🕐</span>
            <span class="expedition-metric-value">{hours}h</span>
            <span class="expedition-metric-label">Duration</span>
          </div>
          <div class="expedition-metric">
            <span class="expedition-metric-icon">₹</span>
            <span class="expedition-metric-value">₹{low:,}–₹{high:,}</span>
            <span class="expedition-metric-label">Est. cost</span>
          </div>
          <div class="expedition-metric">
            <span class="expedition-metric-icon">✨</span>
            <span class="expedition-metric-value">{summary.get("total_stops", 0)}</span>
            <span class="expedition-metric-label">Stops</span>
          </div>
          <div class="expedition-metric">
            <span class="expedition-metric-icon">🚶</span>
            <span class="expedition-metric-value">{summary.get("total_travel_min", 0)} min</span>
            <span class="expedition-metric-label">Walking</span>
          </div>
        </div>
        <p class="expedition-meta">{budget} budget · {city}</p>
      </div>
    </div>
    """


def itinerary_header_block(meta: dict, summary: dict) -> str:
    """Unified expedition hero — single markdown block for Streamlit."""
    return expedition_hero_html(meta, summary)


def map_shell_open() -> str:
    return '<div class="map-shell"><p class="map-label">Live Route</p>'


def map_shell_close() -> str:
    return "</div>"


def stats_panel_html(meta: dict, summary: dict) -> str:
    cost = summary.get("total_cost_inr", {})
    routing = meta.get("routing_source") or "planner"
    return f"""
    <div class="glass-panel stats-panel">
      <h3>Pilot intelligence</h3>
      <div class="stats-grid">
        <div class="stat-box">
          <p class="stat-label">Travel</p>
          <p class="stat-value">{summary.get("total_travel_min", 0)} min</p>
        </div>
        <div class="stat-box">
          <p class="stat-label">Est. cost</p>
          <p class="stat-value">₹{cost.get("low", 0):,}–{cost.get("high", 0):,}</p>
        </div>
        <div class="stat-box stat-wide">
          <p class="stat-tip-title">✨ Routing</p>
          <p class="stat-tip">Via {html.escape(routing)}. Costs are rough estimates —
          not bookings or tickets.</p>
        </div>
      </div>
    </div>
    """


def stop_card_html(stop: dict) -> str:
    cost = stop.get("cost_estimate_inr", {})
    travel = stop.get("travel_to_next_minutes")
    travel_txt = f" · {travel} min to next" if travel else ""
    lat, lon = stop.get("lat"), stop.get("lon")
    gmaps = ""
    if lat is not None and lon is not None:
        q = urlencode({"api": "1", "query": f"{stop.get('name', '')}@{lat},{lon}"})
        gmaps = (
            f' · <a href="https://www.google.com/maps/search/?{q}" '
            f'target="_blank" rel="noopener" style="color:#d0bcff;">Google Maps</a>'
        )
    notes = ""
    if stop.get("notes"):
        notes = f'<div class="stop-notes">✨ {html.escape(stop["notes"])}</div>'
    return f"""
    <div class="stop-card">
      <span class="stop-time">{html.escape(stop.get("arrive_at", ""))} – {html.escape(stop.get("depart_at", ""))}</span>
      <span class="stop-cat">{html.escape(stop.get("category", ""))}</span>
      <div class="stop-name">{stop.get("order", "")}. {html.escape(stop.get("name", ""))}</div>
      <div class="stop-meta">
        Visit {stop.get("visit_minutes", 0)}m · ₹{cost.get("low", 0):,}–{cost.get("high", 0):,}{travel_txt}{gmaps}
      </div>
      {notes}
    </div>
    """


def empty_itinerary_html() -> str:
    return """
    <div class="glass-panel empty-state">
      <p class="empty-icon">📍</p>
      <h2>No saved trips yet</h2>
      <p>Generate a plan to see your expedition itinerary.</p>
    </div>
    """
