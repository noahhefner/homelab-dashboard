from pathlib import Path

import pytest
import yaml

from app import create_app
from tests.soup_utils import parse


def _write_config(tmpdir, data):
    path = Path(tmpdir) / "config.yaml"
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return str(path)


@pytest.fixture
def client_with_tiles(tmpdir):
    data = {
        "title": "Test Lab",
        "tile_groups": [
            {
                "name": "Media",
                "tiles": [
                    {
                        "name": "Plex",
                        "url": "https://plex.lan:32400",
                        "icon": "https://cdn.example.com/plex.png",
                    },
                    {
                        "name": "Nextcloud",
                        "url": "https://cloud.lan",
                        "icon": "nextcloud",
                    },
                    {
                        "name": "<script>alert('x')</script>",
                        "url": "https://unsafe.lan",
                    },
                ],
            }
        ],
    }
    app = create_app(config_path=_write_config(tmpdir, data))
    return app.test_client()


def _home_soup(client):
    return parse(client.get("/").get_data(as_text=True))


def test_tiles_render_name_and_url(client_with_tiles):
    resp = client_with_tiles.get("/")
    assert resp.status_code == 200
    soup = parse(resp.get_data(as_text=True))
    names = [t.get_text() for t in soup.select(".tile-name")]
    assert "Plex" in names
    assert "Nextcloud" in names
    assert "https://plex.lan:32400" in [
        a.get("href") for a in soup.select("a.app-tile")
    ]


def test_tile_with_icon_url_renders_img(client_with_tiles):
    soup = _home_soup(client_with_tiles)
    plex = soup.select_one("a.app-tile")
    assert plex.select_one("img").get("src") == "https://cdn.example.com/plex.png"


def test_tile_without_url_icon_renders_monogram(client_with_tiles):
    soup = _home_soup(client_with_tiles)
    # 'N' is the first letter of Nextcloud, which lacks a URL icon -> monogram
    tiles = soup.select("a.app-tile")
    nextcloud = next(t for t in tiles if "Nextcloud" in t.get_text())
    monogram = nextcloud.select_one(".tile-monogram")
    assert monogram is not None
    assert monogram.get_text() == "N"


def test_tile_names_are_html_escaped(client_with_tiles):
    soup = _home_soup(client_with_tiles)
    assert "<script>alert('x')</script>" not in str(soup)
    escaped = [t for t in soup.select(".tile-name")]
    assert any(t.get_text() == "<script>alert('x')</script>" for t in escaped)


def test_tile_links_open_in_new_tab(client_with_tiles):
    soup = _home_soup(client_with_tiles)
    for tile in soup.select("a.app-tile"):
        assert tile.get("target") == "_blank"
        assert "noopener" in (tile.get("rel") or [])


def test_non_url_icon_renders_monogram_not_img(tmpdir):
    data = {
        "tile_groups": [
            {
                "name": "G",
                "tiles": [
                    {
                        "name": "Nextcloud",
                        "url": "https://cloud.lan",
                        "icon": "nextcloud",
                    },
                ],
            }
        ]
    }
    app = create_app(config_path=_write_config(tmpdir, data))
    soup = parse(app.test_client().get("/").get_data(as_text=True))
    # A plain-word (non-URL) icon must NOT become an <img src>; it shows a monogram.
    assert not any(img.get("src") == "nextcloud" for img in soup.find_all("img"))
    assert soup.find("img") is None
    monogram = soup.select_one(".tile-monogram")
    assert monogram is not None
    assert monogram.get_text() == "N"


def test_unsafe_icon_value_not_rendered_as_img_src(tmpdir):
    data = {
        "tile_groups": [
            {
                "name": "G",
                "tiles": [
                    {
                        "name": "Unsafe",
                        "url": "https://unsafe.lan",
                        "icon": "javascript:alert(1)",
                    },
                ],
            }
        ]
    }
    app = create_app(config_path=_write_config(tmpdir, data))
    soup = parse(app.test_client().get("/").get_data(as_text=True))
    # Unsafe / non-http(s) icon values are never emitted as an image source.
    assert soup.find("img") is None
    assert not any(
        (img.get("src") or "").startswith("javascript:") for img in soup.find_all("img")
    )
    monogram = soup.select_one(".tile-monogram")
    assert monogram is not None
    assert monogram.get_text() == "U"
