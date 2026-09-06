from pathlib import Path

import yaml

from app import create_app
from tests.soup_utils import parse


def _write_config(tmpdir, data):
    path = Path(tmpdir) / "config.yaml"
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return str(path)


def _group_data():
    return {
        "bookmark_groups": [
            {
                "name": "Media",
                "bookmarks": [{"label": "YouTube", "url": "https://youtube.com"}],
            }
        ]
    }


def test_accordion_chevron_not_literal_carat(tmp_path):
    app = create_app(config_path=_write_config(tmp_path, _group_data()))
    soup = parse(app.test_client().get("/").get_data(as_text=True))

    # Each group is rendered as a Bootstrap accordion item whose header button
    # provides the open/closed chevron affordance (via its ::after icon). A
    # literal carat character is never used.
    assert soup.select_one("button.accordion-button") is not None
    assert "\u25be" not in soup.get_text()


def test_accordion_header_contains_group_name(tmp_path):
    app = create_app(config_path=_write_config(tmp_path, _group_data()))
    soup = parse(app.test_client().get("/").get_data(as_text=True))

    # The group name is the focusable accordion header button.
    header = soup.select_one(".accordion-header")
    assert header is not None
    assert "Media" in header.get_text()
