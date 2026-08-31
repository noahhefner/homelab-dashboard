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
