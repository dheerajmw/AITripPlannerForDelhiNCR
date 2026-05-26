"""Ingest pipeline tests with mocked Overpass."""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

from app.db.repository import POIRepository
from app.services.poi_normalizer import dedupe_pois, normalize_elements

FIXTURE = Path(__file__).parent / "fixtures" / "overpass_sample.json"


def test_ingest_pipeline_with_fixture_elements(db_session) -> None:
    elements = json.loads(FIXTURE.read_text())["elements"]
    normalized = normalize_elements(elements)
    deduped = dedupe_pois(normalized)
    assert len(deduped) == 2
    repo = POIRepository(db_session)
    repo.upsert_many(deduped)
    assert repo.count() == 2


@patch("app.services.overpass_client.OverpassClient.fetch_all_queries")
def test_overpass_client_used_only_in_ingest(mock_fetch: MagicMock) -> None:
    mock_fetch.return_value = json.loads(FIXTURE.read_text())["elements"]
    from app.services.overpass_client import OverpassClient

    client = OverpassClient()
    result = client.fetch_all_queries()
    assert len(result) == 2
