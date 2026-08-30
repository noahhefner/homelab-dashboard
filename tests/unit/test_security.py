from app.security import escape_html, validate_url


def test_validate_url_accepts_http():
    assert validate_url("http://example.com") is True


def test_validate_url_accepts_https():
    assert validate_url("https://example.com:32400/path") is True


def test_validate_url_rejects_ftp():
    assert validate_url("ftp://example.com") is False


def test_validate_url_rejects_javascript():
    assert validate_url("javascript:alert(1)") is False


def test_validate_url_rejects_relative():
    assert validate_url("/path/only") is False


def test_validate_url_rejects_empty():
    assert validate_url("") is False


def test_escape_html_escapes_angle_brackets():
    assert (
        escape_html("<script>alert('x')</script>")
        == "&lt;script&gt;alert(&#x27;x&#x27;)&lt;/script&gt;"
    )


def test_escape_html_escapes_quotes():
    assert (
        escape_html('"><img onerror=alert(1)>')
        == "&quot;&gt;&lt;img onerror=alert(1)&gt;"
    )


def test_escape_html_returns_none_for_none():
    assert escape_html(None) is None
