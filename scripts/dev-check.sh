#!/usr/bin/env bash
# Quick check that dev servers are reachable.
set -e
API="${API_URL:-http://127.0.0.1:8000/api/v1}"
WEB="${WEB_URL:-http://127.0.0.1:3000}"

echo "Checking backend at $API/health ..."
if curl -sf "$API/health" >/dev/null; then
  echo "  OK backend"
  curl -s "$API/health" | head -c 120
  echo ""
else
  echo "  FAIL — start backend: make dev-backend"
  exit 1
fi

echo "Checking frontend at $WEB ..."
if curl -sf -o /dev/null "$WEB"; then
  echo "  OK frontend"
else
  echo "  FAIL — start frontend: make dev-frontend"
  echo "  (Browser 'connection failed' usually means nothing is on port 3000.)"
  exit 1
fi

echo "All good. Open $WEB in your browser."
