"""
Trip Pilot — Delhi NCR (Streamlit)

Purple Aurora UI — matches the Next.js frontend.
Deploy with main file: streamlit_app.py
"""

from __future__ import annotations

import streamlit as st

from trippilot_deploy.bootstrap import configure_import_path, init_backend

configure_import_path()

from app.config import DEFAULT_START, NCR_START_LOCATIONS
from trippilot_deploy.theme import (
    inject_header_styles,
    inject_itinerary_layout_styles,
    inject_plan_form_styles,
    inject_theme,
)
from trippilot_deploy.ui import (
    NAV_LABELS,
    NAV_LABEL_TO_PAGE,
    NAV_PAGES,
    NAV_PAGE_TO_LABEL,
    aurora_background_html,
    empty_itinerary_html,
    google_maps_route_url,
    hero_plan,
    home_page_html,
    itinerary_header_block,
    map_shell_close,
    map_shell_open,
    nav_actions_html,
    nav_brand_html,
    stats_panel_html,
    stop_card_html,
)

st.set_page_config(
    page_title="Trip Pilot — Delhi NCR",
    page_icon="✈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_theme()

PAGES = ("home", "plan", "itinerary")

_START_LABELS = [str(loc["label"]) for loc in NCR_START_LOCATIONS]
_START_BY_LABEL = {str(loc["label"]): loc for loc in NCR_START_LOCATIONS}


def _default_start_label() -> str:
    return str(DEFAULT_START["label"])


def _current_page() -> str:
    page = st.session_state.get("page", "home")
    return page if page in PAGES else "home"


def _go(page: str) -> None:
    st.session_state["page"] = page
    st.rerun()


def _on_main_nav_change() -> None:
    label = st.session_state.get("main_nav_segment")
    page = NAV_LABEL_TO_PAGE.get(label)
    if page:
        st.session_state["page"] = page


def _sync_nav_segment(active: str) -> None:
    """Align tab widget with `page` when navigation came from elsewhere (not the segment)."""
    if NAV_LABEL_TO_PAGE.get(st.session_state.get("main_nav_segment")) != active:
        st.session_state["main_nav_segment"] = NAV_PAGE_TO_LABEL.get(active, "Explore")


def render_app_header(active: str, poi_count: int | None, *, api_ready: bool = True) -> None:
    """Sticky header — native Streamlit widgets (CSS sibling hacks do not work)."""
    inject_header_styles()

    with st.container(border=True):
        brand_col, nav_col, actions_col = st.columns([1.15, 2.1, 1.15], gap="small")

        with brand_col:
            st.markdown(nav_brand_html(), unsafe_allow_html=True)

        with nav_col:
            _sync_nav_segment(active)
            if hasattr(st, "segmented_control"):
                st.segmented_control(
                    "Section",
                    list(NAV_LABELS),
                    key="main_nav_segment",
                    on_change=_on_main_nav_change,
                    label_visibility="collapsed",
                )
            else:
                tab_cols = st.columns(3, gap="small")
                for col, (page_id, label) in zip(tab_cols, zip(NAV_PAGES, NAV_LABELS)):
                    with col:
                        if st.button(
                            label,
                            key=f"nav_tab_{page_id}",
                            use_container_width=True,
                            type="primary" if active == page_id else "secondary",
                        ):
                            _go(page_id)

        with actions_col:
            st.markdown(
                nav_actions_html(poi_count, api_ready=api_ready),
                unsafe_allow_html=True,
            )


@st.cache_resource(show_spinner="Starting Trip Pilot…")
def _bootstrap() -> tuple[bool, str]:
    return init_backend()


def _poi_count() -> int:
    from app.db.session import get_session_factory
    from app.services.poi_service import POIService

    with get_session_factory()() as db:
        return POIService(db).count()


def _shell_start(page: str, poi_count: int | None, *, api_ready: bool = True) -> None:
    show_map = page == "home"
    st.markdown(aurora_background_html(show_map=show_map), unsafe_allow_html=True)
    render_app_header(page, poi_count, api_ready=api_ready)


def _resolve_start(label: str) -> dict:
    return _START_BY_LABEL.get(label, _START_BY_LABEL[_default_start_label()])


def render_home() -> None:
    st.markdown(home_page_html(), unsafe_allow_html=True)
    _, center, _ = st.columns([1, 2, 1])
    with center:
        if st.button("✨ Generate AI Itinerary", type="primary", use_container_width=True):
            _go("plan")


def render_plan(poi_count: int) -> None:
    from app.exceptions import AppError
    from app.models.itinerary import ItineraryGenerateRequest
    from app.services.ai.ai_planner import AIPlannerService
    from app.services.planner.orchestrator import PlannerOrchestrator
    from app.db.session import get_session_factory

    inject_plan_form_styles()
    st.markdown(
        f'<div class="tp-page-narrow">{hero_plan()}</div>',
        unsafe_allow_html=True,
    )

    default_label = st.session_state.get("start_label", _default_start_label())
    if default_label not in _START_LABELS:
        default_label = _default_start_label()
    default_idx = _START_LABELS.index(default_label)

    with st.container(border=True):
        col_left, col_right = st.columns(2, gap="large")

        with col_left:
            st.markdown(
                '<div class="form-field-block">'
                '<span class="section-label">Region</span>'
                '<div class="region-chip-row"><span class="preview-chip preview-chip-active">'
                "📍 Delhi NCR</span></div></div>",
                unsafe_allow_html=True,
            )

            st.markdown(
                '<div class="form-field-block">'
                '<span class="section-label">Starting location</span></div>',
                unsafe_allow_html=True,
            )
            start_label = st.selectbox(
                "Starting location",
                _START_LABELS,
                index=default_idx,
                label_visibility="collapsed",
                help="Route begins at a landmark within Delhi NCR only.",
            )

            from datetime import date as date_cls

            plan_date = st.date_input(
                "Trip date (weather-aware)",
                value=date_cls.today(),
                help="Forecast adjusts indoor/outdoor stops for the next 5 days.",
            )

            duration = st.pills(
                "Travel Duration",
                ["4h", "8h", "1d"],
                default="8h",
                selection_mode="single",
                key="pill_duration",
            )

        with col_right:
            budget = st.pills(
                "Estimated Budget",
                ["low", "medium", "high"],
                default="medium",
                selection_mode="single",
                key="pill_budget",
            )
            interests = st.pills(
                "Interests",
                ["food", "history", "nature", "nightlife"],
                default=["history", "nature"],
                selection_mode="multi",
                key="pill_interests",
            )

        use_ai = st.toggle(
            "Enhance with AI (Groq) — real-time tips per stop",
            value=st.session_state.get("use_ai", False),
        )
        st.caption(f"{poi_count:,} places in database · starting near {start_label}")

        if st.button("✨ Generate AI Itinerary", type="primary", use_container_width=True):
            if not interests:
                st.error("Select at least one interest.")
            else:
                start = _resolve_start(start_label)
                try:
                    body = ItineraryGenerateRequest(
                        budget=budget or "medium",
                        interests=list(interests),
                        duration=duration or "8h",
                        start_lat=float(start["lat"]),
                        start_lon=float(start["lon"]),
                        start_label=str(start["label"]),
                        plan_date=plan_date.isoformat() if plan_date else None,
                    )
                except ValueError as exc:
                    st.error(str(exc))
                else:
                    with st.spinner(
                        "Crafting your expedition…" + (" (Groq tips)" if use_ai else "")
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
                            st.session_state["start_label"] = start_label
                            _go("itinerary")


def render_itinerary() -> None:
    inject_itinerary_layout_styles()

    data = st.session_state.get("itinerary")
    if not data:
        st.markdown(
            f'<div class="tp-page-narrow">{empty_itinerary_html()}</div>',
            unsafe_allow_html=True,
        )
        _, center, _ = st.columns([1, 2, 1])
        with center:
            if st.button("✨ Generate AI Itinerary", type="primary", use_container_width=True):
                _go("plan")
        return

    meta = data["meta"]
    summary = data["summary"]
    stops = data["stops"]

    st.markdown(itinerary_header_block(meta, summary), unsafe_allow_html=True)

    for warning in meta.get("warnings") or []:
        st.warning(warning)
    if meta.get("fallback_reason"):
        st.info(f"AI fallback: {meta['fallback_reason']}")

    col_timeline, col_side = st.columns([3, 2], gap="large")

    with col_timeline:
        st.markdown('<span class="section-label">Timeline</span>', unsafe_allow_html=True)
        for stop in stops:
            st.markdown(stop_card_html(stop), unsafe_allow_html=True)

    with col_side:
        if stops:
            import pandas as pd

            st.markdown(map_shell_open(), unsafe_allow_html=True)
            map_df = pd.DataFrame(
                {"lat": [s["lat"] for s in stops], "lon": [s["lon"] for s in stops]}
            )
            st.map(map_df, latitude="lat", longitude="lon", zoom=11, height=280)
            gmaps_url = google_maps_route_url(data)
            if gmaps_url:
                st.markdown(
                    f'<a class="gmaps-link" href="{gmaps_url}" target="_blank" '
                    f'rel="noopener">📍 Open full route in Google Maps</a>',
                    unsafe_allow_html=True,
                )
            st.markdown(map_shell_close(), unsafe_allow_html=True)

        st.markdown(stats_panel_html(meta, summary), unsafe_allow_html=True)

    st.markdown('<div class="itinerary-actions-marker" aria-hidden="true"></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap="medium")
    with c1:
        if st.button("↻ Regenerate", type="primary", use_container_width=True):
            _regenerate_itinerary()
    with c2:
        if st.button("＋ Plan another day", use_container_width=True):
            _go("plan")


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
    start_label = st.session_state.get("start_label", _default_start_label())
    start = _resolve_start(start_label)
    sp = meta.get("start_point")
    if sp and sp.get("label"):
        start = _START_BY_LABEL.get(str(sp["label"]), start)

    body = ItineraryGenerateRequest(
        budget=meta.get("budget_tier", "medium"),
        interests=st.session_state.get("last_interests", ["history", "nature"]),
        duration=_duration_key(meta.get("duration_minutes", 480)),
        start_lat=float(start.get("lat", sp["lat"] if sp else DEFAULT_START["lat"])),
        start_lon=float(start.get("lon", sp["lon"] if sp else DEFAULT_START["lon"])),
        start_label=str(start.get("label", sp.get("label") if sp else DEFAULT_START["label"])),
        plan_date=meta.get("plan_date"),
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

    _shell_start(page, poi_count if ok else None, api_ready=ok)

    if not ok:
        st.error("Cannot start planner")
        st.markdown(bootstrap_msg)
        st.markdown(
            "Reboot the app on Streamlit Cloud — the POI database downloads automatically (~1 min)."
        )
        return

    if page == "home":
        render_home()
    elif page == "plan":
        render_plan(poi_count or 0)
    else:
        render_itinerary()


main()
