from pathlib import Path

import yaml

from app import create_app
from tests.soup_utils import parse


def _write_config(tmpdir, data):
    path = Path(tmpdir) / "config.yaml"
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return str(path)


def _home_soup(tmp_path, data):
    app = create_app(config_path=_write_config(tmp_path, data))
    return parse(app.test_client().get("/").get_data(as_text=True))


def test_bookmark_groups_render_grouped(tmp_path):
    data = {
        "bookmark_groups": [
            {
                "name": "Media",
                "bookmarks": [{"label": "YouTube", "url": "https://youtube.com"}],
            },
            {
                "name": "Finance",
                "bookmarks": [{"label": "Bank", "url": "https://bank.com"}],
            },
        ]
    }
    soup = _home_soup(tmp_path, data)

    group_names = [h.get_text(strip=True) for h in soup.select(".accordion-header")]
    assert "Media" in group_names
    assert "Finance" in group_names
    labels = [l.get_text() for l in soup.select(".bookmark-label")]
    assert "YouTube" in labels
    assert "Bank" in labels


def test_large_number_of_bookmarks_renders(tmp_path):
    groups = []
    for g in range(5):
        bookmarks = [
            {"label": f"B{g}-{i}", "url": f"https://example.com/{g}/{i}"}
            for i in range(30)
        ]
        groups.append({"name": f"Group {g}", "bookmarks": bookmarks})

    soup = _home_soup(tmp_path, {"bookmark_groups": groups})

    labels = [l.get_text() for l in soup.select(".bookmark-label")]
    for g in range(5):
        assert f"B{g}-29" in labels


def test_collapsed_group_renders_collapsed_class(tmp_path):
    data = {
        "bookmark_groups": [
            {
                "name": "Media",
                "collapsed": True,
                "bookmarks": [{"label": "YouTube", "url": "https://youtube.com"}],
            },
            {
                "name": "Finance",
                "bookmarks": [{"label": "Bank", "url": "https://bank.com"}],
            },
        ]
    }
    soup = _home_soup(tmp_path, data)

    # The collapsed group's toggle carries the Bootstrap `collapsed` class and
    # its content omits `show`; the open group's content includes `show`.
    buttons = soup.select("button.accordion-button")
    collapses = soup.select(".accordion-collapse")
    assert len(buttons) == 2
    assert len(collapses) == 2
    collapsed_btn = buttons[0]
    open_btn = buttons[1]
    collapsed_panel = collapses[0]
    open_panel = collapses[1]
    assert "collapsed" in (collapsed_btn.get("class") or [])
    assert "collapsed" not in (open_btn.get("class") or [])
    assert "show" not in (collapsed_panel.get("class") or [])
    assert "show" in (open_panel.get("class") or [])
