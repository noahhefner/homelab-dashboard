from pathlib import Path

import yaml

from app import create_app
from tests.soup_utils import parse


def _write_config(tmpdir, data):
    path = Path(tmpdir) / "config.yaml"
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return str(path)


def _page_soup(tmp_path, data, path="/"):
    app = create_app(config_path=_write_config(tmp_path, data))
    return parse(app.test_client().get(path).get_data(as_text=True))


def _search_form(soup):
    """Return the navbar search form, identified by its 'q' input."""
    return soup.select_one('form input[name="q"]')


# --- Search bar visibility (feature-012 / US1) ------------------------------


def test_search_form_renders_by_default_on_homepage(tmp_path):
    soup = _page_soup(tmp_path, {"tile_groups": []})

    assert _search_form(soup) is not None


def test_search_form_renders_by_default_on_config_page(tmp_path):
    soup = _page_soup(tmp_path, {"tile_groups": []}, path="/config")

    assert _search_form(soup) is not None


def test_search_form_hidden_on_homepage_when_disabled(tmp_path):
    soup = _page_soup(tmp_path, {"tile_groups": [], "show_search": False})

    assert _search_form(soup) is None
    assert soup.select_one(".navbar-brand") is not None
    assert soup.select_one("[data-theme-toggle]") is not None


def test_search_form_hidden_on_config_page_when_disabled(tmp_path):
    soup = _page_soup(
        tmp_path, {"tile_groups": [], "show_search": False}, path="/config"
    )

    assert _search_form(soup) is None
    assert soup.select_one(".navbar-brand") is not None


def test_search_hidden_with_search_config_present_does_not_error(tmp_path):
    data = {
        "tile_groups": [],
        "show_search": False,
        "search_engine": "https://duckduckgo.com/?q={query}",
        "search_engine_icon": "https://example.com/icon.svg",
    }
    soup = _page_soup(tmp_path, data)

    assert _search_form(soup) is None


# --- Bookmarks visibility (feature-012 / US2) -------------------------------


def test_bookmarks_rendered_by_default(tmp_path):
    data = {
        "bookmark_groups": [
            {"name": "Media", "bookmarks": [{"label": "Y", "url": "https://y.com"}]}
        ]
    }
    soup = _page_soup(tmp_path, data)

    assert soup.select_one("aside[aria-label='Bookmarks']") is not None


def test_bookmarks_hidden_when_disabled(tmp_path):
    data = {
        "bookmark_groups": [
            {"name": "Media", "bookmarks": [{"label": "Y", "url": "https://y.com"}]}
        ],
        "show_bookmarks": False,
    }
    soup = _page_soup(tmp_path, data)

    assert soup.select_one("aside[aria-label='Bookmarks']") is None


def test_tiles_full_width_when_bookmarks_disabled(tmp_path):
    data = {
        "tile_groups": [
            {"name": "G", "tiles": [{"name": "A", "url": "https://a.lan"}]}
        ],
        "show_bookmarks": False,
    }
    soup = _page_soup(tmp_path, data)

    tiles = soup.select_one("section[aria-label='Tiles']")
    assert tiles is not None
    assert "col-12" in tiles.get("class")
    assert "col-lg-9" not in tiles.get("class")


def test_tiles_side_by_side_with_bookmarks_by_default(tmp_path):
    data = {"tile_groups": [{"name": "G", "tiles": []}]}
    soup = _page_soup(tmp_path, data)

    tiles = soup.select_one("section[aria-label='Tiles']")
    assert "col-lg-9" in tiles.get("class")


# --- Combined + independence (feature-012 / US3) ----------------------------


def test_both_hidden_renders_minimal_dashboard(tmp_path):
    data = {
        "tile_groups": [
            {"name": "G", "tiles": [{"name": "A", "url": "https://a.lan"}]}
        ],
        "show_search": False,
        "show_bookmarks": False,
    }
    app = create_app(config_path=_write_config(tmp_path, data))
    response = app.test_client().get("/")

    assert response.status_code == 200
    soup = parse(response.get_data(as_text=True))
    assert soup.select_one(".navbar-brand") is not None
    assert soup.select_one("section[aria-label='Tiles']") is not None
    assert _search_form(soup) is None
    assert soup.select_one("aside[aria-label='Bookmarks']") is None


def test_search_hidden_keeps_bookmarks(tmp_path):
    data = {
        "bookmark_groups": [
            {"name": "Media", "bookmarks": [{"label": "Y", "url": "https://y.com"}]}
        ],
        "show_search": False,
    }
    soup = _page_soup(tmp_path, data)

    assert _search_form(soup) is None
    assert soup.select_one("aside[aria-label='Bookmarks']") is not None


def test_bookmarks_hidden_keeps_search(tmp_path):
    data = {
        "tile_groups": [{"name": "G", "tiles": []}],
        "show_bookmarks": False,
    }
    soup = _page_soup(tmp_path, data)

    assert _search_form(soup) is not None
    assert soup.select_one("aside[aria-label='Bookmarks']") is None
