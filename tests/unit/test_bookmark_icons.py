from pathlib import Path

import pytest
import yaml

from app import create_app


def _write_config(tmpdir, data):
    path = Path(tmpdir) / "config.yaml"
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return str(path)


def _render(tmpdir, group):
    data = {"bookmark_groups": [group]}
    app = create_app(config_path=_write_config(tmpdir, data))
    resp = app.test_client().get("/")
    assert resp.status_code == 200
    return resp.get_data(as_text=True)


@pytest.fixture
def group():
    return {
        "name": "Media",
        "bookmarks": [
            {"label": "YouTube", "url": "https://youtube.com"},
        ],
    }


# --- T004: a bookmark with no icon renders a monogram, no <img> -------------


def test_bookmark_without_icon_renders_monogram(tmpdir, group):
    html = _render(tmpdir, group)
    assert "YouTube" in html
    assert "<img" not in html
    # The fallback is a circle with the first letter of the label.
    assert '<span class="bookmark-monogram">Y</span>' in html


# --- T005: a short-word (non-URL) icon renders a monogram, no <img> ----------


def test_bookmark_with_short_word_icon_renders_monogram(tmpdir, group):
    group["bookmarks"][0]["icon"] = "youtube"
    html = _render(tmpdir, group)
    assert "YouTube" in html
    assert 'src="youtube"' not in html
    assert "<img" not in html
    assert '<span class="bookmark-monogram">Y</span>' in html


# --- T006: an unsafe icon value is never emitted as an <img src> -------------


def test_unsafe_icon_value_not_rendered_as_src(tmpdir, group):
    group["bookmarks"][0]["icon"] = "javascript:alert(1)"
    html = _render(tmpdir, group)
    assert 'src="javascript:' not in html
    assert "<img" not in html
    assert '<span class="bookmark-monogram">Y</span>' in html


# --- T007: label escaped and link still opens in a new tab -------------------


def test_bookmark_label_is_html_escaped(tmpdir):
    group = {
        "name": "Media",
        "bookmarks": [{"label": "<script>alert('x')</script>", "url": "https://x.com"}],
    }
    html = _render(tmpdir, group)
    assert "<script>alert('x')</script>" not in html
    assert "&lt;script&gt;" in html


def test_bookmark_link_opens_in_new_tab(tmpdir, group):
    html = _render(tmpdir, group)
    assert 'target="_blank"' in html
    assert "noopener" in html
