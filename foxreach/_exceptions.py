from __future__ import annotations

from typing import Any, Optional


class FoxReachError(Exception):
    """Base exception for all FoxReach SDK errors."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_body: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body


class AuthenticationError(FoxReachError):
    """Raised on 401 Unauthorized responses."""


class PermissionError(FoxReachError):
    """Raised on 403 Forbidden responses."""


class NotFoundError(FoxReachError):
    """Raised on 404 Not Found responses."""


class BadRequestError(FoxReachError):
    """Raised on 400 Bad Request responses."""


class ValidationError(FoxReachError):
    """Raised on 422 Unprocessable Entity responses."""


class RateLimitError(FoxReachError):
    """Raised on 429 Too Many Requests after retries are exhausted."""

    def __init__(
        self,
        message: str,
        retry_after: Optional[float] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(message, **kwargs)
        self.retry_after = retry_after


class ServerError(FoxReachError):
    """Raised on 5xx server errors."""


class ConnectionError(FoxReachError):
    """Raised on network / connection errors."""
