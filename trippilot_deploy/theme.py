"""TripPilot AI design tokens + Streamlit CSS overrides (matches Next.js / Stitch)."""

from __future__ import annotations

import streamlit as st

# From frontend/tailwind.config.ts + globals.css
COLORS = {
    "background": "#151024",
    "surface_container": "#211d31",
    "surface_container_low": "#1d182d",
    "surface_container_highest": "#373247",
    "on_surface": "#e7defb",
    "on_surface_variant": "#d1c2d2",
    "outline_variant": "#4e4350",
    "primary": "#edb1ff",
    "primary_container": "#9d50bb",
    "on_primary_container": "#fff3fd",
    "secondary": "#5dd9d0",
    "tertiary": "#d6baff",
}

HERO_IMAGE = (
    "https://images.unsplash.com/photo-1587474260584-136574528ed5"
    "?q=80&w=1600&auto=format&fit=crop"
)
MAP_PREVIEW = (
    "https://images.unsplash.com/photo-1587474260584-136574528ed5"
    "?q=80&w=1200&auto=format&fit=crop"
)

DESIGN_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', system-ui, sans-serif !important;
}

.stApp {
    background: linear-gradient(180deg, #0d0b1f 0%, #1a0b2e 45%, #151024 100%) !important;
}

.block-container {
    max-width: 56rem !important;
    padding-top: 5rem !important;
    padding-bottom: 3rem !important;
}

#MainMenu, footer, header[data-testid="stHeader"] {
    visibility: hidden !important;
    height: 0 !important;
}

[data-testid="stSidebar"] {
    display: none !important;
}

[data-testid="stAppViewContainer"] > section.main {
    background: transparent !important;
}

h1, h2, h3, h4, p, label, .stMarkdown, span {
    color: #e7defb;
}

.stCaption, .stMarkdown small {
    color: #d1c2d2 !important;
}

/* Pills / segmented controls */
[data-testid="stPills"] button {
    border: 1px solid #4e4350 !important;
    background: #1d182d !important;
    color: #d1c2d2 !important;
    border-radius: 9999px !important;
    font-weight: 500 !important;
    transition: background 0.2s ease, border-color 0.2s ease, color 0.2s ease,
        box-shadow 0.2s ease, transform 0.15s ease !important;
}

@media (hover: hover) {
    [data-testid="stPills"] button:hover:not([aria-pressed="true"]) {
        background: #2c273c !important;
        border-color: #7a6a7d !important;
        color: #e7defb !important;
        transform: translateY(-1px);
    }

    [data-testid="stPills"] button[aria-pressed="true"]:hover {
        box-shadow: 0 0 16px rgba(157, 80, 187, 0.35) !important;
    }
}

[data-testid="stPills"] button[aria-pressed="true"] {
    background: rgba(157, 80, 187, 0.15) !important;
    border-color: #9d50bb !important;
    color: #edb1ff !important;
}

[data-testid="stPills"] button[kind="primary"] {
    background: #9d50bb !important;
    color: #fff3fd !important;
    border-color: #9d50bb !important;
}

div[data-baseweb="select"] > div {
    background: #211d31 !important;
    border-color: #4e4350 !important;
}

.stButton > button {
    transition: background 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease,
        transform 0.15s ease, filter 0.2s ease !important;
}

.stButton > button[kind="primary"] {
    background: #9d50bb !important;
    color: #fff3fd !important;
    border: none !important;
    border-radius: 1rem !important;
    font-weight: 600 !important;
    box-shadow: 0 0 20px rgba(157, 80, 187, 0.35) !important;
    width: 100%;
}

@media (hover: hover) {
    .stButton > button[kind="primary"]:hover:not(:disabled) {
        box-shadow: 0 0 32px rgba(157, 80, 187, 0.55) !important;
        filter: brightness(1.08);
        transform: translateY(-2px);
    }

    .stButton > button[kind="primary"]:active:not(:disabled) {
        transform: scale(0.98) translateY(0) !important;
        box-shadow: 0 0 18px rgba(157, 80, 187, 0.4) !important;
    }

    .stButton > button[kind="secondary"]:hover:not(:disabled) {
        background: #2c273c !important;
        border-color: #9d50bb !important;
        color: #edb1ff !important;
        transform: translateY(-1px);
    }

    .stButton > button[kind="secondary"]:active:not(:disabled) {
        transform: scale(0.98) !important;
    }
}

