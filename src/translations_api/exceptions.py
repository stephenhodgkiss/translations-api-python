"""Exception classes for the Translations API client."""


class ClientException(Exception):
    """Base exception for client errors."""

    def __init__(self, message: str, status_code: int = None):
        self.status_code = status_code
        super().__init__(message)


class RateLimitException(ClientException):
    """Raised when rate limit is exceeded."""

    def __init__(
        self,
        message: str,
        limit: int = None,
        remaining: int = None,
        reset: str = None,
    ):
        super().__init__(message, status_code=429)
        self.limit = limit
        self.remaining = remaining
        self.reset = reset

    def get_limit(self) -> int:
        """Get the rate limit."""
        return self.limit

    def get_remaining(self) -> int:
        """Get the remaining requests."""
        return self.remaining

    def get_reset(self) -> str:
        """Get the reset time."""
        return self.reset


class NetworkException(ClientException):
    """Raised for network-related errors."""

    def __init__(self, message: str):
        super().__init__(message)


class ValidationException(ClientException):
    """Raised for validation errors."""

    def __init__(self, message: str):
        super().__init__(message, status_code=400)


class AuthenticationException(ClientException):
    """Raised for authentication errors."""

    def __init__(self, message: str):
        super().__init__(message, status_code=401)


class QuotaExceededException(ClientException):
    """Raised when quota is exceeded."""

    def __init__(self, message: str):
        super().__init__(message, status_code=402)
