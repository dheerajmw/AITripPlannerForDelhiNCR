#!/usr/bin/env python3
"""Refresh data/analytics_summary.json from the analytics database."""

from app.services.analytics_snapshot import analytics_snapshot_path, refresh_analytics_snapshot


def main() -> None:
    path = refresh_analytics_snapshot(force=True)
    if path is None:
        path = analytics_snapshot_path()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