.stButton > button[kind="secondary"] {
    background: transparent !important;
    color: #e7defb !important;
    border: 1px solid #4e4350 !important;
    border-radius: 1rem !important;
}

/* HTML CTA (matches .btn-primary on Next.js) */
a.btn-primary-cta {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    margin: 1.5rem auto 0;
    padding: 1rem 2rem;
    border-radius: 1rem;
    background: #9d50bb;
    color: #fff3fd !important;
    font-weight: 600;
    text-decoration: none !important;
    box-shadow: 0 0 20px rgba(157, 80, 187, 0.35);
    transition: transform 0.2s ease, box-shadow 0.2s ease, filter 0.2s ease;
}

@media (hover: hover) {
    a.btn-primary-cta:hover {
        box-shadow: 0 0 32px rgba(157, 80, 187, 0.55);
        filter: brightness(1.08);
        transform: translateY(-2px);
    }

    a.btn-primary-cta:active {
        transform: scale(0.98);
    }
}

div[data-testid="stMetric"] {
    background: #211d31;
    border: 1px solid #4e4350;
    border-radius: 1rem;
    padding: 0.75rem 1rem;
}

div[data-testid="stMetricValue"] {
    color: #edb1ff !important;
}

div[data-testid="stMetricLabel"] {
    color: #d1c2d2 !important;
}

.stAlert {
    border-radius: 0.75rem !important;
}

/* Toggle */
[data-testid="stToggle"] label span {
    color: #e7defb !important;
}

@media (hover: hover) {
    [data-testid="stToggle"]:hover label span {
        color: #edb1ff !important;
    }
}

a.tp-back-link {
    color: #edb1ff !important;
    text-decoration: none !important;
    transition: color 0.2s ease, opacity 0.2s ease;
}

@media (hover: hover) {
    a.tp-back-link:hover {
        color: #fff3fd !important;
        text-decoration: underline !important;
    }
}

/* Custom components */
.tp-header {
    position: fixed;
    top: 0; left: 0; right: 0;
    z-index: 999;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 4rem;
    padding: 0 1.25rem;
    border-bottom: 1px solid #4e4350;
    background: rgba(21, 16, 36, 0.85);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
}

.tp-brand {
    font-size: 1.25rem;
    font-weight: 700;
    color: #edb1ff !important;
    text-decoration: none;
}

.tp-nav { display: flex; gap: 1.5rem; align-items: center; }

.tp-nav a {
    font-size: 0.875rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: #d1c2d2 !important;
    text-decoration: none;
    font-weight: 500;
}

.tp-nav a {
    transition: color 0.2s ease, opacity 0.2s ease;
}

