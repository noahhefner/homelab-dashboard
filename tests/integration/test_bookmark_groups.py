from pathlib import Path

import yaml

from app import create_app

EXAMPLE_YAML = Path(__file__).resolve().parents[2] / "config" / "example.yaml"


def _write_config(tmpdir, data):
    path = Path(tmpdir) / "config.yaml"
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return str(path)


def test_bookmark_groups_render_grouped(tmp_path):
    data = {
        "bookmark_groups": [
            {"name": "Media", "bookmarks": [{"label": "YouTube", "url": "https://youtube.com"}]},
            {"name": "Finance", "bookmarks": [{"label": "Bank", "url": "https://bank.com"}]},
        ]
    }
    app = create_app(config_path=_write_config(tmp_path, data))
    html = app.test_client().get("/").get_data(as_text=True)

    assert "Media" in html
    assert "Finance" in html
    assert "YouTube" in html
    assert "Bank" in html


def test_large_number_of_bookmarks_renders(tmp_path):
    groups = []
    for g in range(5):
        bookmarks = [{"label": f"B{g}-{i}", "url": f"https://example.com/{g}/{i}"} for i in range(30)]
        groups.append({"name": f"Group {g}", "bookmarks": bookmarks})

    app = create_app(config_path=_write_config(tmp_path, {"bookmark_groups": groups}))
    html = app.test_client().get("/").get_data(as_text=True)

    for g in range(5):
        assert f"Group {g}" in html
        assert f"B{g}-29" in html


def test_collapsed_group_renders_default_collapsed_marker(tmp_path):
    data = {
        "bookmark_groups": [
            {"name": "Media", "collapsed": True, "bookmarks": [
                {"label": "YouTube", "url": "https://youtube.com"}]},
            {"name": "Finance", "bookmarks": [
                {"label": "Bank", "url": "https://bank.com"}]},
        ]
    }
    app = create_app(config_path=_write_config(tmp_path, data))
    html = app.test_client().get("/").get_data(as_text=True)

    # The collapsed group's toggle carries a collapsed default; the unset group
    # carries the open default.
    assert 'data-default-collapsed="true"' in html
    assert 'data-default-collapsed="false"' in html
