"""HTML layout helpers for Streamlit (Night Explorer / stitch_trip_pilot_ai_planner)."""

from __future__ import annotations

import html

from trippilot_deploy.theme import HERO_IMAGE, NIGHTSCAPE_IMAGE

NAV_ITEMS = [
    ("home", "Dashboard", "📊"),
    ("plan", "Generate Trip", "✨"),
    ("itinerary", "Saved Trips", "🔖"),
]


def sidebar_html(active: str, poi_count: int | None = None) -> str:
    items = []
    for page, label, icon in NAV_ITEMS:
        cls = "nav-item-active" if active == page else ""
        items.append(
            f'<a class="nav-item {cls}" href="?page={page}">'
            f'<span>{icon}</span><span>{html.escape(label)}</span></a>'
        )
    nav = "\n".join(items)

    badge = ""
    if poi_count is not None and poi_count > 0:
        badge = (
            f'<p class="sidebar-badge">'
            f'<span class="dot"></span> {poi_count:,} places loaded</p>'
        )

    return f"""
    <aside class="tp-sidebar">
      <div class="sidebar-brand">
        <h1>Trip Pilot</h1>
        <p>AI Navigator</p>
      </div>
      <nav class="sidebar-nav">{nav}</nav>
      {badge}
      <a class="btn-sidebar-cta" href="?page=plan">＋ New Expedition</a>
    </aside>
    """


def top_bar_html(status: str = "Ready", active: str = "home") -> str:
    nav_links = []
    for page, label, _icon in NAV_ITEMS:
        short = label.split()[0]
        cls = "active" if active == page else ""
        nav_links.append(
            f'<a class="{cls}" href="?page={page}">{html.escape(short)}</a>'
        )
    mobile_nav = '<div class="tp-mobile-nav">' + "".join(nav_links) + "</div>"
    return f"""
    <div class="tp-topbar">
      <div class="tp-topbar-left">
        <span class="tp-status-label">Status</span>
        <span class="tp-status-active">{html.escape(status)}</span>
      </div>
      <div class="tp-topbar-right">
        <span class="tp-search">Search destinations…</span>
      </div>
      {mobile_nav}
    </div>
    """


def home_page_html(city: str = "Delhi NCR") -> str:
    """Single HTML block for dashboard — Streamlit renders one markdown block reliably."""
    return (
        hero_explore(city)
        + '<div style="padding:0 1.5rem;">'
        + quick_plan_card()
        + "</div>"
        + bento_grid_html()
        + '<p class="footer-note">Estimates only · MVP · No bookings or tickets</p>'
    )


def hero_explore(city: str = "Delhi NCR") -> str:
    return f"""
    <div class="hero-explore">
      <div class="hero-bg" style="background-image:url('{NIGHTSCAPE_IMAGE}')"></div>
      <div class="hero-gradient"></div>
      <div class="ai-orbit ai-orbit-lg"></div>
      <div class="ai-orbit ai-orbit-xl"></div>
      <div class="hero-content">
        <h1>Explore {html.escape(city)}<br/><span class="accent">with AI</span></h1>
        <p>Your luxury digital concierge. Craft a personalized expedition using real OSM data
        and optional Groq tips.</p>
      </div>
    </div>
    """


def hero_plan() -> str:
    return f"""
    <div class="hero-plan" style="background-image:url('{HERO_IMAGE}')">
      <div class="hero-gradient"></div>
      <div class="hero-content-left">
        <h1>Generate Your Expedition</h1>
        <p>Tailor your Delhi experience with AI-driven precision and optimized walking routes.</p>
      </div>
    </div>
    """


def quick_plan_card() -> str:
    return """
    <div class="glass-panel quick-plan-card">
      <div class="shine-line"></div>
      <div class="quick-plan-grid">
        <div><span class="field-label">📍 Destination</span>
          <p class="field-value">India Gate, Delhi</p></div>
        <div><span class="field-label">🕐 Duration</span>
          <p class="field-value">4h · 8h · 1 day</p></div>
        <div><span class="field-label">✨ Interests</span>
          <div class="chip-row">
            <span class="chip chip-cyan">Food</span>
            <span class="chip chip-teal">History</span>
            <span class="chip chip-amber">Nature</span>
          </div></div>
        <div class="quick-plan-cta">
          <a class="btn-primary-cta" href="?page=plan">Customize →</a>
        </div>
      </div>
    </div>
    """


