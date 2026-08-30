from pathlib import Path

import yaml

from app import create_app


def _write_config(tmpdir, data):
    path = Path(tmpdir) / "config.yaml"
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return str(path)


def test_accordion_chevron_not_literal_carat(tmp_path):
    data = {
        "bookmark_groups": [
            {
                "name": "Media",
                "bookmarks": [{"label": "YouTube", "url": "https://youtube.com"}],
            }
        ]
    }
    app = create_app(config_path=_write_config(tmp_path, data))
    html = app.test_client().get("/").get_data(as_text=True)

    # Each group is rendered as a Bootstrap accordion item whose header button
    # provides the open/closed chevron affordance (via its ::after icon). A
    # literal carat character is never used.
    assert 'class="accordion-button' in html
    assert "\u25be" not in html


def test_accordion_header_contains_group_name(tmp_path):
    data = {
        "bookmark_groups": [
            {
                "name": "Media",
                "bookmarks": [{"label": "YouTube", "url": "https://youtube.com"}],
            }
        ]
    }
    app = create_app(config_path=_write_config(tmp_path, data))
    html = app.test_client().get("/").get_data(as_text=True)

    # The group name is the focusable accordion header button.
    assert 'class="accordion-header"' in html
    assert "Media" in html
