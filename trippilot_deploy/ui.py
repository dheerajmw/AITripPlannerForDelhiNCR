"""HTML layout helpers for Streamlit (mirrors Next.js components)."""

from __future__ import annotations

import html

from trippilot_deploy.theme import HERO_IMAGE, MAP_PREVIEW


def header_html(active: str, poi_count: int | None = None) -> str:
    def link(page: str, label: str, href_page: str) -> str:
        cls = "active" if active == page else ""
        return f'<a class="{cls}" href="?page={href_page}">{label}</a>'

    badge = ""
    if poi_count is not None and poi_count > 0:
        badge = (
            f'<span class="tp-badge"><span class="dot"></span>'
            f"API ready · {poi_count:,} places</span>"
        )
    elif poi_count is not None:
        badge = '<span class="tp-badge">Starting…</span>'

    return f"""
    <div class="tp-header">
      <span class="tp-brand">🧭 TripPilot AI</span>
      <nav class="tp-nav">
        {link("home", "Home", "home")}
        {link("plan", "Plan", "plan")}
        {link("itinerary", "Itinerary", "itinerary")}
      </nav>
      {badge}
    </div>
    """


def hero_home(city: str = "Delhi NCR") -> str:
    return f"""
    <div class="tp-hero mesh">
      <h1>Plan your {html.escape(city)} day in <span class="accent">minutes</span></h1>
      <p>Real OSM places, walking routes, and optional AI tips.</p>
    </div>
    """


def hero_plan() -> str:
    return f"""
    <div class="tp-hero photo" style="background-image: url('{HERO_IMAGE}');">
      <div>
        <h1>Customize Your Trip</h1>
        <p>Tailor your Delhi experience with AI-driven precision. Every route is optimized for
        walking times and your interests.</p>
      </div>
    </div>
    """


def feature_card(icon: str, title: str, text: str, beta: bool = False) -> str:
    beta_html = '<span class="beta-tag">Beta</span>' if beta else ""
    return f"""
    <div class="glass-card feature">
      <div class="feature-icon">{icon}</div>
      <div>
        <h3 style="margin:0;font-size:1.15rem;color:#e7defb!important;">
          {html.escape(title)} {beta_html}
        </h3>
        <p style="margin:0.35rem 0 0;color:#d1c2d2!important;font-size:0.875rem;">
          {html.escape(text)}
        </p>
      </div>
    </div>
    """


def map_preview_block() -> str:
    return f"""
    <div class="glass-card" style="padding:1rem;">
      <div class="map-preview" style="background-image:url('{MAP_PREVIEW}');">
        <div class="label">
          <span>LIVE VIEW</span><br/>
          <span>Connaught Place</span>
        </div>
      </div>
    </div>
    """


def summary_bar_html(meta: dict, summary: dict) -> str:
    hours = round(meta.get("duration_minutes", 0) / 60 * 10) / 10
    cost = summary.get("total_cost_inr", {})
    low = cost.get("low", 0)
    high = cost.get("high", 0)
    ai = ""
    if meta.get("planner_mode") == "ai":
        status = "AI Optimized" if meta.get("ai_status") == "success" else "AI Fallback"
        ai = f'<span style="color:#edb1ff;font-size:0.8rem;">✨ {status}</span>'
    return f"""
    <div class="summary-bar">
      <div style="display:flex;flex-wrap:wrap;align-items:center;gap:0.75rem;">
        <span class="summary-pill">📍 {html.escape(meta.get("city", "Delhi NCR"))}</span>
        <span class="summary-stats">
          <span>🕐 {hours}h</span>
          <span>₹{low:,}–₹{high:,}</span>
          <span>{summary.get("total_stops", 0)} stops</span>
        </span>
      </div>
      {ai}
    </div>
    """


def stop_card_html(stop: dict) -> str:
    cost = stop.get("cost_estimate_inr", {})
    travel = stop.get("travel_to_next_minutes")
    travel_txt = f" · {travel} min to next" if travel is not None else ""
    notes = ""
    if stop.get("notes"):
        notes = f'<div class="stop-notes">✨ {html.escape(stop["notes"])}</div>'
    return f"""
    <div class="stop-card">
      <div>
        <span class="stop-time">{html.escape(stop.get("arrive_at", ""))} – {html.escape(stop.get("depart_at", ""))}</span>
        <span class="stop-cat">{html.escape(stop.get("category", ""))}</span>
        <div class="stop-name">{stop.get("order", "")}. {html.escape(stop.get("name", ""))}</div>
        <div class="stop-meta">
          Visit {stop.get("visit_minutes", 0)}m · ₹{cost.get("low", 0):,}–₹{cost.get("high", 0):,}{travel_txt}
        </div>
      </div>
      {notes}
    </div>
    """
