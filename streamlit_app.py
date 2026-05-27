"""
TripPilot AI — Delhi NCR (Streamlit)

Matches the Next.js UI (dark Voyager theme). Deploy with main file: streamlit_app.py
"""

from __future__ import annotations

import streamlit as st

from trippilot_deploy.bootstrap import init_backend
from trippilot_deploy.theme import inject_theme
from trippilot_deploy.ui import (
    cta_button_html,
    feature_card,
    header_html,
    hero_home,
    hero_plan,
    map_preview_block,
    stop_card_html,
    summary_bar_html,
)

st.set_page_config(
    page_title="TripPilot AI — Delhi NCR",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_theme()

PAGES = ("home", "plan", "itinerary")


def _current_page() -> str:
    raw = st.query_params.get("page", "home")
    page = raw[0] if isinstance(raw, list) else raw
    return page if page in PAGES else "home"


def _go(page: str) -> None:
    st.query_params["page"] = page
    st.rerun()


@st.cache_resource(show_spinner="Starting TripPilot AI…")
def _bootstrap() -> tuple[bool, str]:
    return init_backend()


def _poi_count() -> int:
    from app.db.session import get_session_factory
    from app.services.poi_service import POIService

    with get_session_factory()() as db:
        return POIService(db).count()


def _format_inr(low: int, high: int) -> str:
    return f"₹{low:,}–₹{high:,}"


def render_home(poi_count: int) -> None:
    st.markdown(hero_home(), unsafe_allow_html=True)
    st.markdown(cta_button_html("Start planning →", "plan"), unsafe_allow_html=True)

    st.markdown('<span class="section-label">Capabilities</span>', unsafe_allow_html=True)
    st.markdown(
        feature_card(
            "🗺️",
            "Real OSM venues",
            "Accurate geospatial data for cafes, monuments, and metro stations in NCR.",
            accent="primary",
        ),
        unsafe_allow_html=True,
    )
    st.markdown(
        feature_card(
            "👣",
            "Optimized walking route",
            "Smart pathfinding for Delhi street layout and pedestrian shortcuts.",
            accent="secondary",
        ),
        unsafe_allow_html=True,
    )
    st.markdown(
        feature_card(
            "✨",
            "Optional AI tips",
            "Peak hours, local etiquette, and hidden spots from Groq.",
            beta=True,
            accent="tertiary",
        ),
        unsafe_allow_html=True,
    )
    st.markdown(map_preview_block(), unsafe_allow_html=True)
    st.markdown(
        '<p class="footer-note">Estimates only · MVP · No bookings or tickets</p>',
        unsafe_allow_html=True,
    )


def render_plan(poi_count: int) -> None:
    from app.exceptions import AppError
    from app.models.itinerary import ItineraryGenerateRequest
    from app.services.ai.ai_planner import AIPlannerService
    from app.services.planner.orchestrator import PlannerOrchestrator
    from app.db.session import get_session_factory

    st.markdown(hero_plan(), unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="form-panel">', unsafe_allow_html=True)

        budget = st.pills(
            "Estimated Budget",
            ["low", "medium", "high"],
            default="medium",
            selection_mode="single",
            key="pill_budget",
        )
        interests = st.pills(
            "Primary Interests",
            ["food", "history", "nature", "nightlife"],
            default=["history", "nature"],
            selection_mode="multi",
            key="pill_interests",
        )
        duration = st.pills(
            "Travel Duration",
            ["4h", "8h", "1d"],
            default="8h",
            selection_mode="single",
            key="pill_duration",
        )

        st.markdown(
            """
            <div class="ai-toggle-box">
              <div>
                <strong style="color:#e7defb;">Enhance with AI (Groq)</strong>
                <p style="margin:0.25rem 0 0;font-size:0.85rem;color:#d1c2d2;">
                  Real-time tips &amp; hidden gems per stop
                </p>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        use_ai = st.toggle("Enable AI tips", value=False, label_visibility="collapsed")

        st.caption(f"{poi_count:,} places in database")

        if st.button("Generate Itinerary →", type="primary", use_container_width=True):
            if not interests:
                st.error("Select at least one interest.")
            else:
                try:
                    body = ItineraryGenerateRequest(
                        budget=budget or "medium",
                        interests=list(interests),
                        duration=duration or "8h",
                    )
                except ValueError as exc:
                    st.error(str(exc))
                else:
                    with st.spinner(
                        "Building your itinerary…" + (" (AI tips)" if use_ai else "")
                    ):
                        try:
                            with get_session_factory()() as db:
                                if use_ai:
                                    result = AIPlannerService(db).generate(body)
                                else:
                                    result = PlannerOrchestrator(db).generate(body)
                        except AppError as exc:
                            st.error(exc.message)
                        except Exception as exc:
                            st.error(f"Could not generate itinerary: {exc}")
                        else:
                            st.session_state["itinerary"] = result.model_dump()
                            st.session_state["use_ai"] = use_ai
                            st.session_state["last_interests"] = list(interests)
                            _go("itinerary")

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        '<p style="text-align:center;margin-top:1.5rem;">'
        '<a class="tp-back-link" href="?page=home">← Back to home</a></p>',
        unsafe_allow_html=True,
    )


def render_itinerary() -> None:
    data = st.session_state.get("itinerary")
    if not data:
        st.markdown(
            """
            <div class="glass-card" style="text-align:center;padding:3rem;">
              <p style="font-size:2rem;margin:0;">📍</p>
              <h2 style="color:#e7defb!important;">No itinerary yet</h2>
              <p style="color:#d1c2d2!important;">Generate a plan to see your day itinerary.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Plan your day", type="primary"):
            _go("plan")
        return

    meta = data["meta"]
    summary = data["summary"]
    stops = data["stops"]

    st.markdown(summary_bar_html(meta, summary), unsafe_allow_html=True)

    mode = "AI-enhanced" if meta.get("planner_mode") == "ai" else "Standard"
    st.markdown(
        f"### Your itinerary\n"
        f"<span style='color:#d1c2d2;'>{mode} plan · "
        f"{summary.get('total_travel_min', 0)} min walking</span>",
        unsafe_allow_html=True,
    )

    for warning in meta.get("warnings") or []:
        st.warning(warning)
    if meta.get("fallback_reason"):
        st.info(f"AI fallback: {meta['fallback_reason']}")

    if stops:
        import pandas as pd

        st.markdown('<div class="map-frame">', unsafe_allow_html=True)
        map_df = pd.DataFrame(
            {"lat": [s["lat"] for s in stops], "lon": [s["lon"] for s in stops]}
        )
        st.map(map_df, latitude="lat", longitude="lon", zoom=11, height=320)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<span class="section-label">Timeline</span>', unsafe_allow_html=True)
    for stop in stops:
        st.markdown(stop_card_html(stop), unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("↻ Regenerate", type="primary", use_container_width=True):
            _regenerate_itinerary()
    with col2:
        if st.button("＋ Plan another day", use_container_width=True):
            _go("plan")

    st.caption("Costs are rough estimates for planning only — not bookings or tickets.")


def _regenerate_itinerary() -> None:
    from app.exceptions import AppError
    from app.models.itinerary import ItineraryGenerateRequest
    from app.services.ai.ai_planner import AIPlannerService
    from app.services.planner.orchestrator import PlannerOrchestrator
    from app.db.session import get_session_factory

    prev = st.session_state.get("itinerary")
    if not prev:
        _go("plan")
        return

    meta = prev.get("meta", {})
    body = ItineraryGenerateRequest(
        budget=meta.get("budget_tier", "medium"),
        interests=st.session_state.get("last_interests", ["history", "nature"]),
        duration=_duration_key(meta.get("duration_minutes", 480)),
    )
    use_ai = st.session_state.get("use_ai", False)

    with st.spinner("Regenerating…"):
        try:
            with get_session_factory()() as db:
                if use_ai:
                    result = AIPlannerService(db).generate(body)
                else:
                    result = PlannerOrchestrator(db).generate(body)
        except AppError as exc:
            st.error(exc.message)
            return
        except Exception as exc:
            st.error(str(exc))
            return
        st.session_state["itinerary"] = result.model_dump()
        st.rerun()


def _duration_key(minutes: int) -> str:
    if minutes <= 240:
        return "4h"
    if minutes <= 480:
        return "8h"
    return "1d"


def main() -> None:
    ok, bootstrap_msg = _bootstrap()
    page = _current_page()

    poi_count: int | None = None
    if ok:
        try:
            poi_count = _poi_count()
        except Exception:
            poi_count = None

    st.markdown(header_html(page, poi_count), unsafe_allow_html=True)

    # Nav fallback (query-param links in header work on full reload; buttons always work)
    n1, n2, n3, _ = st.columns([1, 1, 1, 4])
    with n1:
        if st.button("Home", use_container_width=True, type="secondary" if page != "home" else "primary"):
            _go("home")
    with n2:
        if st.button("Plan", use_container_width=True, type="secondary" if page != "plan" else "primary"):
            _go("plan")
    with n3:
        if st.button("Itinerary", use_container_width=True, type="secondary" if page != "itinerary" else "primary"):
            _go("itinerary")

    if not ok:
        st.error("Cannot start planner")
        st.markdown(bootstrap_msg)
        st.markdown(
            "Reboot the app on Streamlit Cloud. The POI database should download automatically "
            "(~1 minute). See [docs/streamlit-deploy.md](https://github.com/dheerajmw/"
            "AITripPlannerForDelhiNCR/blob/main/docs/streamlit-deploy.md)."
        )
        return

    if page == "home":
        render_home(poi_count or 0)
    elif page == "plan":
        render_plan(poi_count or 0)
    else:
        render_itinerary()


if __name__ == "__main__":
    main()
