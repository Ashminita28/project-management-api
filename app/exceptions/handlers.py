"""Global FastAPI exception handlers."""

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config import logger
from app.exceptions.domain import AppError


async def request_validation_handler(request: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, RequestValidationError)
    """Handle Pydantic request validation errors (422).

    Args:
        request: The FastAPI request.
        exc: The validation error exception.

    Returns:
        JSONResponse with 422 status and validation details.
    """
    logger.warning(
        f"Validation error on {request.method} {request.url.path}: {exc.errors()}"
    )
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "validation_error",
                "message": "Validation error",
                "details": exc.errors(),
            },
            "path": request.url.path,
        },
    )


async def http_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, StarletteHTTPException)
    """Handle FastAPI/Starlette HTTPException.

    Args:
        request: The FastAPI request.
        exc: The HTTP exception.

    Returns:
        JSONResponse with exception status and detail.
    """
    status_code = exc.status_code
    detail = exc.detail
    logger.warning(
        f"HTTP {status_code} on {request.method} {request.url.path}: {detail}"
    )
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": "http_error",
                "message": detail,
            },
            "path": request.url.path,
        },
    )


async def app_error_handler(request: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, AppError)
    """Handle domain AppError and subclasses.

    Args:
        request: The FastAPI request.
        exc: The domain AppError instance.

    Returns:
        JSONResponse with status_code and content from exc.to_response_content().
    """
    logger.warning(
        f"AppError ({exc.code}) on {request.method} {request.url.path}: {exc.message}"
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.response(request.url.path),
    )


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch-all for unhandled exceptions; log and return safe 500 response.

    Args:
        request: The FastAPI request.
        exc: The unhandled exception.

    Returns:
        JSONResponse with 500 status and generic error message.
    """
    logger.error(
        f"Unhandled exception on {request.method} {request.url.path}: {str(exc)}",
        exc_info=True,
    )
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "internal_server_error",
                "message": "Internal Server Error",
            },
            "path": request.url.path,
        },
    )
