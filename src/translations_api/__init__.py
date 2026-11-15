"""Translations API - Python client for multi-language translation management."""

__version__ = "1.0.0"

from .client import TranslationClient
from .exceptions import (
    ClientException,
    RateLimitException,
    NetworkException,
    ValidationException,
    AuthenticationException,
    QuotaExceededException,
)
from .types import (
    TranslationResult,
    BatchResult,
    ExistsResult,
    UsageStats,
    DictionaryResult,
    UploadResult,
    UserString,
    PaginatedStrings,
    UserStats,
    UploadTextResult,
    UploadTextRequest,
)

__all__ = [
    "TranslationClient",
    "ClientException",
    "RateLimitException",
    "NetworkException",
    "ValidationException",
    "AuthenticationException",
    "QuotaExceededException",
    "TranslationResult",
    "BatchResult",
    "ExistsResult",
    "UsageStats",
    "DictionaryResult",
    "UploadResult",
    "UserString",
    "PaginatedStrings",
    "UserStats",
    "UploadTextResult",
    "UploadTextRequest",
]
