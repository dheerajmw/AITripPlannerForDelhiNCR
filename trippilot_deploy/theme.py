"""Purple Aurora design tokens + Streamlit CSS (matches Next.js frontend)."""

from __future__ import annotations

import streamlit as st

COLORS = {
    "background": "#0f131d",
    "surface": "#0f131d",
    "surface_container": "#1b2029",
    "surface_container_low": "#171c25",
    "on_surface": "#dfe2f0",
    "on_surface_variant": "#cbc3d7",
    "outline_variant": "#494454",
    "primary": "#d0bcff",
    "primary_container": "#a078ff",
    "on_primary": "#3c0091",
    "secondary": "#ddb7ff",
    "tertiary": "#ffb0cd",
}

HERO_IMAGE = (
    "https://images.unsplash.com/photo-1587474260584-136574528ed5"
    "?q=80&w=1600&auto=format&fit=crop"
)

DESIGN_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', system-ui, sans-serif !important;
}

.stApp {
    background: #070b14 !important;
}

#MainMenu, footer, header[data-testid="stHeader"] {
    visibility: hidden !important;
    height: 0 !important;
}

[data-testid="stSidebar"] { display: none !important; }

[data-testid="stAppViewContainer"] > section.main {
    background: transparent !important;
}

section.main > div.block-container {
    max-width: 80rem !important;
    padding: 6.5rem 1.25rem 5rem !important;
    margin-left: auto !important;
    margin-right: auto !important;
}

/* Global page alignment */
.tp-page-shell {
    max-width: 72rem;
    margin: 0 auto;
    position: relative;
    z-index: 1;
}
.tp-page-narrow {
    max-width: 56rem;
    margin: 0 auto;
    position: relative;
    z-index: 1;
}
section.main [data-testid="column"] {
    align-self: flex-start !important;
}
section.main [data-testid="column"] > div {
    width: 100%;
}
section.main [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"] {
    align-items: flex-start !important;
    gap: 1.5rem !important;
}
section.main .stButton {
    margin-top: 0.25rem;
}
section.main [data-testid="stCaptionContainer"] {
    text-align: center;
    margin-top: 0.25rem;
}

[data-testid="stMarkdownContainer"],
[data-testid="stVerticalBlockBorderWrapper"] {
    overflow: visible !important;
}

