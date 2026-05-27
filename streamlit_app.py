"""
TripPilot AI — Delhi NCR (Streamlit)

Deploy on Streamlit Community Cloud with main file: streamlit_app.py
"""

from __future__ import annotations

import streamlit as st

from streamlit.bootstrap import init_backend

st.set_page_config(
    page_title="TripPilot AI — Delhi NCR",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
    .stApp { background: linear-gradient(180deg, #0d0b1f 0%, #1a0b2e 45%, #151024 100%); }
    h1, h2, h3, p, label, .stMarkdown { color: #e7defb !important; }
    [data-testid="stSidebar"] { background-color: #1d182d; border-right: 1px solid #4e4350; }
    div[data-testid="stMetricValue"] { color: #edb1ff !important; }
    .stop-card {
        border: 1px solid #4e4350;
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin-bottom: 0.75rem;
        background: #211d31;
    }
    .stop-title { font-size: 1.1rem; font-weight: 700; color: #edb1ff; }
    .stop-meta { color: #d1c2d2; font-size: 0.9rem; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


@st.cache_resource(show_spinner="Starting planner…")
def _bootstrap() -> tuple[bool, str]:
    return init_backend()


def _format_inr(low: int, high: int) -> str:
    return f"₹{low:,}–₹{high:,}"


def render_plan_form() -> None:
    from app.models.itinerary import ItineraryGenerateRequest
    from app.services.ai.ai_planner import AIPlannerService
    from app.services.planner.orchestrator import PlannerOrchestrator
    from app.db.session import get_session_factory
    from app.exceptions import AppError
    from app.services.poi_service import POIService

    st.header("Plan your day")
    st.caption("Rule-based routing with optional Groq tips per stop.")

    with get_session_factory()() as db:
        poi_count = POIService(db).count()

    col1, col2 = st.columns(2)
    with col1:
        budget = st.selectbox("Budget", ["low", "medium", "high"], index=1)
        duration = st.selectbox("Duration", ["4h", "8h", "1d"], index=1)
    with col2:
        interests = st.multiselect(
            "Interests",
            ["food", "history", "nature", "nightlife"],
            default=["history", "nature"],
        )
        use_ai = st.toggle("Enhance with AI (Groq)", value=False)

    st.metric("Places in database", f"{poi_count:,}")

    if st.button("Generate itinerary", type="primary", use_container_width=True):
        if not interests:
            st.error("Select at least one interest.")
            return

        try:
            body = ItineraryGenerateRequest(
                budget=budget,
                interests=interests,
                duration=duration,
            )
        except ValueError as exc:
            st.error(str(exc))
            return

        with st.spinner("Building your route…" + (" (AI tips)" if use_ai else "")):
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
                st.error(f"Could not generate itinerary: {exc}")
                return

        st.session_state["itinerary"] = result.model_dump()
        st.success(f"Created {len(result.stops)} stops.")
        st.rerun()


def render_itinerary() -> None:
    data = st.session_state.get("itinerary")
    if not data:
        st.info("Generate a plan on the **Plan trip** page first.")
        return

    meta = data["meta"]
    summary = data["summary"]
    stops = data["stops"]

    st.header("Your itinerary")
    badges = []
    if meta.get("planner_mode") == "ai":
        badges.append("AI-enhanced")
    if meta.get("routing_source"):
        badges.append(f"routing: {meta['routing_source']}")
    if badges:
        st.caption(" · ".join(badges))

    for warning in meta.get("warnings") or []:
        st.warning(warning)
    if meta.get("fallback_reason"):
        st.info(f"AI fallback: {meta['fallback_reason']}")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Stops", summary["total_stops"])
    m2.metric("Travel (min)", summary["total_travel_min"])
    m3.metric("Visit (min)", summary.get("total_visit_min", 0))
    cost = summary["total_cost_inr"]
    m4.metric("Est. cost", _format_inr(cost["low"], cost["high"]))

    if stops:
        import pandas as pd

        map_df = pd.DataFrame(
            {
                "lat": [s["lat"] for s in stops],
                "lon": [s["lon"] for s in stops],
                "name": [s["name"] for s in stops],
            }
        )
        st.subheader("Map")
        st.map(map_df, latitude="lat", longitude="lon", zoom=11)

    st.subheader("Timeline")
    for stop in stops:
        cost_stop = stop["cost_estimate_inr"]
        travel = stop.get("travel_to_next_minutes")
        travel_txt = f" · {travel} min to next" if travel is not None else ""
        st.markdown(
            f"""
            <div class="stop-card">
              <div class="stop-title">{stop['order']}. {stop['name']}</div>
              <div class="stop-meta">
                {stop['category']} · {stop['arrive_at']} – {stop['depart_at']}
                · visit {stop['visit_minutes']} min{travel_txt}
                · {_format_inr(cost_stop['low'], cost_stop['high'])}
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if stop.get("notes"):
            st.caption(stop["notes"])

    st.caption("Costs are rough estimates for planning only.")


def main() -> None:
    ok, bootstrap_msg = _bootstrap()
    if not ok:
        st.error("Cannot start planner")
        st.markdown(bootstrap_msg)
        st.markdown(
            """
            **Streamlit Cloud setup**
            1. Upload `data/pois.db` to a GitHub Release (or cloud storage).
            2. In app **Settings → Secrets**, add:
            ```
            POI_DB_DOWNLOAD_URL = "https://github.com/.../pois.db"
            GROQ_API_KEY = "..."   # optional, for AI tips
            ```
            3. Reboot the app.

            **Local:** run `make ingest`, then `streamlit run streamlit_app.py`
            """
        )
        return

    st.sidebar.title("🧭 TripPilot AI")
    st.sidebar.caption("Delhi NCR day scout")
    st.sidebar.success(bootstrap_msg)

    page = st.sidebar.radio(
        "Navigate",
        ["Plan trip", "Itinerary"],
        label_visibility="collapsed",
    )

    if page == "Plan trip":
        render_plan_form()
    else:
        render_itinerary()

    st.sidebar.divider()
    st.sidebar.markdown(
        "[GitHub](https://github.com/dheerajmw/AITripPlannerForDelhiNCR) · "
        "Built with FastAPI + Streamlit"
    )


if __name__ == "__main__":
    main()
