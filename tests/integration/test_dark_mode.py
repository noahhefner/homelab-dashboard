from pathlib import Path

import yaml

from app import create_app
from tests.soup_utils import parse


def _write_config(tmpdir, data):
    path = Path(tmpdir) / "config.yaml"
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return str(path)


def _page_soup(tmp_path, data):
    app = create_app(config_path=_write_config(tmp_path, data))
    return parse(app.test_client().get("/").get_data(as_text=True))


def test_page_sets_a_theme_attribute_on_root(tmp_path):
    soup = _page_soup(tmp_path, {"title": "MyLab"})

    # The root <html> element carries a data-bs-theme attribute so Bootstrap
    # 5.3 can switch the whole component palette between light and dark.
    root = soup.find("html")
    assert root is not None
    assert root.has_attr("data-bs-theme")


def test_navbar_contains_theme_toggle(tmp_path):
    soup = _page_soup(tmp_path, {"title": "MyLab"})

    toggle = soup.select_one("[data-theme-toggle]")
    assert toggle is not None
    # The toggle is rendered with an icon element for clear affordance.
    assert soup.select_one(".theme-toggle i") is not None
