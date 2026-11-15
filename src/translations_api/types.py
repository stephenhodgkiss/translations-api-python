"""Type definitions for the Translations API client."""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any


@dataclass
class TranslationResult:
    """Translation result (one entry of a batch response)."""

    text: Optional[str] = None
    language: Optional[str] = None
    translated: Optional[str] = None
    source_id: Optional[int] = None
    is_machine: bool = False


@dataclass
class BatchResult:
    """Batch translation result."""

    results: List[TranslationResult]
    total: int


@dataclass
class ExistsResult:
    """Result from exists endpoint."""

    exists: bool
    source: Optional[str] = None
    translations_count: Optional[int] = None


@dataclass
class UsageStats:
    """Usage statistics from usage endpoint."""

    subscription: Dict[str, Any]
    plan: Dict[str, Any]
    usage: Dict[str, Any]
    limits: Dict[str, Any]


@dataclass
class DictionaryResult:
    """Dictionary lookup result."""

    language: str
    module: Optional[str]
    translations: Dict[str, str]
    total: int


@dataclass
class UploadResult:
    """File upload result."""

    success: bool
    message: str
    strings_added: int
    strings_updated: int
    strings_skipped: int


@dataclass
class UserString:
    """User's stored string."""

    id: int
    text: str
    translations_count: int
    created_at: str
    updated_at: str


@dataclass
class PaginatedStrings:
    """Paginated list of user strings."""

    data: List[UserString]
    total: int
    page: int
    per_page: int
    total_pages: int


@dataclass
class UserStats:
    """User statistics."""

    total_strings: int
    total_translations: int
    languages_used: int
    modules_used: int


@dataclass
class UploadTextResult:
    """Text strings upload result."""

    success: bool
    message: str
    strings_added: int
    strings_updated: int
    strings_skipped: int


@dataclass
class UploadTextRequest:
    """Request for uploading text strings."""

    strings: List[str]
    auto_translate: bool = False
