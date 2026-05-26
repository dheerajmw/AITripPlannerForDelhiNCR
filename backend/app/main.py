"""FastAPI application entrypoint."""

import json
from typing import Any, Dict, Optional

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.v1.router import api_router
from app.config import APP_VERSION
from app.db.session import init_db
from app.exceptions import AppError
from app.models.errors import ErrorBody, ErrorResponse
from app.settings import get_settings

settings = get_settings()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    version=APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


def _error_json(
    code: str,
    message: str,
    status_code: int,
    details: Optional[Dict[str, Any]] = None,
) -> JSONResponse:
    body = ErrorResponse(error=ErrorBody(code=code, message=message, details=details))
    return JSONResponse(status_code=status_code, content=json.loads(body.model_dump_json()))


@app.exception_handler(AppError)
async def app_error_handler(_request: Request, exc: AppError) -> JSONResponse:
    return _error_json(exc.code, exc.message, exc.status_code, exc.details)


def _json_safe_validation_errors(exc: RequestValidationError) -> list:
    """Pydantic error dicts may embed non-JSON-serializable ctx values."""
    return json.loads(json.dumps(exc.errors(), default=str))


@app.exception_handler(RequestValidationError)
async def validation_error_handler(
    _request: Request, exc: RequestValidationError
) -> JSONResponse:
    return _error_json(
        code="VALIDATION_ERROR",
        message="Request validation failed",
        status_code=400,
        details={"errors": _json_safe_validation_errors(exc)},
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(
    _request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    if isinstance(exc.detail, dict) and "error" in exc.detail:
        return JSONResponse(status_code=exc.status_code, content=exc.detail)
    return _error_json(
        code="HTTP_ERROR",
        message=str(exc.detail),
        status_code=exc.status_code,
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(_request: Request, _exc: Exception) -> JSONResponse:
    return _error_json(
        code="INTERNAL_ERROR",
        message="An unexpected error occurred",
        status_code=500,
    )
