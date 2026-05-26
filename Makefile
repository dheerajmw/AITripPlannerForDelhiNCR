.PHONY: dev dev-backend dev-frontend test test-backend test-frontend install ingest

# Run backend + frontend together
dev:
	npm run dev

PY ?= python3
# Paths relative to backend/ when recipes use `cd backend && …`
BACKEND_PY := $(if $(wildcard backend/.venv/bin/python),.venv/bin/python,$(PY))

dev-backend:
	cd backend && $(BACKEND_PY) -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend:
	cd frontend && npm run dev

test: test-backend test-frontend

test-backend:
	cd backend && $(BACKEND_PY) -m pytest

test-frontend:
	cd frontend && npm test

install:
	cd backend && $(BACKEND_PY) -m pip install -e ".[dev]"
	cd frontend && npm install
	npm install

# Phase 1: Overpass → SQLite
ingest:
	cd backend && .venv/bin/python scripts/ingest_pois.py

check-pois:
	cd backend && .venv/bin/python scripts/check_poi_seed.py
