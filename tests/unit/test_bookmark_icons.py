from pathlib import Path

import pytest
import yaml

from app import create_app
from tests.soup_utils import parse


def _write_config(tmpdir, data):
    path = Path(tmpdir) / "config.yaml"
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return str(path)


def _render(tmpdir, group):
    data = {"bookmark_groups": [group]}
    app = create_app(config_path=_write_config(tmpdir, data))
    resp = app.test_client().get("/")
    assert resp.status_code == 200
    return parse(resp.get_data(as_text=True))


def _bookmark_links(soup):
    return soup.select("a.bookmark-link")


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
    soup = _render(tmpdir, group)
    link = _bookmark_links(soup)[0]
    assert link.select_one("span.bookmark-label").get_text() == "YouTube"
    assert soup.find("img") is None
    # The fallback is a circle with the first letter of the label.
    monogram = link.select_one("span.bookmark-monogram")
    assert monogram is not None
    assert monogram.get_text() == "Y"


# --- T005: a short-word (non-URL) icon renders a monogram, no <img> ----------


def test_bookmark_with_short_word_icon_renders_monogram(tmpdir, group):
    group["bookmarks"][0]["icon"] = "youtube"
    soup = _render(tmpdir, group)
    link = _bookmark_links(soup)[0]
    assert link.select_one("span.bookmark-label").get_text() == "YouTube"
    assert soup.find("img") is None
    assert "youtube" not in (img.get("src") for img in soup.find_all("img"))
    monogram = link.select_one("span.bookmark-monogram")
    assert monogram is not None
    assert monogram.get_text() == "Y"


# --- T006: an unsafe icon value is never emitted as an <img src> -------------


def test_unsafe_icon_value_not_rendered_as_src(tmpdir, group):
    group["bookmarks"][0]["icon"] = "javascript:alert(1)"
    soup = _render(tmpdir, group)
    link = _bookmark_links(soup)[0]
    assert soup.find("img") is None
    assert not any(
        (img.get("src") or "").startswith("javascript:") for img in soup.find_all("img")
    )
    monogram = link.select_one("span.bookmark-monogram")
    assert monogram is not None
    assert monogram.get_text() == "Y"


# --- T007: label escaped and link still opens in a new tab -------------------


def test_bookmark_label_is_html_escaped(tmpdir):
    group = {
        "name": "Media",
        "bookmarks": [{"label": "<script>alert('x')</script>", "url": "https://x.com"}],
    }
    html = _render(tmpdir, group)
    assert "<script>alert('x')</script>" not in str(html)
    link = _bookmark_links(html)[0]
    label = link.select_one("span.bookmark-label")
    assert label.get_text() == "<script>alert('x')</script>"


def test_bookmark_link_opens_in_new_tab(tmpdir, group):
    soup = _render(tmpdir, group)
    link = _bookmark_links(soup)[0]
    assert link.get("target") == "_blank"
    assert link.get("rel") == ["noopener", "noreferrer"]
