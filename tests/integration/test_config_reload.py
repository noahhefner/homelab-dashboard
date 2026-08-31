import os
import time

import yaml

from app import create_app


def _write(path, data):
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def _bump_mtime(path):
    st = path.stat()
    os.utime(path, (st.st_atime_ns / 1e9, st.st_mtime_ns / 1e9 + 2.0))


def test_config_edit_reflected_on_refresh(tmp_path):
    cfg = tmp_path / "config.yaml"
    _write(cfg, {"tiles": [{"name": "One", "url": "https://one.lan"}]})

    app = create_app(config_path=str(cfg))
    client = app.test_client()

    assert "One" in client.get("/").get_data(as_text=True)
    assert "Two" not in client.get("/").get_data(as_text=True)

    _write(
        cfg,
        {
            "tiles": [
                {"name": "One", "url": "https://one.lan"},
                {"name": "Two", "url": "https://two.lan"},
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
    _write(cfg, {"tiles": [{"name": "Svc", "url": "https://svc.lan", "icon": logo_a}]})

    app = create_app(config_path=str(cfg))
    client = app.test_client()

    # Initial: the logo <img> for logo_a is present.
    assert f'src="{logo_a}"' in client.get("/").get_data(as_text=True)

    # Change the logo to logo_b -> reflected on next request (no restart/rebuild).
    _write(cfg, {"tiles": [{"name": "Svc", "url": "https://svc.lan", "icon": logo_b}]})
    _bump_mtime(cfg)
    time.sleep(0.01)
    html = client.get("/").get_data(as_text=True)
    assert f'src="{logo_b}"' in html
    assert f'src="{logo_a}"' not in html

    # Remove the logo -> falls back to a monogram on reload.
    _write(cfg, {"tiles": [{"name": "Svc", "url": "https://svc.lan"}]})
    _bump_mtime(cfg)
    time.sleep(0.01)
    html = client.get("/").get_data(as_text=True)
    assert f'src="{logo_b}"' not in html
    assert '<span class="tile-monogram">S</span>' in html


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


def test_moving_grouped_tile_to_flat_list_reflected_on_reload(tmp_path):
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

    # Move T out of the group into the flat (ungrouped) tile list.
    _write(
        cfg,
        {
            "tiles": [{"name": "T", "url": "https://t.lan"}],
            "tile_groups": [],
        },
    )
    _bump_mtime(cfg)
    time.sleep(0.01)

    html = client.get("/").get_data(as_text=True)
    assert "T" in html
    # With the group removed, the tile is flat and no group header exists.
    assert '<h3 class="group-title">' not in html
