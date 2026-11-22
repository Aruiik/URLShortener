
import re
from urllib.parse import urlparse


def is_valid_url(url: str) -> bool:
    if not isinstance(url, str):
        return False

    url = url.strip()

    if not url:
        return False

    try:
        parsed_url = urlparse(url)

        if parsed_url.scheme not in ("http", "https"):
            return False

        if not parsed_url.hostname:
            return False

        # Sprawdzenie poprawności portu
        _ = parsed_url.port

        return True

    except ValueError:
        return False


def is_valid_short_code(code: str) -> bool:
    if not isinstance(code, str):
        return False

    code = code.strip().lower()

    if not 3 <= len(code) <= 10:
        return False

    return bool(
        re.fullmatch(
            r"[a-z0-9][a-z0-9-]{1,8}[a-z0-9]",
            code
        )
    )