def bento_grid_html() -> str:
    return """
    <div class="bento-grid">
      <div class="glass-panel bento-card bento-wide">
        <span class="bento-tag">Exclusive Access</span>
        <h3>Curated Dining at Taj</h3>
        <p>AI identified lower wait times for window seats at Varq tonight.</p>
      </div>
      <div class="glass-panel bento-card bento-stats">
        <div class="stats-icon">📊</div>
        <h3>Live Insights</h3>
        <div class="stat-row"><span>Crowd: GK-II</span><span class="teal">Low</span></div>
        <div class="stat-bar"><div class="stat-fill teal" style="width:30%"></div></div>
        <div class="stat-row"><span>Traffic: Cyber Hub</span><span class="error">High</span></div>
        <div class="stat-bar"><div class="stat-fill error" style="width:85%"></div></div>
      </div>
      <div class="glass-panel bento-card bento-sm">
        <span class="bento-icon">🚕</span>
        <h4>Premium Transit</h4>
        <p>Zero-wait travel coordinated with your AI itinerary.</p>
      </div>
      <div class="glass-panel bento-card bento-sm">
        <span class="bento-icon">🏛️</span>
        <h4>Historical Walk</h4>
        <p>AI audio guide for Lodhi Gardens at your pace.</p>
      </div>
      <div class="glass-panel bento-card bento-sm">
        <span class="bento-icon">🎭</span>
        <h4>Late Night Arts</h4>
        <p>Immersive theater — AI recommends tickets.</p>
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
        ai = f'<span class="ai-badge">✨ {status}</span>'
    return f"""
    <div class="summary-bar">
      <span class="summary-pill">📍 {html.escape(meta.get("city", "Delhi NCR"))}</span>
      <span class="summary-stats">
        <span>🕐 {hours}h</span>
        <span>₹{low:,}–₹{high:,}</span>
        <span>{summary.get("total_stops", 0)} stops</span>
      </span>
      {ai}
    </div>
    """


def expedition_header_html(meta: dict, summary: dict) -> str:
    mode = "AI-enhanced" if meta.get("planner_mode") == "ai" else "Standard"
    budget = meta.get("budget_tier", "medium")
    hours = round(meta.get("duration_minutes", 0) / 60)
    return f"""
    <div class="expedition-header">
      <h1>Your expedition</h1>
      <div class="badge-row">
        <span class="badge badge-teal">{hours}h</span>
        <span class="badge badge-amber">{html.escape(budget)} budget</span>
        {"<span class='badge badge-cyan'>✨ AI enhanced</span>" if mode == "AI-enhanced" else ""}
      </div>
      <p class="expedition-sub">
        {mode} plan · {summary.get("total_travel_min", 0)} min walking ·
        {summary.get("total_stops", 0)} stops
      </p>
    </div>
    """


def stats_panel_html(meta: dict, summary: dict) -> str:
    cost = summary.get("total_cost_inr", {})
    routing = meta.get("routing_source") or "planner"
    return f"""
    <div class="glass-panel stats-panel">
      <h3>Expedition stats</h3>
      <div class="stats-grid">
        <div class="stat-box">
          <p class="stat-label">Travel</p>
          <p class="stat-value">{summary.get("total_travel_min", 0)}<span> min</span></p>
        </div>
        <div class="stat-box">
          <p class="stat-label">Est. cost</p>
          <p class="stat-value">₹{cost.get("low", 0):,}–{cost.get("high", 0):,}</p>
        </div>
        <div class="stat-box stat-wide">
          <p class="stat-tip-title">✨ Pilot intelligence</p>
          <p class="stat-tip">Routing via {html.escape(routing)}. Costs are rough estimates —
          not bookings or tickets.</p>
        </div>
      </div>
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
      <span class="stop-time">{html.escape(stop.get("arrive_at", ""))} – {html.escape(stop.get("depart_at", ""))}</span>
      <span class="stop-cat">{html.escape(stop.get("category", ""))}</span>
      <div class="stop-name">{stop.get("order", "")}. {html.escape(stop.get("name", ""))}</div>
      <div class="stop-meta">
        Visit {stop.get("visit_minutes", 0)}m · ₹{cost.get("low", 0):,}–₹{cost.get("high", 0):,}{travel_txt}
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