h1, h2, h3, h4, p, label, .stMarkdown { color: #dfe2f0; }
.stCaption { color: #cbc3d7 !important; }

/* Aurora backdrop */
.tp-aurora {
    pointer-events: none;
    position: fixed;
    inset: 0;
    z-index: 0;
    overflow: hidden;
}
.tp-aurora-blob-1 {
    position: absolute;
    left: -10%;
    top: -10%;
    width: 40%;
    height: 40%;
    border-radius: 50%;
    background: rgba(208, 188, 255, 0.2);
    filter: blur(120px);
    animation: pulse-glow 4s ease-in-out infinite;
}
.tp-aurora-blob-2 {
    position: absolute;
    right: -10%;
    bottom: -10%;
    width: 50%;
    height: 50%;
    border-radius: 50%;
    background: rgba(221, 183, 255, 0.1);
    filter: blur(150px);
    animation: pulse-glow 4s ease-in-out infinite 2s;
}
.tp-aurora-map {
    position: absolute;
    inset: 0;
    opacity: 0.2;
    background-size: cover;
    background-position: center;
    mask-image: linear-gradient(to bottom, black 0%, rgba(0,0,0,0.6) 50%, transparent 100%);
    -webkit-mask-image: linear-gradient(to bottom, black 0%, rgba(0,0,0,0.6) 50%, transparent 100%);
}
@keyframes pulse-glow {
    0%, 100% { transform: scale(1); opacity: 0.8; }
    50% { transform: scale(1.1); opacity: 1; }
}

/* Top nav pill */
.tp-topnav-wrap {
    position: fixed;
    left: 0; right: 0; top: 0;
    z-index: 100;
    padding: 0.5rem 1.25rem;
}
.tp-topnav-inner {
    max-width: 80rem;
    margin: 0 auto;
}
.tp-topnav {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    padding: 0.75rem 1.5rem;
    border-radius: 9999px;
    border: 1px solid rgba(203, 195, 215, 0.1);
    background: rgba(15, 19, 29, 0.4);
    backdrop-filter: blur(16px);
    box-shadow: 0 0 20px rgba(208, 188, 255, 0.1);
}
.tp-brand {
    font-size: 1.25rem;
    font-weight: 700;
    color: #d0bcff !important;
    text-decoration: none !important;
}
.tp-nav-links { display: none; gap: 2rem; }
@media (min-width: 768px) { .tp-nav-links { display: flex; } }
.tp-nav-link {
    color: #cbc3d7 !important;
    text-decoration: none !important;
    font-size: 0.95rem;
    transition: color 0.2s;
}
.tp-nav-link:hover { color: #d0bcff !important; }
.tp-nav-link-active { color: #d0bcff !important; font-weight: 600; }
.tp-nav-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.35rem 0.75rem;
    border-radius: 9999px;
    border: 1px solid rgba(255,255,255,0.1);
    background: rgba(49, 53, 63, 0.8);
    font-size: 0.7rem;
    color: #cbc3d7 !important;
}
.tp-nav-badge .dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #ffb0cd;
}
.tp-nav-actions {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    flex-shrink: 0;
}
.tp-avatar {
    width: 2.5rem; height: 2.5rem;
    border-radius: 50%;
    border: 2px solid rgba(208, 188, 255, 0.3);
    background: #262a34;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.75rem;
    font-weight: 700;
    color: #d0bcff;
}
.tp-mobile-nav {
    display: flex;
    gap: 0.5rem;
    width: 100%;
    margin-top: 0.5rem;
}
@media (min-width: 768px) { .tp-mobile-nav { display: none; } }
.tp-mobile-nav a {
    flex: 1;
    text-align: center;
    padding: 0.5rem;
    border-radius: 0.75rem;
    font-size: 0.75rem;
    font-weight: 600;
    text-decoration: none !important;
    border: 1px solid rgba(73, 68, 84, 0.4);
    color: #cbc3d7 !important;
    background: rgba(27, 32, 41, 0.6);
}
.tp-mobile-nav a.active {
    background: rgba(208, 188, 255, 0.2);
    border-color: rgba(208, 188, 255, 0.3);
    color: #d0bcff !important;
}

/* Hero */
.hero-center {
    text-align: center;
    padding: 2rem 1rem 2.5rem;
    position: relative;
    z-index: 1;
}
.hero-orb {
    position: relative;
    width: 6rem;
    height: 6rem;
    margin: 0 auto 1.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    background: linear-gradient(135deg, #d0bcff, #ddb7ff);
    box-shadow: 0 0 80px 20px rgba(160, 120, 255, 0.4);
    font-size: 2.5rem;
}
.hero-orb-glow {
    position: absolute;
    inset: 0;
    border-radius: 50%;
    background: rgba(208, 188, 255, 0.3);
    filter: blur(48px);
    transform: scale(1.5);
    z-index: -1;
}
.hero-center h1 {
    font-size: clamp(2rem, 5vw, 3rem);
    font-weight: 800;
    color: #dfe2f0 !important;
    line-height: 1.15;
    margin: 0;
}
.aurora-text {
    background: linear-gradient(to right, #d0bcff, #ddb7ff, #a078ff);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-center p {
    color: #cbc3d7 !important;
    margin-top: 1rem;
    font-size: 1.1rem;
    max-width: 42rem;
    margin-left: auto;
    margin-right: auto;
}

.hero-plan-compact {
    position: relative;
    text-align: center;
    padding: 1rem 1rem 1.5rem;
    z-index: 1;
    max-width: 48rem;
    margin: 0 auto;
}
.hero-orb-sm {
    width: 5rem !important;
    height: 5rem !important;
    min-width: 5rem;
    min-height: 5rem;
    max-width: 5rem;
    max-height: 5rem;
    margin: 0 auto 1rem !important;
    font-size: 2rem !important;
    flex-shrink: 0;
}
.hero-plan-compact h1 {
    font-size: clamp(1.75rem, 4vw, 2.5rem);
    font-weight: 800;
    margin: 0;
    color: #dfe2f0 !important;
}
.hero-plan-compact p {
    color: #cbc3d7 !important;
    margin-top: 0.75rem;
    font-size: 1rem;
    line-height: 1.5;
    text-shadow: 0 1px 12px rgba(7, 11, 20, 0.85);
}

/* Glass */
.glass-panel {
    background: rgba(15, 19, 29, 0.55);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(203, 195, 215, 0.1);
    border-top-color: rgba(255, 255, 255, 0.15);
    border-radius: 2rem;
    position: relative;
    z-index: 1;
}
.glass-card {
    background: rgba(15, 19, 29, 0.4);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(203, 195, 215, 0.1);
    border-radius: 1rem;
    transition: transform 0.3s, box-shadow 0.3s, border-color 0.2s;
}
@media (hover: hover) {
    .glass-card:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(208, 188, 255, 0.12);
        border-color: rgba(208, 188, 255, 0.2);
    }
    .stop-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 24px rgba(160, 120, 255, 0.15);
        border-color: rgba(208, 188, 255, 0.3);
    }
}

.preview-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.5rem 0.85rem;
    border-radius: 0.75rem;
    font-size: 0.85rem;
    font-weight: 600;
    border: 1px solid rgba(73, 68, 84, 0.3);
}
.preview-chip-muted {
    background: rgba(49, 53, 63, 0.6);
    color: #cbc3d7 !important;
}
.preview-chip-active {
    background: rgba(208, 188, 255, 0.2);
    border-color: rgba(208, 188, 255, 0.3);
    color: #d0bcff !important;
}

.quick-plan-card {
    max-width: 56rem;
    margin: 0 auto;
    padding: 2rem 2.5rem;
    box-shadow: 0 25px 50px rgba(160, 120, 255, 0.08);
}
.quick-plan-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 1.5rem;
}
.field-label {
    display: block;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #d0bcff;
    margin-bottom: 0.5rem;
}
.chip-row { display: flex; flex-wrap: wrap; gap: 0.5rem; }
.preview-note {
    text-align: center;
    font-size: 0.75rem;
    color: #cbc3d7;
    margin-bottom: 1rem;
}

