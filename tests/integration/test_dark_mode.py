from pathlib import Path

import yaml

from app import create_app


def _write_config(tmpdir, data):
    path = Path(tmpdir) / "config.yaml"
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return str(path)


def test_page_sets_a_theme_attribute_on_root(tmp_path):
    app = create_app(config_path=_write_config(tmp_path, {"title": "MyLab"}))
    html = app.test_client().get("/").get_data(as_text=True)

    # The root <html> element carries a data-bs-theme attribute so Bootstrap
    # 5.3 can switch the whole component palette between light and dark.
    assert '<html lang="en" data-bs-theme=' in html


def test_navbar_contains_theme_toggle(tmp_path):
    app = create_app(config_path=_write_config(tmp_path, {"title": "MyLab"}))
    html = app.test_client().get("/").get_data(as_text=True)

    assert "data-theme-toggle" in html
    # The toggle is rendered with an icon element for clear affordance.
    assert "theme-toggle" in html
