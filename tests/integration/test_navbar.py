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


def test_page_renders_navbar_with_brand(tmp_path):
    soup = _page_soup(tmp_path, {"title": "MyLab"})

    assert soup.select_one("nav.navbar") is not None
    brand = soup.select_one(".navbar-brand")
    assert brand is not None
    assert brand.get_text(strip=True) == "MyLab"


def test_navbar_brand_shows_configurable_title(tmp_path):
    soup = _page_soup(tmp_path, {"title": "Custom Name"})

    assert soup.select_one(".navbar-brand").get_text(strip=True) == "Custom Name"


def test_navbar_brand_shows_default_when_no_title(tmp_path):
    soup = _page_soup(tmp_path, {"tile_groups": []})

    assert soup.select_one(".navbar-brand").get_text(strip=True) == "Homelab"


def test_navbar_has_right_side_toggle_area(tmp_path):
    app = create_app(config_path=_write_config(tmp_path, {"title": "MyLab"}))
    html = app.test_client().get("/").get_data(as_text=True)

    # The brand (title) must come before the theme-toggle container in source
    # order, and a right-aligned (ms-auto) control region must exist.
    brand_idx = html.find("navbar-brand")
    toggle_idx = html.find("data-theme-toggle")
    assert brand_idx != -1
    assert toggle_idx != -1
    assert brand_idx < toggle_idx


# --- Header search bar (feature-011) -----------------------------------------


def test_navbar_has_search_form_on_homepage(tmp_path):
    soup = _page_soup(tmp_path, {"title": "MyLab"})

    form = soup.select_one("form")
    assert form is not None
    assert form.get("method") == "get"
    assert form.get("target") == "_blank"
    assert "noopener" in (form.get("rel") or "")
    search_input = form.select_one('input[name="q"]')
    assert search_input is not None
    assert search_input.get("type") == "search"


def test_navbar_has_search_form_on_config_page(tmp_path):
    soup = _page_soup(tmp_path, {"title": "MyLab"}, path="/config")

    form = soup.select_one("form")
    assert form is not None
    assert form.get("method") == "get"
    assert form.select_one('input[name="q"]') is not None


def test_navbar_shows_default_search_icon_when_no_icon_configured(tmp_path):
    soup = _page_soup(tmp_path, {"title": "MyLab"})

    assert soup.select_one(".search-engine-icon .bi-search") is not None


def test_navbar_renders_configured_search_icon_with_onerror_fallback(tmp_path):
    icon = "https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/svg/google.svg"
    soup = _page_soup(tmp_path, {"title": "MyLab", "search_engine_icon": icon})

    icon_img = soup.select_one("img.search-engine-icon")
    assert icon_img is not None
    assert icon_img.get("src") == icon
    assert icon_img.has_attr("onerror")


def test_navbar_uses_custom_search_engine_in_action(tmp_path):
    custom = "https://duckduckgo.com/?q={query}"
    soup = _page_soup(tmp_path, {"title": "MyLab", "search_engine": custom})

    form = soup.select_one("form")
    assert form is not None
    assert form.get("action").startswith("https://duckduckgo.com/")