.btn-primary-cta {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 1.25rem 1.5rem;
    border-radius: 1rem;
    background: linear-gradient(to right, #8b5cf6, #a855f7);
    color: #fff !important;
    font-weight: 700;
    text-decoration: none !important;
    box-shadow: 0 0 30px rgba(160, 120, 255, 0.4);
    width: 100%;
    transition: transform 0.2s, box-shadow 0.2s;
}
@media (hover: hover) {
    .btn-primary-cta:hover {
        box-shadow: 0 0 40px rgba(160, 120, 255, 0.55);
        transform: translateY(-1px);
    }
}

.bento-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1.25rem;
    max-width: 72rem;
    margin: 2.5rem auto 0;
    padding: 0 0 2rem;
    position: relative;
    z-index: 1;
}
@media (min-width: 768px) {
    .bento-grid { grid-template-columns: repeat(12, 1fr); }
    .bento-wide { grid-column: span 8; min-height: 240px; }
    .bento-stats { grid-column: span 4; min-height: 240px; }
    .bento-sm { grid-column: span 4; min-height: 200px; }
}
.bento-card { padding: 1.5rem; display: flex; flex-direction: column; justify-content: flex-end; }
.bento-tag {
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #ddb7ff;
}
.bento-card h3, .bento-card h4 { color: #dfe2f0 !important; margin: 0.5rem 0 0.25rem; }
.bento-card p { color: #cbc3d7 !important; font-size: 0.85rem; margin: 0; }
.bento-icon { font-size: 1.75rem; margin-bottom: 0.75rem; }
.bento-stats { justify-content: space-between; }
.stat-row { display: flex; justify-content: space-between; font-size: 0.85rem; color: #cbc3d7; margin-top: 0.75rem; }
.stat-row .secondary { color: #ddb7ff; }
.stat-row .error { color: #ffb4ab; }
.stat-bar { height: 4px; background: rgba(255,255,255,0.05); border-radius: 99px; margin-top: 0.35rem; overflow: hidden; }
.stat-fill { height: 100%; border-radius: 99px; }
.stat-fill.secondary { background: #ddb7ff; box-shadow: 0 0 8px #ddb7ff; }
.stat-fill.error { background: #ffb4ab; box-shadow: 0 0 8px #ffb4ab; }

.form-section-gap {
    margin-bottom: 1.25rem;
}

.itinerary-shell {
    max-width: 72rem;
    margin: 0 auto;
    position: relative;
    z-index: 1;
}
.summary-bar {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
    padding: 0.85rem 1.25rem;
    border: 1px solid rgba(73, 68, 84, 0.35);
    background: rgba(27, 32, 41, 0.92);
    backdrop-filter: blur(8px);
    margin-bottom: 1rem;
    border-radius: 1rem;
    position: relative;
    z-index: 1;
}
.summary-pill {
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    border: 1px solid rgba(221, 183, 255, 0.3);
    background: rgba(221, 183, 255, 0.1);
    font-size: 0.7rem;
    color: #ddb7ff !important;
}
.summary-stats { display: flex; gap: 1rem; font-size: 0.8rem; color: #cbc3d7 !important; }
.ai-badge { color: #d0bcff !important; font-size: 0.8rem; }

.expedition-header {
    padding: 0 0 1.25rem;
    margin-bottom: 0.5rem;
    text-align: center;
    position: relative;
    z-index: 1;
}
.expedition-header h1 {
    font-size: 2rem;
    font-weight: 800;
    margin: 0;
    background: linear-gradient(to right, #d0bcff, #ddb7ff, #a078ff);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}
.badge-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 0.75rem;
    justify-content: center;
}
.badge {
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
    border: 1px solid;
}
.badge-primary { border-color: rgba(208,188,255,0.3); background: rgba(208,188,255,0.15); color: #d0bcff; }
.badge-secondary { border-color: rgba(221,183,255,0.3); background: rgba(221,183,255,0.1); color: #ddb7ff; }
.expedition-sub { color: #cbc3d7 !important; font-size: 0.9rem; margin-top: 0.5rem; }

.stop-card {
    border: 1px solid rgba(73, 68, 84, 0.4);
    border-radius: 1rem;
    background: rgba(15, 19, 29, 0.4);
    backdrop-filter: blur(16px);
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
    transition: all 0.25s ease;
}
.stop-time { font-size: 0.8rem; color: #d0bcff !important; font-weight: 600; letter-spacing: 0.05em; }
.stop-cat {
    display: inline-block;
    margin-left: 0.5rem;
    padding: 0.1rem 0.5rem;
    border-radius: 9999px;
    background: rgba(38, 42, 52, 0.8);
    font-size: 0.65rem;
    font-weight: 700;
    text-transform: uppercase;
    color: #cbc3d7 !important;
}
.stop-name { font-size: 1.2rem; font-weight: 700; color: #dfe2f0 !important; margin: 0.35rem 0; }
.stop-meta { color: #cbc3d7 !important; font-size: 0.9rem; }
.stop-notes {
    margin-top: 0.75rem;
    padding: 0.75rem 1rem;
    border-left: 2px solid #a078ff;
    background: rgba(208, 188, 255, 0.1);
    border-radius: 0 0.5rem 0.5rem 0;
    font-style: italic;
    color: #d0bcff !important;
    font-size: 0.9rem;
}

.stats-panel { padding: 1.5rem; margin-bottom: 1rem; }
.stats-panel h3 { font-size: 1.1rem; font-weight: 600; color: #dfe2f0 !important; margin: 0 0 1rem; }
.stats-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.stat-box {
    padding: 1rem;
    border-radius: 0.75rem;
    border: 1px solid rgba(255,255,255,0.05);
    background: rgba(27, 32, 41, 0.5);
    text-align: center;
}
.stat-wide { grid-column: span 2; border-color: rgba(208,188,255,0.2); background: rgba(208,188,255,0.05); }
.stat-label { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: #cbc3d7; margin: 0 0 0.25rem; }
.stat-value { font-size: 1.25rem; font-weight: 700; color: #dfe2f0 !important; margin: 0; }
.stat-tip-title { font-size: 0.85rem; font-weight: 700; color: #d0bcff !important; margin: 0 0 0.25rem; }
.stat-tip { font-size: 0.75rem; color: #cbc3d7 !important; margin: 0; line-height: 1.5; }

.map-shell {
    margin-bottom: 1rem;
    border-radius: 1rem;
    border: 1px solid rgba(73, 68, 84, 0.4);
    background: #1b2029;
    overflow: hidden;
}
.map-label {
    padding: 0.65rem 1rem;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #d0bcff;
    margin: 0;
}
.map-shell [data-testid="stDeckGlJsonChart"] {
    margin: 0 !important;
}
.form-field-block {
    margin-bottom: 1rem;
}
.region-chip-row {
    margin-bottom: 0.75rem;
}
.itinerary-actions {
    max-width: 72rem;
    margin: 1.5rem auto 0;
}
.gmaps-link {
    display: block;
    margin: 0.75rem 1rem 1rem;
    padding: 0.75rem 1rem;
    text-align: center;
    border-radius: 0.75rem;
    border: 1px solid rgba(208, 188, 255, 0.3);
    background: rgba(208, 188, 255, 0.1);
    color: #d0bcff !important;
    font-weight: 600;
    font-size: 0.85rem;
    text-decoration: none !important;
}

.empty-state { text-align: center; padding: 3rem; margin: 2rem 0; }
.empty-icon { font-size: 2.5rem; margin: 0; }
.empty-state h2 { color: #dfe2f0 !important; margin: 1rem 0 0.5rem; }
.empty-state p { color: #cbc3d7 !important; }

.section-label {
    display: block;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #d0bcff;
    margin-bottom: 0.75rem;
}
.footer-note {
    text-align: center;
    font-size: 0.75rem;
    color: rgba(203, 195, 215, 0.6);
    padding: 2rem 0;
    position: relative;
    z-index: 1;
}

/* Streamlit widgets */
[data-testid="stPills"] button {
    border: 1px solid rgba(73, 68, 84, 0.4) !important;
    background: rgba(49, 53, 63, 0.6) !important;
    color: #cbc3d7 !important;
    border-radius: 0.75rem !important;
}
[data-testid="stPills"] button[aria-pressed="true"] {
    background: rgba(208, 188, 255, 0.2) !important;
    border-color: rgba(208, 188, 255, 0.3) !important;
    color: #d0bcff !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(to right, #8b5cf6, #a855f7) !important;
    color: #fff !important;
    font-weight: 700 !important;
    border: none !important;
    box-shadow: 0 0 30px rgba(160, 120, 255, 0.35) !important;
    border-radius: 1rem !important;
}
.stButton > button[kind="secondary"] {
    background: transparent !important;
    color: #dfe2f0 !important;
    border: 1px solid rgba(73, 68, 84, 0.4) !important;
    border-radius: 1rem !important;
}
[data-testid="stSelectbox"] label { color: #d0bcff !important; font-weight: 600 !important; }
"""


def inject_theme() -> None:
    st.markdown(f"<style>{DESIGN_CSS}</style>", unsafe_allow_html=True)


ITINERARY_LAYOUT_CSS = """
section.main .itinerary-shell ~ [data-testid="stHorizontalBlock"] {
    max-width: 72rem;
    margin-left: auto !important;
    margin-right: auto !important;
    width: 100%;
    align-items: flex-start !important;
}
section.main .itinerary-shell ~ [data-testid="stHorizontalBlock"] [data-testid="column"] {
    align-self: stretch !important;
}
section.main .itinerary-actions-marker ~ [data-testid="stHorizontalBlock"] {
    max-width: 72rem;
    margin: 1.5rem auto 0;
    width: 100%;
}
"""

PLAN_FORM_CSS = """
section.main [data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(15, 19, 29, 0.72) !important;
    backdrop-filter: blur(16px);
    border: 1px solid rgba(203, 195, 215, 0.12) !important;
    border-radius: 2rem !important;
    padding: 1.75rem 2rem 2rem !important;
    max-width: 56rem;
    margin: 0 auto 2rem !important;
    box-shadow: 0 25px 50px rgba(160, 120, 255, 0.08);
}
section.main [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stWidgetLabel"] p {
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    color: #d0bcff !important;
}
section.main [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stSelectbox"] > div > div {
    background: rgba(49, 53, 63, 0.6) !important;
    border-color: rgba(73, 68, 84, 0.5) !important;
    border-radius: 0.75rem !important;
}
section.main [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stPills"] button {
    min-height: 2.5rem;
    border-radius: 0.75rem !important;
}
section.main [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stPills"] button[aria-pressed="true"] {
    background: rgba(160, 120, 255, 0.25) !important;
    border-color: rgba(208, 188, 255, 0.45) !important;
    color: #d0bcff !important;
    box-shadow: 0 0 12px rgba(160, 120, 255, 0.2);
}
section.main [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stToggle"] {
    padding-top: 0.75rem;
    border-top: 1px solid rgba(73, 68, 84, 0.35);
    margin-top: 0.5rem;
}
section.main [data-testid="stVerticalBlockBorderWrapper"] [data-testid="column"] {
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
}
section.main [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stSelectbox"],
section.main [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stPills"] {
    margin-bottom: 1rem;
}
section.main [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stCaptionContainer"] {
    text-align: left;
}
"""


def inject_plan_form_styles() -> None:
    st.markdown(f"<style>{PLAN_FORM_CSS}</style>", unsafe_allow_html=True)


def inject_itinerary_layout_styles() -> None:
    st.markdown(f"<style>{ITINERARY_LAYOUT_CSS}</style>", unsafe_allow_html=True)