@media (hover: hover) {
    .tp-nav a:hover { color: #edb1ff !important; }
    .tp-nav a.active:hover { color: #fff3fd !important; }
    .tp-brand:hover { filter: brightness(1.15); }
    .tp-badge:hover {
        border-color: #7a6a7d;
        background: #3f3a52;
    }
}

.tp-nav a.active { color: #edb1ff !important; font-weight: 700; }

.tp-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.35rem 0.75rem;
    border-radius: 9999px;
    border: 1px solid #4e4350;
    background: #373247;
    font-size: 0.7rem;
    color: #d1c2d2 !important;
}

.tp-badge .dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #4ade80;
}

.tp-hero {
    position: relative;
    overflow: hidden;
    border-radius: 1.5rem;
    border: 1px solid #4e4350;
    padding: 2rem 2rem 2.5rem;
    margin-bottom: 1.5rem;
    background: #211d31;
}

.tp-hero.mesh {
    background-image:
        radial-gradient(at 0% 0%, rgba(157, 80, 187, 0.15) 0px, transparent 50%),
        radial-gradient(at 100% 0%, rgba(93, 217, 208, 0.1) 0px, transparent 50%),
        radial-gradient(at 100% 100%, rgba(237, 177, 255, 0.05) 0px, transparent 50%);
    background-color: #211d31;
    text-align: center;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

@media (hover: hover) {
    .tp-hero.mesh:hover {
        border-color: rgba(157, 80, 187, 0.45);
        box-shadow: 0 0 48px rgba(157, 80, 187, 0.14);
    }

    .tp-hero.photo:hover {
        border-color: rgba(93, 217, 208, 0.25);
    }
}

.tp-hero.photo {
    min-height: 200px;
    display: flex;
    align-items: flex-end;
    padding: 2rem;
    background-size: cover;
    background-position: center;
}

.tp-hero.photo::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(to top, #151024 0%, rgba(21,16,36,0.4) 50%, transparent 100%);
}

.tp-hero.photo > * { position: relative; z-index: 1; }

.tp-hero h1 {
    font-size: clamp(1.75rem, 4vw, 3rem);
    font-weight: 800;
    color: #e7defb !important;
    margin: 0;
    line-height: 1.15;
}

.tp-hero h1 .accent { color: #edb1ff; }

.tp-hero p {
    color: #d1c2d2 !important;
    margin-top: 0.75rem;
    max-width: 36rem;
}

.tp-hero.photo h1 { font-size: 2rem; }

.glass-card {
    border: 1px solid #4e4350;
    border-radius: 1rem;
    background: #211d31;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: background-color 0.2s ease, border-color 0.2s ease,
        box-shadow 0.2s ease, transform 0.2s ease;
}

@media (hover: hover) {
    .glass-card-hover:hover,
    .glass-card.feature:hover {
        background: #1d182d !important;
        border-color: #6b5a6d !important;
        box-shadow: 0 8px 28px rgba(0, 0, 0, 0.28);
        transform: translateY(-2px);
    }

    .glass-card.feature.accent-primary:hover .feature-icon {
        border-color: #edb1ff !important;
        box-shadow: 0 0 14px rgba(237, 177, 255, 0.3);
    }

    .glass-card.feature.accent-secondary:hover .feature-icon {
        border-color: #5dd9d0 !important;
        box-shadow: 0 0 14px rgba(93, 217, 208, 0.3);
    }

    .glass-card.feature.accent-tertiary:hover .feature-icon {
        border-color: #d6baff !important;
        box-shadow: 0 0 14px rgba(214, 186, 255, 0.3);
    }

    .glass-card.feature:hover .feature-icon {
        transform: scale(1.06);
    }
}

.glass-card.feature {
    display: flex;
    gap: 1.25rem;
    align-items: flex-start;
}

.feature-icon {
    width: 3rem; height: 3rem;
    border-radius: 0.75rem;
    border: 1px solid #4e4350;
    background: #373247;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.25rem;
    flex-shrink: 0;
    transition: border-color 0.2s ease, box-shadow 0.2s ease, transform 0.2s ease;
}

.section-label {
    font-size: 0.75rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #d1c2d2 !important;
    font-weight: 600;
    margin-bottom: 0.75rem;
    display: block;
}

.form-panel {
    border: 1px solid #4e4350;
    border-radius: 1rem;
    background: #211d31;
    padding: 2rem;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.45);
}

.ai-toggle-box {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    padding: 1rem;
    border-radius: 0.75rem;
    border: 1px solid rgba(78, 67, 80, 0.5);
    background: #1d182d;
    margin: 1rem 0;
    transition: border-color 0.2s ease, background 0.2s ease;
}

@media (hover: hover) {
    .ai-toggle-box:hover {
        border-color: rgba(157, 80, 187, 0.4);
        background: #211d31;
    }
}

.summary-bar {
    position: sticky;
    top: 4rem;
    z-index: 50;
    margin: -1rem -1rem 1.5rem;
    padding: 0.75rem 1rem;
    border-bottom: 1px solid #4e4350;
    background: rgba(29, 24, 45, 0.92);
    backdrop-filter: blur(8px);
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
}

.summary-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    border: 1px solid rgba(93, 217, 208, 0.2);
    background: rgba(93, 217, 208, 0.1);
    font-size: 0.7rem;
    color: #5dd9d0 !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.summary-stats {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    font-size: 0.8rem;
    color: #d1c2d2 !important;
    font-variant-numeric: tabular-nums;
}

.stop-card {
    border: 1px solid #4e4350;
    border-radius: 1rem;
    background: #211d31;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: background 0.2s ease, border-color 0.2s ease,
        box-shadow 0.2s ease, transform 0.2s ease;
}

@media (hover: hover) {
    .stop-card:hover {
        background: #2c273c;
        border-color: #6b5a6d;
        box-shadow: 0 6px 24px rgba(0, 0, 0, 0.3);
        transform: translateY(-2px);
    }

    .stop-notes:hover {
        background: rgba(157, 80, 187, 0.16) !important;
        border-left-color: #edb1ff !important;
    }
}

.stop-time {
    font-size: 0.8rem;
    letter-spacing: 0.05em;
    color: #5dd9d0 !important;
    font-weight: 500;
}

.stop-cat {
    display: inline-block;
    padding: 0.15rem 0.5rem;
    border-radius: 4px;
    background: #373247;
    font-size: 0.65rem;
    font-weight: 700;
    text-transform: uppercase;
    color: #d1c2d2 !important;
    margin-left: 0.5rem;
}

.stop-name {
    font-size: 1.35rem;
    font-weight: 700;
    color: #e7defb !important;
    margin: 0.35rem 0;
}

.stop-meta { color: #d1c2d2 !important; font-size: 0.9rem; }

.stop-notes {
    margin-top: 1rem;
    padding: 0.75rem 1rem;
    border-left: 2px solid #9d50bb;
    background: rgba(157, 80, 187, 0.1);
    border-radius: 0 0.5rem 0.5rem 0;
    font-style: italic;
    color: #edb1ff !important;
    font-size: 0.9rem;
}

.map-frame {
    border: 1px solid #4e4350;
    border-radius: 1rem;
    overflow: hidden;
    margin-bottom: 1.5rem;
    background: #211d31;
    padding: 0.5rem;
    transition: border-color 0.25s ease, box-shadow 0.25s ease;
}

div[data-testid="stMap"] {
    border-radius: 0.75rem;
    overflow: hidden;
    transition: box-shadow 0.25s ease;
}

@media (hover: hover) {
    .map-frame:hover {
        border-color: #6b5a6d;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }

    .map-frame:hover div[data-testid="stMap"] {
        box-shadow: inset 0 0 0 1px rgba(157, 80, 187, 0.2);
    }
}

.map-preview-wrap {
    overflow: hidden;
    border-radius: 0.75rem;
    border: 1px solid #4e4350;
    transition: border-color 0.3s ease;
}

@media (hover: hover) {
    .map-preview-wrap:hover {
        border-color: #7a6a7d;
    }
}

.map-preview {
    height: 16rem;
    border-radius: 0.75rem;
    background-size: cover;
    background-position: center;
    position: relative;
    overflow: hidden;
    filter: grayscale(1);
    opacity: 0.55;
    transition: transform 0.7s ease, filter 0.7s ease, opacity 0.7s ease;
}

@media (hover: hover) {
    .map-preview-wrap:hover .map-preview {
        transform: scale(1.05);
        filter: grayscale(0.2);
        opacity: 0.85;
    }
}

.map-preview::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(to top, #151024, transparent 60%);
}

.map-preview .label {
    position: absolute;
    bottom: 1.25rem;
    left: 1.25rem;
    z-index: 1;
}

.map-preview .label span:first-child {
    font-size: 0.7rem;
    font-weight: 700;
    color: #edb1ff !important;
    letter-spacing: 0.1em;
}

.map-preview .label span:last-child {
    font-size: 1.5rem;
    font-weight: 700;
    color: #e7defb !important;
}

.footer-note {
    text-align: center;
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: rgba(209, 194, 210, 0.5) !important;
    margin-top: 2rem;
}

.beta-tag {
    font-size: 0.65rem;
    padding: 0.15rem 0.4rem;
    border-radius: 4px;
    border: 1px solid rgba(214, 186, 255, 0.2);
    background: rgba(214, 186, 255, 0.1);
    color: #d6baff !important;
    font-weight: 700;
    text-transform: uppercase;
}
"""


def inject_theme() -> None:
    st.markdown(f"<style>{DESIGN_CSS}</style>", unsafe_allow_html=True)
