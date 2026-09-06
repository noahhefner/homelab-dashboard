import os
import time

import yaml

from app import create_app
from tests.soup_utils import parse


def _home_soup(client):
    return parse(client.get("/").get_data(as_text=True))


def _write(path, data):
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def _bump_mtime(path):
    st = path.stat()
    os.utime(path, (st.st_atime_ns / 1e9, st.st_mtime_ns / 1e9 + 2.0))


def test_config_edit_reflected_on_refresh(tmp_path):
    cfg = tmp_path / "config.yaml"
    _write(
        cfg,
        {
            "tile_groups": [
                {"name": "G", "tiles": [{"name": "One", "url": "https://one.lan"}]}
            ]
        },
    )

    app = create_app(config_path=str(cfg))
    client = app.test_client()

    assert "One" in client.get("/").get_data(as_text=True)
    assert "Two" not in client.get("/").get_data(as_text=True)

    _write(
        cfg,
        {
            "tile_groups": [
                {
                    "name": "G",
                    "tiles": [
                        {"name": "One", "url": "https://one.lan"},
                        {"name": "Two", "url": "https://two.lan"},
                    ],
                }
            ]
        },
    )
    _bump_mtime(cfg)
    time.sleep(0.01)

    html = client.get("/").get_data(as_text=True)
    assert "Two" in html


def test_removing_bookmark_reflected_on_refresh(tmp_path):
    cfg = tmp_path / "config.yaml"
    _write(
        cfg,
        {
            "bookmark_groups": [
                {
                    "name": "G",
                    "bookmarks": [
                        {"label": "Keep", "url": "https://keep.com"},
                        {"label": "Drop", "url": "https://drop.com"},
                    ],
                }
            ]
        },
    )

    app = create_app(config_path=str(cfg))
    client = app.test_client()
    assert "Drop" in client.get("/").get_data(as_text=True)

    _write(
        cfg,
        {
            "bookmark_groups": [
                {
                    "name": "G",
                    "bookmarks": [{"label": "Keep", "url": "https://keep.com"}],
                }
            ]
        },
    )
    _bump_mtime(cfg)
    time.sleep(0.01)

    html = client.get("/").get_data(as_text=True)
    assert "Drop" not in html


def test_tile_logo_change_reflected_on_reload(tmp_path):
    cfg = tmp_path / "config.yaml"
    logo_a = "https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/svg/plex.svg"
    logo_b = "https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/svg/nextcloud.svg"
    _write(
        cfg,
        {
            "tile_groups": [
                {
                    "name": "G",
                    "tiles": [
                        {"name": "Svc", "url": "https://svc.lan", "icon": logo_a}
                    ],
                }
            ]
        },
    )

    app = create_app(config_path=str(cfg))
    client = app.test_client()

    # Initial: the logo <img> for logo_a is present.
    soup = _home_soup(client)
    img = soup.select_one("a.app-tile img")
    assert img is not None
    assert img.get("src") == logo_a

    # Change the logo to logo_b -> reflected on next request (no restart/rebuild).
    _write(
        cfg,
        {
            "tile_groups": [
                {
                    "name": "G",
                    "tiles": [
                        {"name": "Svc", "url": "https://svc.lan", "icon": logo_b}
                    ],
                }
            ]
        },
    )
    _bump_mtime(cfg)
    time.sleep(0.01)
    img = parse(client.get("/").get_data(as_text=True)).select_one("a.app-tile img")
    assert img is not None
    assert img.get("src") == logo_b

    # Remove the logo -> falls back to a monogram on reload.
    _write(
        cfg,
        {
            "tile_groups": [
                {"name": "G", "tiles": [{"name": "Svc", "url": "https://svc.lan"}]}
            ]
        },
    )
    _bump_mtime(cfg)
    time.sleep(0.01)
    soup = _home_soup(client)
    assert soup.select_one("a.app-tile img") is None
    monogram = soup.select_one(".tile-monogram")
    assert monogram is not None
    assert monogram.get_text() == "S"


def test_moving_tile_between_groups_reflected_on_reload(tmp_path):
    cfg = tmp_path / "config.yaml"
    _write(
        cfg,
        {
            "tile_groups": [
                {
                    "name": "GroupAlpha",
                    "tiles": [{"name": "TileMove", "url": "https://t.lan"}],
                },
                {"name": "GroupBeta", "tiles": []},
            ]
        },
    )

    app = create_app(config_path=str(cfg))
    client = app.test_client()
    html = client.get("/").get_data(as_text=True)
    # TileMove renders under GroupAlpha (the first group).
    assert html.index("TileMove") < html.index("GroupBeta")

    # Move TileMove from GroupAlpha to GroupBeta -> reflected on next request.
    _write(
        cfg,
        {
            "tile_groups": [
                {"name": "GroupAlpha", "tiles": []},
                {
                    "name": "GroupBeta",
                    "tiles": [{"name": "TileMove", "url": "https://t.lan"}],
                },
            ]
        },
    )
    _bump_mtime(cfg)
    time.sleep(0.01)

    html = client.get("/").get_data(as_text=True)
    # TileMove now renders in GroupBeta, which appears after GroupAlpha.
    assert html.index("GroupAlpha") < html.index("GroupBeta")
    assert html.index("GroupBeta") < html.index("TileMove")


def test_removing_grouped_tile_reflected_on_reload(tmp_path):
    cfg = tmp_path / "config.yaml"
    _write(
        cfg,
        {
            "tile_groups": [
                {"name": "G", "tiles": [{"name": "T", "url": "https://t.lan"}]}
            ]
        },
    )

    app = create_app(config_path=str(cfg))
    client = app.test_client()

    assert _home_soup(client).select_one(".tile-name") is not None

    # Remove the tile group -> on refresh the tile and its header disappear.
    _write(cfg, {"tile_groups": []})
    _bump_mtime(cfg)
    time.sleep(0.01)

    soup = _home_soup(client)
    assert soup.select_one(".tile-name") is None
    assert soup.select_one("h3.group-title") is None
