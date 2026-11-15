"""Basic usage example for the Translations API Python SDK."""

from translations_api import TranslationClient, ClientException

# Initialize the client with your API key
client = TranslationClient(
    api_key="your-api-key-here",
    api_base_url="https://translationsapi.com/api/v1",
    timeout=30
)

# Using context manager for automatic cleanup
with client:
    # Translate a single text
    try:
        translation = client.translate("Hello, world!", "de")
        print(f"Translation: {translation}")
    except ClientException as e:
        print(f"Error: {e}")

    # Check if a string exists in your translation pool
    exists = client.exists("Hello, world!")
    print(f"String exists: {exists}")

    # Translate or add if it doesn't exist
    translation = client.translate_or_add("Welcome to our app", "fr", use_deepl=True)
    print(f"Translation (or added): {translation}")

    # Batch translate multiple texts
    batch_result = client.batch(
        texts=["Hello", "Goodbye", "Thank you"],
        languages=["de", "fr", "es"],
        use_deepl=False
    )
    print(f"Batch translated {batch_result.total} items")

    # Get dictionary for a language
    dictionary = client.dictionary("de", module="yemchain")
    print(f"Dictionary has {dictionary.total} translations")

    # Get usage statistics
    usage = client.usage()
    print(f"API calls used: {usage.usage.get('api_calls', 0)}")
    print(f"API calls remaining: {usage.limits.get('api_calls_remaining', 0)}")

    # Get user's stored strings
    strings = client.get_my_strings(page=1, per_page=10)
    print(f"Total strings: {strings.total}")

    # Upload text strings
    upload_result = client.upload_strings(
        strings=["New string 1", "New string 2"],
        auto_translate=False
    )
    print(f"Added {upload_result.strings_added} strings")