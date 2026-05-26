"""Groq chat completions adapter (JSON mode)."""

import json
import logging
from dataclasses import dataclass
from typing import Any, Dict, Optional

from groq import Groq

from app.config import GROQ_TEMPERATURE
from app.settings import get_settings

logger = logging.getLogger(__name__)


class GroqClientError(Exception):
    """Base error for Groq client failures."""


class GroqTimeoutError(GroqClientError):
    pass


class GroqRateLimitError(GroqClientError):
    pass


class GroqInvalidJsonError(GroqClientError):
    pass


@dataclass
class GroqCompletionResult:
    data: Dict[str, Any]
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None


class GroqClient:
    def __init__(self) -> None:
        settings = get_settings()
        if not settings.groq_api_key:
            raise GroqClientError("GROQ_API_KEY is not configured")
        self._settings = settings
        self._client = Groq(api_key=settings.groq_api_key)

    def complete_json(
        self,
        system_prompt: str,
        user_payload: str,
        *,
        retry_suffix: Optional[str] = None,
    ) -> GroqCompletionResult:
        user_content = user_payload
        if retry_suffix:
            user_content = user_payload + retry_suffix

        try:
            response = self._client.chat.completions.create(
                model=self._settings.groq_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content},
                ],
                response_format={"type": "json_object"},
                temperature=GROQ_TEMPERATURE,
                timeout=self._settings.groq_timeout_sec,
            )
        except Exception as exc:  # groq SDK raises various types
            msg = str(exc).lower()
            if "timeout" in msg or "timed out" in msg:
                raise GroqTimeoutError(str(exc)) from exc
            if "429" in msg or "rate" in msg:
                raise GroqRateLimitError(str(exc)) from exc
            raise GroqClientError(str(exc)) from exc

        content = response.choices[0].message.content or ""
        usage = getattr(response, "usage", None)
        prompt_tokens = getattr(usage, "prompt_tokens", None) if usage else None
        completion_tokens = getattr(usage, "completion_tokens", None) if usage else None
        total_tokens = getattr(usage, "total_tokens", None) if usage else None

        if prompt_tokens is not None:
            logger.info(
                "Groq completion tokens prompt=%s completion=%s total=%s",
                prompt_tokens,
                completion_tokens,
                total_tokens,
            )

        try:
            data = json.loads(content)
        except json.JSONDecodeError as exc:
            raise GroqInvalidJsonError(f"Invalid JSON from Groq: {content[:200]}") from exc

        if not isinstance(data, dict):
            raise GroqInvalidJsonError("Groq response root must be a JSON object")

        return GroqCompletionResult(
            data=data,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
        )
