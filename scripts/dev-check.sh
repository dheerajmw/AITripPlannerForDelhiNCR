#!/usr/bin/env bash
# Quick check that dev servers are reachable and the planner API is wired up.
set -e
API="${API_URL:-http://127.0.0.1:8000/api/v1}"
WEB="${WEB_URL:-http://127.0.0.1:3000}"

echo "Checking backend at $API/health ..."
HEALTH_JSON=$(curl -sf "$API/health" 2>/dev/null) || {
  echo "  FAIL — nothing on port 8000. Run: make dev-backend"
  exit 1
}
echo "  OK backend"
echo "  $HEALTH_JSON"

POI_COUNT=$(echo "$HEALTH_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin).get('poi_count'))" 2>/dev/null || echo "None")
if [ "$POI_COUNT" = "None" ] || [ "$POI_COUNT" = "null" ] || [ -z "$POI_COUNT" ]; then
  echo "  WARN — poi_count is missing. You may have an OLD backend on :8000."
  echo "        Kill it and restart from this repo: make dev-backend"
  exit 1
fi

echo "Checking planner endpoint $API/itinerary/generate ..."
PROBE='{"budget":"medium","interests":["history","nature"],"duration":"8h"}'
HTTP_CODE=$(curl -s -o /tmp/aitp-probe.json -w "%{http_code}" -X POST \
  "$API/itinerary/generate?mode=rule" \
  -H "Content-Type: application/json" \
  -d "$PROBE")
if [ "$HTTP_CODE" = "404" ]; then
  echo "  FAIL — itinerary route returned 404 (wrong/stale API on port 8000)."
  echo "        Stop other Python servers on :8000, then: make dev-backend"
  exit 1
fi
if [ "$HTTP_CODE" != "200" ]; then
  echo "  FAIL — itinerary returned HTTP $HTTP_CODE"
  head -c 200 /tmp/aitp-probe.json 2>/dev/null || true
  echo ""
  exit 1
fi
echo "  OK planner (sample itinerary generated)"

echo "Checking frontend at $WEB ..."
if curl -sf -o /dev/null "$WEB"; then
  echo "  OK frontend"
else
  echo "  FAIL — start frontend: make dev-frontend"
  echo "  (Browser 'connection failed' usually means nothing is on port 3000.)"
  exit 1
fi

echo "All good. Open $WEB/plan and generate an itinerary."
