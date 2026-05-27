#!/usr/bin/env bash
# Upload data/pois.db to GitHub Releases for Streamlit Cloud (run after make ingest).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DB="$ROOT/data/pois.db"
TAG="${1:-v0.1.0-poi}"

if [[ ! -f "$DB" ]]; then
  echo "Missing $DB — run: make ingest"
  exit 1
fi

echo "Publishing $DB to release $TAG ..."
gh release upload "$TAG" "$DB" --clobber --repo dheerajmw/AITripPlannerForDelhiNCR 2>/dev/null || \
  gh release create "$TAG" "$DB" \
    --repo dheerajmw/AITripPlannerForDelhiNCR \
    --title "POI database for Streamlit Cloud" \
    --notes "SQLite POI database for TripPilot AI Streamlit deployment."

echo "Done. URL:"
echo "  https://github.com/dheerajmw/AITripPlannerForDelhiNCR/releases/download/${TAG}/pois.db"
