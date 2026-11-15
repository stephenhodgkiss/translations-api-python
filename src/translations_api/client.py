"""Translations API Client."""

import httpx
from typing import Optional, List, Dict, Any

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


class TranslationClient:
    """
    Translations API Client.

    Args:
        api_key: Your API key from the customer portal
        api_base_url: API base URL (default: https://translationsapi.com/api/v1)
        timeout: Request timeout in seconds (default: 30)
    """

    def __init__(
        self,
        api_key: str,
        api_base_url: str = "https://translationsapi.com/api/v1",
        timeout: int = 30,
    ):
        self.api_key = api_key
        self.api_base_url = api_base_url.rstrip("/")
        self.timeout = timeout
        self._client = httpx.Client(timeout=timeout)
        self._last_response: Optional[Dict[str, Any]] = None
        self._last_status_code: Optional[int] = None

    def translate(
        self, text: str, language: str, use_deepl: bool = False
    ) -> str:
        """
        Translate text.

        Args:
            text: Source text to translate
            language: Target language code (e.g., 'de', 'fr', 'es')
            use_deepl: Use DeepL auto-translation if not found (default: False)

        Returns:
            Translated text

        Raises:
            ClientException: On API errors
            RateLimitException: When rate limit is exceeded
        """
        return self._request(
            "POST",
            "/translate",
            {"text": text, "language": language, "auto_translate": use_deepl},
        )["data"]["translated"]

    def exists(self, text: str) -> bool:
        """
        Check if string exists in user's translation pool.

        Args:
            text: Source text to check

        Returns:
            True if string exists, False otherwise

        Raises:
            ClientException: On API errors
        """
        result = self._request("POST", "/exists", {"text": text})
        return result.get("data", {}).get("exists", False)

    def translate_or_add(
        self, text: str, language: str, use_deepl: bool = True
    ) -> str:
        """
        Translate text or add it if it doesn't exist.

        Args:
            text: Source text to translate
            language: Target language code (e.g., 'de', 'fr', 'es')
            use_deepl: Use DeepL auto-translation if not found (default: True)

        Returns:
            Translated text

        Raises:
            ClientException: On API errors
            RateLimitException: When rate limit is exceeded
        """
        return self._request(
            "POST",
            "/translate",
            {"text": text, "language": language, "auto_translate": use_deepl},
        )["data"]["translated"]

    def batch(
        self, texts: List[str], languages: List[str], use_deepl: bool = False
    ) -> BatchResult:
        """
        Batch translate multiple texts.

        Args:
            texts: List of source texts
            languages: List of target language codes
            use_deepl: Use DeepL auto-translation if not found (default: False)

        Returns:
            BatchResult with translation results

        Raises:
            ClientException: On API errors
            RateLimitException: When rate limit is exceeded
        """
        result = self._request(
            "POST",
            "/batch",
            {"texts": texts, "languages": languages, "auto_translate": use_deepl},
        )
        data = result.get("data", {})
        return BatchResult(
            results=[TranslationResult(**r) for r in data.get("results", [])],
            total=data.get("total_requests", 0),
        )

    def dictionary(
        self, language: str, module: Optional[str] = None
    ) -> DictionaryResult:
        """
        Get dictionary of translations for a language.

        Args:
            language: Language code (e.g., 'de', 'fr', 'es')
            module: Optional module filter (e.g., 'yemchain', 'yemfoundation')

        Returns:
            DictionaryResult with translations

        Raises:
            ClientException: On API errors
        """
        data = {"language": language}
        if module:
            data["module"] = module

        result = self._request("POST", "/dictionary", data)
        payload = result.get("data", {})
        return DictionaryResult(
            language=payload.get("language", language),
            module=payload.get("module"),
            translations=payload.get("translations", {}),
            total=payload.get("count", 0),
        )

    def upload_file(
        self, file_path: str, format: str = "txt"
    ) -> UploadResult:
        """
        Upload a translation file.

        Args:
            file_path: Path to the file to upload
            format: File format ('txt', 'csv', 'json')

        Returns:
            UploadResult with upload statistics

        Raises:
            ClientException: On API errors
            RateLimitException: When rate limit is exceeded
        """
        with open(file_path, "rb") as f:
            files = {"file": (file_path, f, "application/octet-stream")}
            data = {"format": format}
            result = self._request("POST", "/upload", data, files=files)

        payload = result.get("data", result)
        return UploadResult(
            success=True,
            message="",
            strings_added=payload.get("strings_added", 0),
            strings_updated=0,
            strings_skipped=payload.get("strings_skipped", 0),
        )

    def upload_strings(
        self, strings: List[str], auto_translate: bool = False
    ) -> UploadTextResult:
        """
        Upload text strings.

        Args:
            strings: List of text strings to upload
            auto_translate: Auto-translate uploaded strings (default: False)

        Returns:
            UploadTextResult with upload statistics

        Raises:
            ClientException: On API errors
            RateLimitException: When rate limit is exceeded
        """
        result = self._request(
            "POST",
            "/upload-text",
            {"strings": strings, "auto_translate": auto_translate},
        )
        payload = result.get("data", {})
        return UploadTextResult(
            success=True,
            message="",
            strings_added=payload.get("strings_added", 0),
            strings_updated=0,
            strings_skipped=payload.get("strings_skipped_common", 0)
            + payload.get("strings_skipped_duplicate", 0),
        )

    def get_my_strings(
        self, page: int = 1, per_page: int = 100
    ) -> PaginatedStrings:
        """
        Get user's stored strings.

        Args:
            page: Page number (default: 1)
            per_page: Items per page (default: 100)

        Returns:
            PaginatedStrings with user's strings

        Raises:
            ClientException: On API errors
        """
        result = self._request(
            "GET",
            f"/my-strings?page={page}&per_page={per_page}",
        )
        payload = result.get("data", {})
        total = payload.get("total", 0)
        return PaginatedStrings(
            data=[UserString(**s) for s in payload.get("strings", [])],
            total=total,
            page=payload.get("page", page),
            per_page=payload.get("per_page", per_page),
            total_pages=(total + per_page - 1) // per_page if per_page else 0,
        )

    def usage(self) -> UsageStats:
        """
        Get usage statistics.

        Returns:
            UsageStats with subscription, plan, usage, and limits

        Raises:
            ClientException: On API errors
        """
        result = self._request("GET", "/usage")
        payload = result.get("data", {})
        return UsageStats(
            subscription=payload.get("subscription", {}),
            plan=payload.get("plan", {}),
            usage=payload.get("usage", {}),
            limits=payload.get("limits", {}),
        )

    def get_last_response(self) -> Optional[Dict[str, Any]]:
        """
        Get the last API response.

        Returns:
            Last response data or None
        """
        return self._last_response

    def get_last_status_code(self) -> Optional[int]:
        """
        Get the last HTTP status code.

        Returns:
            Last status code or None
        """
        return self._last_status_code

    def set_api_base_url(self, api_base_url: str) -> "TranslationClient":
        """
        Set the API base URL.

        Args:
            api_base_url: New API base URL

        Returns:
            Self for method chaining
        """
        self.api_base_url = api_base_url.rstrip("/")
        return self

    def set_timeout(self, timeout: int) -> "TranslationClient":
        """
        Set the request timeout.

        Args:
            timeout: New timeout in seconds

        Returns:
            Self for method chaining
        """
        self.timeout = timeout
        self._client.timeout = timeout
        return self

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make an API request.

        Args:
            method: HTTP method ('GET', 'POST')
            endpoint: API endpoint
            data: Request data
            files: Files to upload

        Returns:
            Response data

        Raises:
            ClientException: On API errors
            RateLimitException: When rate limit is exceeded
            NetworkException: On network errors
            ValidationException: On validation errors
            AuthenticationException: On authentication errors
            QuotaExceededException: When quota is exceeded
        """
        url = f"{self.api_base_url}{endpoint}"
        headers = {"Authorization": f"Bearer {self.api_key}"}

        try:
            if method == "GET":
                response = self._client.get(url, headers=headers)
            else:
                if files:
                    response = self._client.post(url, headers=headers, data=data, files=files)
                else:
                    response = self._client.post(url, headers=headers, json=data)

            self._last_status_code = response.status_code

            if response.status_code == 401:
                raise AuthenticationException("Invalid API key")

            if response.status_code == 402:
                raise QuotaExceededException("Quota exceeded")

            if response.status_code == 429:
                raise RateLimitException(
                    "Rate limit exceeded",
                    limit=int(response.headers.get("X-RateLimit-Limit", 0)),
                    remaining=int(response.headers.get("X-RateLimit-Remaining", 0)),
                    reset=response.headers.get("X-RateLimit-Reset"),
                )

            response.raise_for_status()

            self._last_response = response.json()
            return self._last_response

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 400:
                raise ValidationException("Validation error")
            raise ClientException(f"HTTP error: {e.response.status_code}", e.response.status_code)
        except httpx.RequestError as e:
            raise NetworkException(f"Network error: {str(e)}")
        except Exception as e:
            if isinstance(e, (ClientException, RateLimitException, NetworkException, ValidationException, AuthenticationException, QuotaExceededException)):
                raise
            raise ClientException(f"Unexpected error: {str(e)}")

    def close(self):
        """Close the HTTP client."""
        if self._client:
            self._client.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
