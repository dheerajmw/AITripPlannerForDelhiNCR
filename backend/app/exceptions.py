"""Application exceptions mapped to HTTP error responses."""

from typing import Any, Dict, Optional


class AppError(Exception):
    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = 400,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(message)


class ValidationAppError(AppError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(
            code="VALIDATION_ERROR",
            message=message,
            status_code=400,
            details=details,
        )


class UnprocessablePlanError(AppError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(
            code="UNPROCESSABLE_PLAN",
            message=message,
            status_code=422,
            details=details,
        )
