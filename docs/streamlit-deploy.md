# Streamlit deployment

Deploy the **TripPilot AI** UI on [Streamlit Community Cloud](https://streamlit.io/cloud) without running Next.js or a separate FastAPI process. The Streamlit app imports the Python backend directly.

## Entry point

| File | Purpose |
|------|---------|
| `streamlit_app.py` | Main app (set this as the Cloud **Main file path**) |
| `requirements.txt` | Python dependencies (repo root) |
| `.streamlit/config.toml` | Theme and server options |
| `trippilot_deploy/bootstrap.py` | Path setup, secrets, POI DB download (not named `streamlit/` — avoids import clash with the Streamlit library) |

## Local run

```bash
cd /path/to/AITripPlanner
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e backend/.   # optional; app uses sys.path if skipped

make ingest                # creates data/pois.db (~2.4 MB)
cp backend/.env.example backend/.env   # add GROQ_API_KEY for AI mode

streamlit run streamlit_app.py
```

Open http://localhost:8501

## Streamlit Cloud (GitHub)

1. Push this repo to GitHub.
2. **Share → Streamlit Cloud → New app** → select repo.
3. **Main file path:** `streamlit_app.py`
4. **App URL** (optional): customize subdomain.

### Secrets (Settings → Secrets) — optional for POI DB

The app **auto-downloads** the POI database from the public release on first start:

`https://github.com/dheerajmw/AITripPlannerForDelhiNCR/releases/download/v0.1.0-poi/pois.db`

You only need secrets if you override that URL or want AI tips:

```toml
GROQ_API_KEY = "your-groq-key"
OSRM_BASE_URL = "http://router.project-osrm.org"
# POI_DB_DOWNLOAD_URL = "..."   # optional override
```

First boot on Cloud may take **30–60 seconds** while `pois.db` (~2.4 MB) downloads.

### Refresh the hosted POI database

```bash
make ingest
./scripts/publish-poi-release.sh v0.1.0-poi
```

## What runs in Streamlit

- Same planner as the API: `PlannerOrchestrator`, optional `AIPlannerService`
- SQLite POI DB under `data/pois.db`
- OSRM walking matrix (HTTP public demo; see README TLS note)

## Limits

- No Next.js UI on Streamlit; map uses `st.map` (simpler than Leaflet).
- Cold start downloads POI DB once (cached on disk until redeploy).
- Public OSRM demo has rate limits; production should use a dedicated OSRM instance.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| “POI database not found” | Set `POI_DB_DOWNLOAD_URL` or run `make ingest` locally |
| “No POIs match interests” | DB empty or corrupt; re-download or re-ingest |
| OSRM warning | Set `OSRM_BASE_URL=http://router.project-osrm.org` in secrets |
| AI tips fail | Set `GROQ_API_KEY`; rule-based mode still works |
