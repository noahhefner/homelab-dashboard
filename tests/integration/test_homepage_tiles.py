from pathlib import Path

import yaml

from app import create_app
from tests.soup_utils import parse

EXAMPLE_YAML = Path(__file__).resolve().parents[2] / "tests" / "static" / "test-config.yaml"


def _write_config(tmpdir, data):
    path = Path(tmpdir) / "config.yaml"
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return str(path)


def _soup_for(tmpdir, data):
    app = create_app(config_path=_write_config(tmpdir, data))
    return parse(app.test_client().get("/").get_data(as_text=True))


def test_homepage_renders_all_example_tiles():
    with open(EXAMPLE_YAML, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    app = create_app(config_path=str(EXAMPLE_YAML))
    soup = parse(app.test_client().get("/").get_data(as_text=True))

    configured_names = [
        tile["name"]
        for group in data.get("tile_groups", [])
        for tile in group.get("tiles", [])
    ]
    assert configured_names, "example config should have tiles"
    rendered_names = [t.get_text() for t in soup.select(".tile-name")]
    for name in configured_names:
        assert name in rendered_names


# --- User Story 2: grouped tiles render with labeled, always-visible headers --


def test_tile_groups_render_headers_and_own_tiles(tmpdir):
    data = {
        "tile_groups": [
            {"name": "Media", "tiles": [{"name": "Plex", "url": "https://plex.lan"}]},
            {
                "name": "Networking",
                "tiles": [{"name": "Pi-hole", "url": "https://pihole.lan"}],
            },
        ]
    }
    soup = _soup_for(tmpdir, data)
    headers = [h.get_text(strip=True) for h in soup.select("h3.group-title")]
    assert "Media" in headers
    assert "Networking" in headers
    rendered_names = [t.get_text() for t in soup.select(".tile-name")]
    assert "Plex" in rendered_names
    assert "Pi-hole" in rendered_names


def test_tile_groups_are_not_collapsible(tmpdir):
    data = {
        "tile_groups": [{"name": "G", "tiles": [{"name": "T", "url": "https://t.lan"}]}]
    }
    soup = _soup_for(tmpdir, data)
    # Tile groups have no collapse/expand control (no accordion button/data-bs-toggle)
    # in the tiles section.
    tiles = soup.select_one('section[aria-label="Tiles"]')
    assert tiles is not None
    assert tiles.select_one('[data-bs-toggle="collapse"]') is None


def test_tile_groups_render_in_declared_order(tmpdir):
    data = {
        "tile_groups": [
            {"name": "First", "tiles": [{"name": "A", "url": "https://a.lan"}]},
            {"name": "Second", "tiles": [{"name": "B", "url": "https://b.lan"}]},
        ]
    }
    soup = _soup_for(tmpdir, data)
    names = [el.get_text() for el in soup.select("h3.group-title .tile-group-name")]
    assert names == ["First", "Second"]


# --- User Story 3: optional tile-group icon renders beside the group name -------


def test_tile_group_with_icon_renders_img_beside_name(tmpdir):
    icon = "https://cdn.example.com/media.png"
    data = {
        "tile_groups": [
            {
                "name": "Media",
                "icon": icon,
                "tiles": [{"name": "Plex", "url": "https://plex.lan"}],
            }
        ]
    }
    soup = _soup_for(tmpdir, data)
    header = soup.select_one("h3.group-title")
    icon_img = header.select_one(".tile-group-icon")
    assert icon_img is not None
    assert icon_img.get("src") == icon


def test_tile_group_with_non_url_icon_renders_monogram(tmpdir):
    data = {
        "tile_groups": [
            {
                "name": "Media",
                "icon": "media",
                "tiles": [{"name": "Plex", "url": "https://plex.lan"}],
            }
        ]
    }
    soup = _soup_for(tmpdir, data)
    header = soup.select_one("h3.group-title")
    # A plain-word icon must NOT become an <img src>; the group shows a monogram.
    assert header.select_one(".tile-group-icon") is None
    monogram = header.select_one(".tile-group-monogram")
    assert monogram is not None
    assert monogram.get_text() == "M"


def test_tile_group_without_icon_renders_name_alone(tmpdir):
    data = {
        "tile_groups": [
            {"name": "Media", "tiles": [{"name": "Plex", "url": "https://plex.lan"}]}
        ]
    }
    soup = _soup_for(tmpdir, data)
    # No group icon <img> is emitted when none is configured.
    tiles = soup.select_one('section[aria-label="Tiles"]')
    assert tiles is not None
    assert tiles.select_one(".tile-group-icon") is None
    headers = soup.select("h3.group-title .tile-group-name")
    assert any(h.get_text() == "Media" for h in headers)


# --- User Story 5: hardcoded "Bookmarks" header above the accordion ------------


def test_bookmarks_header_renders_above_accordion(tmpdir):
    data = {
        "bookmark_groups": [
            {"name": "News", "bookmarks": [{"label": "BBC", "url": "https://bbc.com"}]}
        ]
    }
    soup = _soup_for(tmpdir, data)
    bookmarks_heading = soup.select_one("h2, h3")
    assert bookmarks_heading is not None
    assert bookmarks_heading.get_text() == "Bookmarks"
    accordion = soup.select_one(".accordion")
    assert accordion is not None
    assert accordion in bookmarks_heading.find_all_next()


def test_bookmarks_header_omitted_when_no_bookmark_groups(tmpdir):
    data = {
        "tile_groups": [
            {"name": "G", "tiles": [{"name": "Plex", "url": "https://plex.lan"}]}
        ]
    }
    soup = _soup_for(tmpdir, data)
    assert "No bookmarks configured yet." in soup.get_text()
    # The hardcoded header is scoped to bookmark groups; a bare config must not
    # render a "Bookmarks" heading above a tile section.
    heading_texts = [h.get_text(strip=True) for h in soup.find_all(["h1", "h2", "h3"])]
    assert "Bookmarks" not in heading_texts


# --- User Story 7: home page main section is aria-labeled "Tiles" --------------


def test_homepage_main_section_labeled_tiles(tmpdir):
    soup = _soup_for(
        tmpdir,
        {
            "tile_groups": [
                {"name": "G", "tiles": [{"name": "Plex", "url": "https://plex.lan"}]}
            ]
        },
    )
    assert soup.select_one('section[aria-label="Tiles"]') is not None
