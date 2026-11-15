import html
from urllib.parse import ParseResult, urlparse


def validate_url(value: object) -> bool:
    """Return True if value is a valid absolute http/https URL."""
    if not value or not isinstance(value, str):
        return False
    try:
        parsed: ParseResult = urlparse(value.strip())
    except ValueError, TypeError:
        return False
    if parsed.scheme not in ("http", "https"):
        return False
    return bool(parsed.netloc)


def escape_html(value) -> str | None:
    """HTML-escape a renderable string. Returns None for falsy/reserved values."""
    if value is None:
        return None
    return html.escape(str(value), quote=True)
