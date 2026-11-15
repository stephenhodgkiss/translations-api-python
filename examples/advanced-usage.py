"""Advanced usage example for the Translations API Python SDK."""

import os
from translations_api import (
    TranslationClient,
    ClientException,
    RateLimitException,
    AuthenticationException,
    QuotaExceededException,
)

# Get API key from environment variable
api_key = os.getenv("TRANSLATIONS_API_KEY", "your-api-key-here")

# Initialize the client
client = TranslationClient(api_key=api_key)

try:
    # Configure client settings
    client.set_api_base_url("https://translationsapi.com/api/v1")
    client.set_timeout(60)

    # Translate with error handling
    try:
        translation = client.translate(
            text="Advanced features demonstration",
            language="de",
            use_deepl=True
        )
        print(f"Translation: {translation}")
    except RateLimitException as e:
        print(f"Rate limit exceeded. Remaining: {e.get_remaining()}, Reset: {e.get_reset()}")
    except AuthenticationException:
        print("Invalid API key")
    except QuotaExceededException:
        print("Quota exceeded. Please upgrade your plan")
    except ClientException as e:
        print(f"Error: {e}")

    # Batch translate with multiple languages
    texts = [
        "Create account",
        "Sign in",
        "Sign out",
        "Settings",
        "Profile"
    ]
    languages = ["de", "fr", "es", "it", "pt"]

    batch_result = client.batch(texts=texts, languages=languages, use_deepl=False)
    print(f"\nBatch translation results:")
    for result in batch_result.results:
        print(f"  {result.source} -> {result.language}: {result.translation}")

    # Get dictionary for specific module
    yemchain_dict = client.dictionary("de", module="yemchain")
    print(f"\nYemChain dictionary (German): {yemchain_dict.total} translations")

    # Get common dictionary
    common_dict = client.dictionary("fr", module="common")
    print(f"Common dictionary (French): {common_dict.total} translations")

    # Get detailed usage statistics
    usage = client.usage()
    print(f"\nUsage Statistics:")
    print(f"  Plan: {usage.plan.get('display_name')}")
    print(f"  Status: {usage.subscription.get('status')}")
    print(f"  API calls: {usage.usage.get('api_calls')} / {usage.plan.get('api_calls_limit')}")
    print(f"  DeepL calls: {usage.usage.get('deepl_calls')} / {usage.plan.get('deepl_calls_limit')}")
    print(f"  Custom strings: {usage.usage.get('custom_strings')} / {usage.plan.get('custom_strings_limit')}")
    print(f"  Uploads: {usage.usage.get('uploads_this_month')} / {usage.plan.get('uploads_per_month')}")

    # Get all user strings with pagination
    print(f"\nUser Strings:")
    page = 1
    per_page = 50

    while True:
        strings = client.get_my_strings(page=page, per_page=per_page)
        print(f"  Page {page}/{strings.total_pages}: {len(strings.data)} strings")

        for user_string in strings.data:
            print(f"    - {user_string.text[:50]}... (ID: {user_string.id}, Translations: {user_string.translations_count})")

        if page >= strings.total_pages:
            break
        page += 1

    # Upload a file
    # upload_result = client.upload_file("translations.txt", format="txt")
    # print(f"\nFile upload: {upload_result.message}")
    # print(f"  Added: {upload_result.strings_added}")
    # print(f"  Updated: {upload_result.strings_updated}")
    # print(f"  Skipped: {upload_result.strings_skipped}")

    # Upload strings with auto-translation
    new_strings = [
        "New feature announcement",
        "Product description",
        "Terms of service"
    ]
    upload_result = client.upload_strings(new_strings, auto_translate=True)
    print(f"\nString upload: {upload_result.message}")
    print(f"  Added: {upload_result.strings_added}")
    print(f"  Updated: {upload_result.strings_updated}")
    print(f"  Skipped: {upload_result.strings_skipped}")

    # Check last response and status code
    print(f"\nLast status code: {client.get_last_status_code()}")
    last_response = client.get_last_response()
    if last_response:
        print(f"Last response keys: {list(last_response.keys())}")

except ClientException as e:
    print(f"Fatal error: {e}")
finally:
    # Always close the client
    client.close()