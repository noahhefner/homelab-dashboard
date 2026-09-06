from pathlib import Path

import yaml

from app import create_app

EXAMPLE_YAML = Path(__file__).resolve().parents[2] / "config" / "example.yaml"


def _write_config(tmpdir, data):
    path = Path(tmpdir) / "config.yaml"
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return str(path)


def _html_for(tmpdir, data):
    app = create_app(config_path=_write_config(tmpdir, data))
    return app.test_client().get("/").get_data(as_text=True)


def test_homepage_renders_all_example_tiles():
    with open(EXAMPLE_YAML, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    app = create_app(config_path=str(EXAMPLE_YAML))
    html = app.test_client().get("/").get_data(as_text=True)

    configured_names = [
        tile["name"]
        for group in data.get("tile_groups", [])
        for tile in group.get("tiles", [])
    ]
    assert configured_names, "example config should have tiles"
    for name in configured_names:
        assert name in html


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
    html = _html_for(tmpdir, data)
    assert '<h3 class="group-title">' in html
    assert "Media" in html
    assert "Networking" in html
    assert "Plex" in html
    assert "Pi-hole" in html


def test_tile_groups_are_not_collapsible(tmpdir):
    data = {
        "tile_groups": [{"name": "G", "tiles": [{"name": "T", "url": "https://t.lan"}]}]
    }
    html = _html_for(tmpdir, data)
    # Tile groups have no collapse/expand control (no accordion button/data-bs-toggle).
    assert 'data-bs-toggle="collapse"' not in html.split("bookmark-accordion")[0]


def test_tile_groups_render_in_declared_order(tmpdir):
    data = {
        "tile_groups": [
            {"name": "First", "tiles": [{"name": "A", "url": "https://a.lan"}]},
            {"name": "Second", "tiles": [{"name": "B", "url": "https://b.lan"}]},
        ]
    }
    html = _html_for(tmpdir, data)
    assert html.index("First") < html.index("Second")


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
    html = _html_for(tmpdir, data)
    assert f'src="{icon}"' in html
    # The icon renders inside the group header, before the group name.
    header = html.split('</h3>')[0]
    assert f'src="{icon}"' in header


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
    html = _html_for(tmpdir, data)
    # A plain-word icon must NOT become an <img src>; the group shows a monogram.
    assert 'class="tile-group-icon"' not in html
    assert '<span class="tile-group-monogram">M</span>' in html


def test_tile_group_without_icon_renders_name_alone(tmpdir):
    data = {
        "tile_groups": [
            {"name": "Media", "tiles": [{"name": "Plex", "url": "https://plex.lan"}]}
        ]
    }
    html = _html_for(tmpdir, data)
    assert "Media" in html
    # No group icon <img> is emitted when none is configured.
    assert "<img" not in html.split("bookmark-accordion")[0]


# --- User Story 5: hardcoded "Bookmarks" header above the accordion ------------


def test_bookmarks_header_renders_above_accordion(tmpdir):
    data = {
        "bookmark_groups": [
            {"name": "News", "bookmarks": [{"label": "BBC", "url": "https://bbc.com"}]}
        ]
    }
    html = _html_for(tmpdir, data)
    bookmarks_pos = html.index("Bookmarks")
    accordion_pos = html.index("bookmark-accordion")
    assert "Bookmarks" in html
    assert bookmarks_pos < accordion_pos


def test_bookmarks_header_omitted_when_no_bookmark_groups(tmpdir):
    data = {
        "tile_groups": [
            {"name": "G", "tiles": [{"name": "Plex", "url": "https://plex.lan"}]}
        ]
    }
    html = _html_for(tmpdir, data)
    assert "No bookmarks configured yet." in html
    # The hardcoded header is scoped to bookmark groups; a bare config must not
    # render a "Bookmarks" heading above a tile section.
    assert html.count(">Bookmarks<") == 0


# --- User Story 7: home page main section is aria-labeled "Tiles" --------------


def test_homepage_main_section_labeled_tiles(tmpdir):
    html = _html_for(
        tmpdir,
        {
            "tile_groups": [
                {"name": "G", "tiles": [{"name": "Plex", "url": "https://plex.lan"}]}
            ]
        },
    )
    assert 'aria-label="Tiles"' in html
