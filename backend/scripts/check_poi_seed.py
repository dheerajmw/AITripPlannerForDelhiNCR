#!/usr/bin/env python3
"""Verify POI database meets minimum seed requirements (Phase 1 gate)."""

import sys
from pathlib import Path

_BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(_BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(_BACKEND_ROOT))

from app.config import MIN_POI_SEED_COUNT, SUPPORTED_POI_CATEGORIES
from app.db.repository import POIRepository
from app.db.session import get_session_factory, init_db


def main() -> int:
    init_db()
    session = get_session_factory()()
    try:
        repo = POIRepository(session)
        total = repo.count()
        print(f"Total POIs: {total}")
        by_cat = dict(repo.count_by_category())
        for cat in SUPPORTED_POI_CATEGORIES:
            print(f"  {cat}: {by_cat.get(cat, 0)}")

        monument_count = by_cat.get("monument", 0) + by_cat.get("attraction", 0) + by_cat.get("museum", 0)
        if monument_count < 20:
            print(f"FAIL: monument-like POIs {monument_count} < 20")
            return 1
        if total < MIN_POI_SEED_COUNT:
            print(f"FAIL: total {total} < {MIN_POI_SEED_COUNT}")
            return 1
        print("OK: seed requirements met")
        return 0
    finally:
        session.close()


if __name__ == "__main__":
    raise SystemExit(main())
