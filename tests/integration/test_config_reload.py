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
    _write(cfg, {"services": [{"name": "One", "url": "https://one.lan"}]})

    app = create_app(config_path=str(cfg))
    client = app.test_client()

    assert "One" in client.get("/").get_data(as_text=True)
    assert "Two" not in client.get("/").get_data(as_text=True)

    _write(
        cfg,
        {
            "services": [
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


def test_service_logo_change_reflected_on_reload(tmp_path):
    cfg = tmp_path / "config.yaml"
    logo_a = "https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/svg/plex.svg"
    logo_b = "https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/svg/nextcloud.svg"
    _write(
        cfg, {"services": [{"name": "Svc", "url": "https://svc.lan", "icon": logo_a}]}
    )

    app = create_app(config_path=str(cfg))
    client = app.test_client()

    # Initial: the logo <img> for logo_a is present.
    assert f'src="{logo_a}"' in client.get("/").get_data(as_text=True)

    # Change the logo to logo_b -> reflected on next request (no restart/rebuild).
    _write(
        cfg, {"services": [{"name": "Svc", "url": "https://svc.lan", "icon": logo_b}]}
    )
    _bump_mtime(cfg)
    time.sleep(0.01)
    html = client.get("/").get_data(as_text=True)
    assert f'src="{logo_b}"' in html
    assert f'src="{logo_a}"' not in html

    # Remove the logo -> falls back to a monogram on reload.
    _write(cfg, {"services": [{"name": "Svc", "url": "https://svc.lan"}]})
    _bump_mtime(cfg)
    time.sleep(0.01)
    html = client.get("/").get_data(as_text=True)
    assert f'src="{logo_b}"' not in html
    assert '<span class="service-monogram">S</span>' in html
