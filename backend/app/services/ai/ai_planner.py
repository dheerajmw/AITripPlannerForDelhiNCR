"""AI mode: rule-based draft + Groq note enrichment with fallback."""

import logging
from typing import List, Optional

from sqlalchemy.orm import Session

from app.db.repository import POIRepository
from app.models.itinerary import (
    ItineraryGenerateRequest,
    ItineraryMeta,
    ItineraryResponse,
    ItineraryStop,
)
from app.services.ai.context_builder import ContextBuilder
from app.services.ai.groq_client import (
    GroqClient,
    GroqClientError,
    GroqInvalidJsonError,
    GroqRateLimitError,
    GroqTimeoutError,
)
from app.services.ai.itinerary_validator import ItineraryValidationError, ItineraryValidator
from app.services.ai.prompts import JSON_RETRY_SUFFIX, SYSTEM_PROMPT, build_user_payload
from app.services.planner.filter import PreferenceFilter
from app.services.planner.orchestrator import PlannerOrchestrator
from app.settings import get_settings

logger = logging.getLogger(__name__)

FALLBACK_USER_MESSAGES = {
    "no_api_key": "AI tips unavailable (API key not configured). Showing standard plan.",
    "timeout": "AI took too long; showing standard plan.",
    "rate_limit": "AI is busy; showing standard plan.",
    "invalid_json": "AI response was invalid; showing standard plan.",
    "validation": "AI suggestions could not be applied; showing standard plan.",
    "error": "AI enhancement failed; showing standard plan.",
}


class AIPlannerService:
    def __init__(self, session: Session) -> None:
        self._session = session
        self._rule = PlannerOrchestrator(session)
        self._repo = POIRepository(session)
        self._filter = PreferenceFilter()
        self._validator = ItineraryValidator()

    def generate(self, request: ItineraryGenerateRequest) -> ItineraryResponse:
        draft = self._rule.generate(request)

        if not get_settings().groq_api_key:
            return self._fallback(draft, "no_api_key")

        try:
            return self._enrich_with_groq(request, draft)
        except GroqTimeoutError:
            return self._fallback(draft, "timeout")
        except GroqRateLimitError:
            return self._fallback(draft, "rate_limit")
        except (GroqInvalidJsonError, ItineraryValidationError) as exc:
            logger.warning("AI validation/JSON failed: %s", exc)
            return self._fallback(draft, "validation")
        except GroqClientError as exc:
            logger.warning("Groq client error: %s", exc)
            return self._fallback(draft, "error")

    def _enrich_with_groq(
        self, request: ItineraryGenerateRequest, draft: ItineraryResponse
    ) -> ItineraryResponse:
        candidates = self._repo.find_by_interests(request.interests, limit=500)
        filtered = self._filter.apply(
            candidates, interests=request.interests, budget=request.budget
        )
        context = ContextBuilder.build(request, draft, filtered)
        user_payload = build_user_payload(context)

        allowed_ids = set(context["allowed_poi_ids"])
        required_ids = {s.poi_id for s in draft.stops}
        client = GroqClient()
        try:
            result = client.complete_json(SYSTEM_PROMPT, user_payload)
        except GroqInvalidJsonError:
            result = client.complete_json(
                SYSTEM_PROMPT, user_payload, retry_suffix=JSON_RETRY_SUFFIX
            )

        try:
            notes = self._validator.extract_notes(
                result.data,
                allowed_ids=allowed_ids,
                required_ids=required_ids,
            )
        except ItineraryValidationError:
            result = client.complete_json(
                SYSTEM_PROMPT, user_payload, retry_suffix=JSON_RETRY_SUFFIX
            )
            notes = self._validator.extract_notes(
                result.data,
                allowed_ids=allowed_ids,
                required_ids=required_ids,
            )

        return self._merge_notes(draft, notes, ai_status="success")

    def _merge_notes(
        self,
        draft: ItineraryResponse,
        notes: dict,
        *,
        ai_status: str,
        fallback_reason: Optional[str] = None,
        extra_warnings: Optional[List[str]] = None,
    ) -> ItineraryResponse:
        warnings = list(draft.meta.warnings)
        if extra_warnings:
            warnings.extend(extra_warnings)

        stops: List[ItineraryStop] = []
        for stop in draft.stops:
            stops.append(
                stop.model_copy(update={"notes": notes.get(stop.poi_id, stop.notes)})
            )

        meta = draft.meta.model_copy(
            update={
                "planner_mode": "ai",
                "ai_status": ai_status,
                "fallback_reason": fallback_reason,
                "warnings": warnings,
            }
        )

        return ItineraryResponse(meta=meta, stops=stops, summary=draft.summary)

    def _fallback(self, draft: ItineraryResponse, reason: str) -> ItineraryResponse:
        message = FALLBACK_USER_MESSAGES.get(reason, FALLBACK_USER_MESSAGES["error"])
        warnings = list(draft.meta.warnings)
        if message not in warnings:
            warnings.append(message)

        meta: ItineraryMeta = draft.meta.model_copy(
            update={
                "planner_mode": "ai",
                "ai_status": "fallback",
                "fallback_reason": reason,
                "warnings": warnings,
            }
        )
        return ItineraryResponse(meta=meta, stops=draft.stops, summary=draft.summary)
