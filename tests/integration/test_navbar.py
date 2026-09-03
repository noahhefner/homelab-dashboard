from pathlib import Path

import yaml

from app import create_app


def _write_config(tmpdir, data):
    path = Path(tmpdir) / "config.yaml"
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return str(path)


def test_page_renders_navbar_with_brand(tmp_path):
    app = create_app(config_path=_write_config(tmp_path, {"title": "MyLab"}))
    html = app.test_client().get("/").get_data(as_text=True)

    assert 'class="navbar' in html
    assert 'class="navbar-brand' in html
    assert "MyLab" in html


def test_navbar_brand_shows_configurable_title(tmp_path):
    app = create_app(config_path=_write_config(tmp_path, {"title": "Custom Name"}))
    html = app.test_client().get("/").get_data(as_text=True)

    assert "Custom Name" in html


def test_navbar_brand_shows_default_when_no_title(tmp_path):
    app = create_app(config_path=_write_config(tmp_path, {"tiles": []}))
    html = app.test_client().get("/").get_data(as_text=True)

    assert ">Homelab<" in html


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
    app = create_app(config_path=_write_config(tmp_path, {"title": "MyLab"}))
    html = app.test_client().get("/").get_data(as_text=True)

    assert 'method="GET"' in html
    assert 'target="_blank"' in html
    assert 'rel="noopener"' in html
    assert 'name="q"' in html
    assert 'type="search"' in html


def test_navbar_has_search_form_on_config_page(tmp_path):
    app = create_app(config_path=_write_config(tmp_path, {"title": "MyLab"}))
    html = app.test_client().get("/config").get_data(as_text=True)

    assert 'method="GET"' in html
    assert 'name="q"' in html


def test_navbar_shows_default_search_icon_when_no_icon_configured(tmp_path):
    app = create_app(config_path=_write_config(tmp_path, {"title": "MyLab"}))
    html = app.test_client().get("/").get_data(as_text=True)

    assert 'bi-search' in html


def test_navbar_renders_configured_search_icon_with_onerror_fallback(tmp_path):
    icon = "https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/svg/google.svg"
    app = create_app(
        config_path=_write_config(
            tmp_path, {"title": "MyLab", "search_engine_icon": icon}
        )
    )
    html = app.test_client().get("/").get_data(as_text=True)

    assert icon in html
    assert "onerror" in html


def test_navbar_uses_custom_search_engine_in_action(tmp_path):
    custom = "https://duckduckgo.com/?q={query}"
    app = create_app(
        config_path=_write_config(tmp_path, {"title": "MyLab", "search_engine": custom})
    )
    html = app.test_client().get("/").get_data(as_text=True)

    assert "https://duckduckgo.com/" in html
