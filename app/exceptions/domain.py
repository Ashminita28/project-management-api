"""Custom exception classes"""


class AppError(Exception):
    """Base application error with HTTP status and error code."""

    status_code: int = 500
    code: str = "internal_error"

    def __init__(self, message: str) -> None:
        """Initialize AppError with a message.

        Args:
            message: Error message.
        """
        super().__init__(message)
        self.message = message

    def response(self, path: str) -> dict:
        """Build the JSON body for the error.

        Args:
            path: Request path for the response.

        Returns:
            Dict with error code, message, and path.
        """
        return {
            "error": {"code": self.code, "message": self.message},
            "path": path,
        }


class UnauthorizedError(AppError):
    """User Unauthorized to access resource."""

    status_code = 401
    code = "unauthorized"


class NotFoundError(AppError):
    """Resource not found."""

    status_code = 404
    code = "not_found"


class ConflictError(AppError):
    """Resource already exists."""

    status_code = 409
    code = "conflict"


class ValidationError(AppError):
    """validation failed."""

    status_code = 422
    code = "validation_error"


class InternalError(AppError):
    """Unexpected internal error."""

    status_code = 500
    code = "internal_error"
