import html
from urllib.parse import urlparse


def validate_url(url):
    """Return True if url is a valid absolute http/https URL."""
    if not url or not isinstance(url, str):
        return False
    try:
        parsed = urlparse(url.strip())
    except (ValueError, TypeError):
        return False
    if parsed.scheme not in ("http", "https"):
        return False
    if not parsed.netloc:
        return False
    return True


def escape_html(value):
    """HTML-escape a renderable string. Returns None for falsy/reserved values."""
    if value is None:
        return None
    return html.escape(str(value), quote=True)
