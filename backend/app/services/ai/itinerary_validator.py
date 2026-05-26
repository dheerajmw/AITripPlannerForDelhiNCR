"""Validate Groq JSON output against allowed POI ids (Pattern A: notes only)."""

from typing import Dict, Set

from app.config import AI_NOTES_MAX_LENGTH


class ItineraryValidationError(ValueError):
    pass


class ItineraryValidator:
    def extract_notes(
        self,
        raw: dict,
        *,
        allowed_ids: Set[str],
        required_ids: Set[str],
    ) -> Dict[str, str]:
        stops_raw = raw.get("stops")
        if not isinstance(stops_raw, list):
            raise ItineraryValidationError("Response must include a stops array")

        notes: Dict[str, str] = {}
        for item in stops_raw:
            if not isinstance(item, dict):
                raise ItineraryValidationError("Each stop must be an object")
            poi_id = item.get("poi_id")
            if not poi_id or not isinstance(poi_id, str):
                raise ItineraryValidationError("Each stop must include poi_id")
            if poi_id not in allowed_ids:
                raise ItineraryValidationError(f"Unknown poi_id: {poi_id}")
            text = str(item.get("notes", "") or "").strip()
            notes[poi_id] = text[:AI_NOTES_MAX_LENGTH]

        unknown_in_response = set(notes.keys()) - allowed_ids
        if unknown_in_response:
            raise ItineraryValidationError(f"Unknown poi_ids: {sorted(unknown_in_response)}")

        missing = required_ids - set(notes.keys())
        if missing:
            raise ItineraryValidationError(f"Missing notes for poi_ids: {sorted(missing)}")

        return notes
