"""Night Explorer design tokens + Streamlit CSS (matches Next.js stitch_trip_pilot_ai_planner)."""

from __future__ import annotations

import streamlit as st

# Night Explorer palette — frontend/tailwind.config.ts
COLORS = {
    "background": "#0e1416",
    "surface_container": "#1b2122",
    "surface_container_low": "#171d1e",
    "on_surface": "#dee3e6",
    "on_surface_variant": "#bcc9cd",
    "outline_variant": "#3d494c",
    "primary": "#4cd7f6",
    "primary_container": "#06b6d4",
    "secondary": "#4fdbc8",
    "tertiary": "#ffb95f",
}

HERO_IMAGE = (
    "https://images.unsplash.com/photo-1587474260584-136574528ed5"
    "?q=80&w=1600&auto=format&fit=crop"
)
NIGHTSCAPE_IMAGE = HERO_IMAGE

DESIGN_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', system-ui, sans-serif !important;
}

.stApp {
    background: #0e1416 !important;
}

#MainMenu, footer, header[data-testid="stHeader"] {
    visibility: hidden !important;
    height: 0 !important;
}

[data-testid="stSidebar"] { display: none !important; }

[data-testid="stAppViewContainer"] > section.main {
    background: transparent !important;
}

/* Offset all Streamlit content right of the fixed sidebar */
section.main > div.block-container {
    max-width: 100% !important;
    padding: 1rem 1.5rem 2rem !important;
}
@media (min-width: 768px) {
    section.main > div.block-container {
        padding-left: 17rem !important;
    }
}

[data-testid="stMarkdownContainer"],
[data-testid="stVerticalBlockBorderWrapper"] {
    overflow: visible !important;
}

[data-testid="stMarkdownContainer"] .hero-explore,
[data-testid="stMarkdownContainer"] .hero-plan,
[data-testid="stMarkdownContainer"] .bento-grid {
    width: 100%;
}

h1, h2, h3, h4, p, label, .stMarkdown { color: #dee3e6; }
.stCaption { color: #bcc9cd !important; }

/* ── Sidebar ── */
.tp-sidebar {
    display: none;
    position: fixed;
    left: 0; top: 0;
    width: 16rem;
    height: 100vh;
    z-index: 999;
    flex-direction: column;
    padding: 1.5rem;
    border-right: 1px solid rgba(255,255,255,0.1);
    background: rgba(14, 20, 22, 0.85);
    backdrop-filter: blur(16px);
    box-shadow: 0 0 20px rgba(173, 198, 255, 0.08);
}
@media (min-width: 768px) {
    .tp-sidebar { display: flex; }
}

.sidebar-brand h1 {
    font-size: 1.25rem;
    font-weight: 700;
    color: #4cd7f6 !important;
    margin: 0;
}
.sidebar-brand p {
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.2em;
    color: #bcc9cd !important;
    opacity: 0.7;
    margin: 0.25rem 0 0;
}

.sidebar-nav { flex: 1; margin-top: 2rem; display: flex; flex-direction: column; gap: 0.5rem; }

.nav-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem 1rem;
    border-radius: 0.5rem;
    color: #bcc9cd !important;
    text-decoration: none !important;
    font-size: 1rem;
    transition: all 0.3s ease;
    border: 1px solid transparent;
}
.nav-item:hover {
    color: #dee3e6 !important;
    background: rgba(255,255,255,0.05);
    box-shadow: 0 0 15px rgba(173,198,255,0.12);
}
.nav-item-active {
    background: rgba(6, 182, 212, 0.2) !important;
    color: #4cd7f6 !important;
    border-color: rgba(76, 215, 246, 0.3) !important;
    box-shadow: 0 0 10px rgba(173,198,255,0.2);
}

.sidebar-badge {
    font-size: 0.7rem;
    color: #bcc9cd !important;
    display: flex;
    align-items: center;
    gap: 0.35rem;
    margin: 1rem 0;
}
.sidebar-badge .dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #4ade80;
}

.btn-sidebar-cta {
    display: block;
    text-align: center;
    padding: 0.75rem;
    border-radius: 0.5rem;
    background: #4cd7f6;
    color: #003640 !important;
    font-weight: 700;
    text-decoration: none !important;
    box-shadow: 0 0 20px rgba(76, 215, 246, 0.35);
    transition: filter 0.2s, transform 0.15s;
    margin-top: auto;
}
.btn-sidebar-cta:hover { filter: brightness(1.1); transform: translateY(-1px); }

