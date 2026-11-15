# Translations API Python SDK

Python client for the Translations API - Multi-language translation management with DeepL integration.

## Features

- **3-tier translation lookup**: User Custom Pool → Common Library → DeepL auto-translation
- **SHA256 hash-based O(1) string lookup** for efficient translation retrieval
- **Batch translation** for multiple texts and languages
- **Dictionary lookups** for complete language modules
- **User string management** with pagination support
- **Usage statistics** and quota monitoring
- **File upload** for bulk translation imports
- **Type-safe** with full type hints
- **Context manager support** for automatic resource cleanup

## Installation

```bash
pip install translations-api
```

Or install from source:

```bash
git clone https://github.com/translationsapi/sdk-python.git
cd sdk-python
pip install -e .
```

## Quick Start

```python
from translations_api import TranslationClient

# Initialize the client
client = TranslationClient(api_key="your-api-key-here")

# Using context manager for automatic cleanup
with client:
    # Translate a single text
    translation = client.translate("Hello, world!", "de")
    print(translation)  # "Hallo, Welt!"

    # Check if a string exists
    exists = client.exists("Hello, world!")
    print(exists)  # True or False

    # Translate or add if it doesn't exist
    translation = client.translate_or_add("Welcome", "fr", use_deepl=True)
    print(translation)
```

## Usage

### Basic Translation

```python
from translations_api import TranslationClient, ClientException

client = TranslationClient(api_key="your-api-key-here")

try:
    # Translate to German
    translation = client.translate("Hello, world!", "de")
    print(translation)
except ClientException as e:
    print(f"Error: {e}")
```

### Batch Translation

```python
# Translate multiple texts to multiple languages
batch_result = client.batch(
    texts=["Hello", "Goodbye", "Thank you"],
    languages=["de", "fr", "es"],
    use_deepl=False
)

for result in batch_result.results:
    print(f"{result.source} -> {result.language}: {result.translation}")
```

### Dictionary Lookup

```python
# Get complete dictionary for a language
dictionary = client.dictionary("de", module="yemchain")
print(f"Total translations: {dictionary.total}")

# Access translations
for source, translation in dictionary.translations.items():
    print(f"{source} -> {translation}")
```

### User String Management

```python
# Get user's stored strings with pagination
strings = client.get_my_strings(page=1, per_page=10)
print(f"Total strings: {strings.total}")

for user_string in strings.data:
    print(f"ID: {user_string.id}, Text: {user_string.text}")
```

### Upload Strings

```python
# Upload text strings
upload_result = client.upload_strings(
    strings=["New string 1", "New string 2"],
    auto_translate=False
)

print(f"Added: {upload_result.strings_added}")
print(f"Updated: {upload_result.strings_updated}")
print(f"Skipped: {upload_result.strings_skipped}")
```

### Upload Files

```python
# Upload a translation file
upload_result = client.upload_file("translations.txt", format="txt")
print(f"Upload: {upload_result.message}")
```

### Usage Statistics

```python
# Get usage statistics
usage = client.usage()
print(f"API calls: {usage.usage['api_calls']}")
print(f"Remaining: {usage.limits['api_calls_remaining']}")
print(f"Plan: {usage.plan['display_name']}")
```

### Error Handling

```python
from translations_api import (
    TranslationClient,
    ClientException,
    RateLimitException,
    AuthenticationException,
    QuotaExceededException,
)

client = TranslationClient(api_key="your-api-key-here")

try:
    translation = client.translate("Hello", "de")
except RateLimitException as e:
    print(f"Rate limit exceeded. Remaining: {e.get_remaining()}")
except AuthenticationException:
    print("Invalid API key")
except QuotaExceededException:
    print("Quota exceeded. Please upgrade your plan")
except ClientException as e:
    print(f"Error: {e}")
```

### Configuration

```python
client = TranslationClient(
    api_key="your-api-key-here",
    api_base_url="https://translationsapi.com/api/v1",
    timeout=30
)

# Or configure after initialization
client.set_api_base_url("https://custom-api.com/api/v1")
client.set_timeout(60)
```

### Context Manager

```python
# Using context manager for automatic cleanup
with TranslationClient(api_key="your-api-key-here") as client:
    translation = client.translate("Hello", "de")
    print(translation)

# Client is automatically closed
```

## API Reference

### TranslationClient

#### Constructor

```python
TranslationClient(
    api_key: str,
    api_base_url: str = "https://translationsapi.com/api/v1",
    timeout: int = 30
)
```

#### Methods

- `translate(text: str, language: str, use_deepl: bool = False) -> str`
  - Translate a single text

- `exists(text: str) -> bool`
  - Check if string exists in user's translation pool

- `translate_or_add(text: str, language: str, use_deepl: bool = True) -> str`
  - Translate text or add it if it doesn't exist

- `batch(texts: List[str], languages: List[str], use_deepl: bool = False) -> BatchResult`
  - Batch translate multiple texts

- `dictionary(language: str, module: Optional[str] = None) -> DictionaryResult`
  - Get dictionary of translations for a language

- `upload_file(file_path: str, format: str = "txt") -> UploadResult`
  - Upload a translation file

- `upload_strings(strings: List[str], auto_translate: bool = False) -> UploadTextResult`
  - Upload text strings

- `get_my_strings(page: int = 1, per_page: int = 100) -> PaginatedStrings`
  - Get user's stored strings

- `usage() -> UsageStats`
  - Get usage statistics

- `get_last_response() -> Optional[Dict[str, Any]]`
  - Get the last API response

- `get_last_status_code() -> Optional[int]`
  - Get the last HTTP status code

- `set_api_base_url(api_base_url: str) -> TranslationClient`
  - Set the API base URL

- `set_timeout(timeout: int) -> TranslationClient`
  - Set the request timeout

- `close()`
  - Close the HTTP client

### Exceptions

- `ClientException` - Base exception for client errors
- `RateLimitException` - Raised when rate limit is exceeded
- `NetworkException` - Raised for network-related errors
- `ValidationException` - Raised for validation errors
- `AuthenticationException` - Raised for authentication errors
- `QuotaExceededException` - Raised when quota is exceeded

### Types

- `TranslationResult` - Translation result from translate endpoint
- `BatchResult` - Batch translation result
- `ExistsResult` - Result from exists endpoint
- `UsageStats` - Usage statistics from usage endpoint
- `DictionaryResult` - Dictionary lookup result
- `UploadResult` - File upload result
- `UserString` - User's stored string
- `PaginatedStrings` - Paginated list of user strings
- `UserStats` - User statistics
- `UploadTextResult` - Text strings upload result
- `UploadTextRequest` - Request for uploading text strings

## Requirements

- Python 3.8+
- httpx 0.24.0+

## License

MIT License - see LICENSE file for details.

## Support

- Documentation: https://docs.translationsapi.com
- GitHub Issues: https://github.com/translationsapi/sdk-python/issues
- Email: support@translationsapi.com