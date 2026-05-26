#!/usr/bin/env python3
"""Fetch Delhi NCR POIs from Overpass and upsert into SQLite."""

import logging
import sys
from pathlib import Path

# Allow running as script from backend/
_BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(_BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(_BACKEND_ROOT))

from app.db.repository import POIRepository
from app.db.session import get_session_factory, init_db
from app.services.overpass_client import OverpassClient
from app.services.poi_normalizer import dedupe_pois, normalize_elements

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def main() -> int:
    logger.info("Initializing database...")
    init_db()

    client = OverpassClient()
    logger.info("Fetching POIs from Overpass (this may take a few minutes)...")
    elements = client.fetch_all_queries()
    logger.info("Received %d raw OSM elements", len(elements))

    normalized = normalize_elements(elements)
    logger.info("Normalized to %d POIs", len(normalized))

    deduped = dedupe_pois(normalized)
    logger.info("After dedupe: %d POIs", len(deduped))

    session = get_session_factory()()
    try:
        repo = POIRepository(session)
        count = repo.upsert_many(deduped)
        logger.info("Upserted %d POIs into database", count)
        by_cat = repo.count_by_category()
        for cat, n in by_cat:
            logger.info("  %s: %d", cat, n)
        logger.info("Total POIs: %d", repo.count())
    finally:
        session.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