/* ── Top bar ── */
.tp-topbar {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 0.75rem;
    min-height: 4rem;
    padding: 0.75rem 0;
    background: linear-gradient(to bottom, #0e1416, transparent);
    position: sticky;
    top: 0;
    z-index: 40;
}
.tp-mobile-nav {
    display: flex;
    gap: 0.5rem;
    width: 100%;
}
@media (min-width: 768px) {
    .tp-mobile-nav { display: none; }
}
.tp-mobile-nav a {
    flex: 1;
    text-align: center;
    padding: 0.5rem 0.75rem;
    border-radius: 0.5rem;
    font-size: 0.8rem;
    font-weight: 600;
    text-decoration: none !important;
    border: 1px solid #3d494c;
    color: #bcc9cd !important;
    background: #171d1e;
}
.tp-mobile-nav a.active {
    background: rgba(76, 215, 246, 0.15);
    border-color: #4cd7f6;
    color: #4cd7f6 !important;
}
.tp-status-label {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #bcc9cd;
    margin-right: 0.5rem;
}
.tp-status-active {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #4cd7f6;
    border-bottom: 2px solid #4cd7f6;
    padding-bottom: 2px;
}
.tp-search {
    font-size: 0.8rem;
    color: #bcc9cd;
    padding: 0.35rem 1rem;
    border-radius: 9999px;
    border: 1px solid rgba(61,73,76,0.5);
    background: rgba(23,29,30,0.6);
}

/* ── Hero explore ── */
.hero-explore {
    position: relative;
    min-height: 420px;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    overflow: hidden;
}
.hero-bg {
    position: absolute;
    inset: 0;
    background-size: cover;
    background-position: center;
    opacity: 0.4;
    mix-blend-mode: screen;
}
.hero-gradient {
    position: absolute;
    inset: 0;
    background: linear-gradient(to bottom, transparent, rgba(14,20,22,0.2), #0e1416);
}
.hero-content { position: relative; z-index: 10; padding: 2rem; max-width: 48rem; }
.hero-content h1 {
    font-size: clamp(2rem, 5vw, 3rem);
    font-weight: 800;
    color: #fff !important;
    line-height: 1.15;
    margin: 0;
}
.hero-content h1 .accent { color: #4cd7f6; font-style: italic; }
.hero-content p { color: #bcc9cd !important; margin-top: 1rem; font-size: 1.1rem; }

.hero-plan {
    position: relative;
    min-height: 200px;
    display: flex;
    align-items: flex-end;
    padding: 2rem;
    background-size: cover;
    background-position: center;
    margin-bottom: -2rem;
}
.hero-content-left { position: relative; z-index: 10; }
.hero-content-left h1 { font-size: 1.75rem; font-weight: 700; color: #dee3e6 !important; margin: 0; }
.hero-content-left p { color: #bcc9cd !important; margin-top: 0.5rem; }

.ai-orbit {
    position: absolute;
    border-radius: 50%;
    border: 1px solid rgba(76, 215, 246, 0.3);
    left: 50%; top: 50%;
    transform: translate(-50%, -50%);
    pointer-events: none;
    animation: orbit-spin 20s linear infinite;
}
.ai-orbit-lg { width: 500px; height: 500px; opacity: 0.2; }
.ai-orbit-xl { width: 700px; height: 700px; opacity: 0.1; animation-direction: reverse; animation-duration: 35s; }

@keyframes orbit-spin {
    from { transform: translate(-50%, -50%) rotate(0deg); }
    to { transform: translate(-50%, -50%) rotate(360deg); }
}

/* ── Glass panels ── */
.glass-panel {
    background: rgba(14, 20, 22, 0.72);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(148, 163, 184, 0.12);
    border-radius: 1rem;
    transition: border-color 0.2s, box-shadow 0.2s, transform 0.2s;
}
@media (hover: hover) {
    .glass-panel:hover { border-color: rgba(76, 215, 246, 0.25); }
    .bento-card:hover { transform: translateY(-2px); box-shadow: 0 8px 28px rgba(0,0,0,0.35); }
    .stop-card:hover { transform: translateY(-2px); box-shadow: 0 6px 24px rgba(0,0,0,0.3); border-color: #4cd7f6; }
}

.shine-line {
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(to right, transparent, rgba(76,215,246,0.4), transparent);
}

.quick-plan-card {
    position: relative;
    max-width: 64rem;
    margin: -4rem auto 0;
    padding: 2rem 2.5rem;
    box-shadow: 0 25px 50px rgba(0,0,0,0.45);
}
.quick-plan-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 1.5rem;
    align-items: end;
}
.field-label {
    display: block;
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #4cd7f6;
    margin-bottom: 0.5rem;
}
.field-value {
    background: rgba(9,15,17,0.5);
    padding: 0.75rem;
    border-radius: 0.5rem;
    color: #dee3e6 !important;
    margin: 0;
    font-size: 0.9rem;
}
.chip-row { display: flex; flex-wrap: wrap; gap: 0.5rem; }
.chip {
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    border: 1px solid;
}
.chip-cyan { border-color: rgba(76,215,246,0.2); background: rgba(76,215,246,0.1); color: #4cd7f6; }
.chip-teal { border-color: rgba(79,219,200,0.2); background: rgba(79,219,200,0.1); color: #4fdbc8; }
.chip-amber { border-color: rgba(255,185,95,0.2); background: rgba(255,185,95,0.1); color: #ffb95f; }

.btn-primary-cta {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 1rem 1.5rem;
    border-radius: 0.75rem;
    background: #4cd7f6;
    color: #003640 !important;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-size: 0.8rem;
    text-decoration: none !important;
    box-shadow: 0 0 20px rgba(76, 215, 246, 0.4);
    transition: box-shadow 0.2s, transform 0.15s, filter 0.2s;
    width: 100%;
}
@media (hover: hover) {
    .btn-primary-cta:hover {
        box-shadow: 0 0 35px rgba(76, 215, 246, 0.6);
        filter: brightness(1.08);
        transform: translateY(-2px);
    }
}

/* ── Bento grid ── */
.bento-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1.25rem;
    max-width: 72rem;
    margin: 3rem auto 0;
    padding: 0 1.5rem 3rem;
}
@media (min-width: 768px) {
    .bento-grid { grid-template-columns: repeat(12, 1fr); }
    .bento-wide { grid-column: span 8; min-height: 280px; }
    .bento-stats { grid-column: span 4; min-height: 280px; }
    .bento-sm { grid-column: span 4; min-height: 200px; }
}
.bento-card { padding: 1.5rem; display: flex; flex-direction: column; justify-content: flex-end; }
.bento-tag { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: #4fdbc8; }
.bento-card h3, .bento-card h4 { color: #fff !important; margin: 0.5rem 0 0.25rem; }
.bento-card p { color: #bcc9cd !important; font-size: 0.85rem; margin: 0; }
.bento-icon { font-size: 1.75rem; margin-bottom: 0.75rem; }
.bento-stats { justify-content: space-between; border-color: rgba(76,215,246,0.2) !important; }
.stats-icon { font-size: 1.5rem; }
.stat-row { display: flex; justify-content: space-between; font-size: 0.85rem; color: #bcc9cd; margin-top: 0.75rem; }
.stat-row .teal { color: #4fdbc8; }
.stat-row .error { color: #ffb4ab; }
.stat-bar { height: 4px; background: rgba(255,255,255,0.05); border-radius: 99px; margin-top: 0.35rem; overflow: hidden; }
.stat-fill { height: 100%; border-radius: 99px; }
.stat-fill.teal { background: #4fdbc8; box-shadow: 0 0 8px #4fdbc8; }
.stat-fill.error { background: #ffb4ab; box-shadow: 0 0 8px #ffb4ab; }

/* ── Form panel ── */
.form-panel {
    max-width: 48rem;
    margin: 0 auto;
    padding: 2rem 2.5rem;
    position: relative;
}
.form-panel .shine-line { position: absolute; top: 0; left: 0; right: 0; }

/* ── Itinerary ── */
.summary-bar {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
    padding: 0.75rem 1.5rem;
    border-bottom: 1px solid rgba(61,73,76,0.5);
    background: rgba(23,29,30,0.92);
    backdrop-filter: blur(8px);
    margin-bottom: 1.5rem;
}
.summary-pill {
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    border: 1px solid rgba(79,219,200,0.2);
    background: rgba(79,219,200,0.1);
    font-size: 0.7rem;
    color: #4fdbc8 !important;
    text-transform: uppercase;
}
.summary-stats { display: flex; gap: 1rem; font-size: 0.8rem; color: #bcc9cd !important; }
.ai-badge { color: #4cd7f6 !important; font-size: 0.8rem; }

.expedition-header { padding: 0 1.5rem 1rem; }
.expedition-header h1 { font-size: 2rem; font-weight: 700; color: #dee3e6 !important; margin: 0; }
.badge-row { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.75rem; }
.badge {
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
    border: 1px solid;
}
.badge-teal { border-color: rgba(79,219,200,0.2); background: rgba(79,219,200,0.1); color: #4fdbc8; }
.badge-amber { border-color: rgba(255,185,95,0.2); background: rgba(255,185,95,0.1); color: #ffb95f; }
.badge-cyan { border-color: rgba(76,215,246,0.2); background: rgba(76,215,246,0.1); color: #4cd7f6; }
.expedition-sub { color: #bcc9cd !important; font-size: 0.9rem; margin-top: 0.5rem; }

.stop-card {
    border: 1px solid #3d494c;
    border-radius: 1rem;
    background: rgba(27,33,34,0.8);
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
    transition: all 0.25s ease;
}
.stop-time { font-size: 0.8rem; color: #4fdbc8 !important; font-weight: 500; letter-spacing: 0.05em; }
.stop-cat {
    display: inline-block;
    margin-left: 0.5rem;
    padding: 0.1rem 0.5rem;
    border-radius: 4px;
    background: #303638;
    font-size: 0.65rem;
    font-weight: 700;
    text-transform: uppercase;
    color: #bcc9cd !important;
}
.stop-name { font-size: 1.2rem; font-weight: 700; color: #dee3e6 !important; margin: 0.35rem 0; }
.stop-meta { color: #bcc9cd !important; font-size: 0.9rem; }
.stop-notes {
    margin-top: 0.75rem;
    padding: 0.75rem 1rem;
    border-left: 2px solid #4cd7f6;
    background: rgba(76, 215, 246, 0.08);
    border-radius: 0 0.5rem 0.5rem 0;
    font-style: italic;
    color: #4cd7f6 !important;
    font-size: 0.9rem;
}

.stats-panel { padding: 1.5rem; margin: 0 1.5rem 1.5rem; }
.stats-panel h3 { font-size: 1.1rem; font-weight: 600; color: #dee3e6 !important; margin: 0 0 1rem; }
.stats-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.stat-box {
    padding: 1rem;
    border-radius: 0.75rem;
    border: 1px solid rgba(255,255,255,0.05);
    background: rgba(23,29,30,0.5);
}
.stat-wide { grid-column: span 2; border-color: rgba(76,215,246,0.2); background: rgba(76,215,246,0.05); }
.stat-label { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: #bcc9cd; margin: 0 0 0.25rem; }
.stat-value { font-size: 1.5rem; font-weight: 700; color: #dee3e6 !important; margin: 0; }
.stat-value span { font-size: 0.85rem; font-weight: 400; color: #bcc9cd; }
.stat-tip-title { font-size: 0.85rem; font-weight: 700; color: #4cd7f6 !important; margin: 0 0 0.25rem; }
.stat-tip { font-size: 0.75rem; color: #bcc9cd !important; margin: 0; line-height: 1.5; }

.map-frame {
    margin: 0 1.5rem 1.5rem;
    padding: 0.5rem;
    border-radius: 1rem;
    border: 1px solid #3d494c;
    background: #1b2122;
    overflow: hidden;
}
.map-label {
    padding: 0.5rem 1rem;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #4cd7f6;
}

.empty-state { text-align: center; padding: 3rem; margin: 2rem 1.5rem; }
.empty-icon { font-size: 2.5rem; margin: 0; }
.empty-state h2 { color: #dee3e6 !important; margin: 1rem 0 0.5rem; }
.empty-state p { color: #bcc9cd !important; }

.itinerary-body { padding: 0 1.5rem 2rem; }

/* ── Streamlit widgets ── */
[data-testid="stPills"] button {
    border: 1px solid #3d494c !important;
    background: #171d1e !important;
    color: #bcc9cd !important;
    border-radius: 9999px !important;
    transition: all 0.2s ease !important;
}
@media (hover: hover) {
    [data-testid="stPills"] button:hover:not([aria-pressed="true"]) {
        background: #252b2d !important;
        border-color: #4cd7f6 !important;
        color: #dee3e6 !important;
    }
}
[data-testid="stPills"] button[aria-pressed="true"] {
    background: rgba(76, 215, 246, 0.15) !important;
    border-color: #4cd7f6 !important;
    color: #4cd7f6 !important;
}

.stButton > button {
    transition: all 0.2s ease !important;
    border-radius: 0.75rem !important;
}
.stButton > button[kind="primary"] {
    background: #4cd7f6 !important;
    color: #003640 !important;
    font-weight: 700 !important;
    border: none !important;
    box-shadow: 0 0 20px rgba(76, 215, 246, 0.35) !important;
}
@media (hover: hover) {
    .stButton > button[kind="primary"]:hover:not(:disabled) {
        box-shadow: 0 0 32px rgba(76, 215, 246, 0.55) !important;
        filter: brightness(1.08);
        transform: translateY(-1px);
    }
}
.stButton > button[kind="secondary"] {
    background: transparent !important;
    color: #dee3e6 !important;
    border: 1px solid #3d494c !important;
}
@media (hover: hover) {
    .stButton > button[kind="secondary"]:hover {
        border-color: #4cd7f6 !important;
        color: #4cd7f6 !important;
        background: rgba(255,255,255,0.05) !important;
    }
}

.section-label {
    display: block;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #4cd7f6;
    margin-bottom: 0.75rem;
}

.footer-note {
    text-align: center;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: rgba(188,201,205,0.5);
    padding: 2rem;
}
"""


def inject_theme() -> None:
    st.markdown(f"<style>{DESIGN_CSS}</style>", unsafe_allow_html=True)
