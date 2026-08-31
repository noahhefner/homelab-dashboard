import pytest

from app.schema import ConfigValidationError, parse_dashboard


def test_valid_full_config():
    data = {
        "title": "My Lab",
        "tiles": [{"name": "Plex", "url": "https://plex.lan:32400", "icon": "plex"}],
        "tile_groups": [
            {
                "name": "Media",
                "icon": "play",
                "tiles": [{"name": "Emby", "url": "https://emby.lan"}],
            }
        ],
        "bookmark_groups": [
            {
                "name": "Media",
                "icon": "play",
                "bookmarks": [{"label": "YouTube", "url": "https://youtube.com"}],
            }
        ],
    }
    config = parse_dashboard(data)
    assert config.title == "My Lab"
    assert len(config.tiles) == 1
    assert config.tiles[0].name == "Plex"
    assert config.tiles[0].icon == "plex"
    assert len(config.tile_groups) == 1
    assert config.tile_groups[0].name == "Media"
    assert config.tile_groups[0].icon == "play"
    assert config.tile_groups[0].tiles[0].name == "Emby"
    assert len(config.bookmark_groups) == 1
    assert config.bookmark_groups[0].name == "Media"
    assert config.bookmark_groups[0].bookmarks[0].label == "YouTube"


def test_empty_config_returns_defaults():
    config = parse_dashboard({})
    assert config.title == "Homelab"
    assert config.tiles == []
    assert config.tile_groups == []
    assert config.bookmark_groups == []


def test_none_config_returns_defaults():
    config = parse_dashboard(None)
    assert config.title == "Homelab"
    assert config.tiles == []
    assert config.tile_groups == []


def test_blank_title_returns_default():
    config = parse_dashboard({"title": "   "})
    assert config.title == "Homelab"


def test_empty_string_title_returns_default():
    config = parse_dashboard({"title": ""})
    assert config.title == "Homelab"


def test_custom_title_is_preserved_and_stripped():
    config = parse_dashboard({"title": "  My Lab  "})
    assert config.title == "My Lab"


def test_missing_tile_name_raises():
    with pytest.raises(ConfigValidationError):
        parse_dashboard({"tiles": [{"url": "https://example.com"}]})


def test_invalid_tile_url_raises():
    with pytest.raises(ConfigValidationError):
        parse_dashboard({"tiles": [{"name": "Bad", "url": "not-a-url"}]})


def test_non_http_url_raises():
    with pytest.raises(ConfigValidationError):
        parse_dashboard({"tiles": [{"name": "Ftp", "url": "ftp://example.com"}]})


def test_unknown_top_level_keys_ignored():
    config = parse_dashboard({"unknown_key": "ignored", "tiles": []})
    assert config.tiles == []


def test_legacy_services_key_not_recognized_as_tiles():
    # Clarification Q1 -> A: the legacy `services`/`service_groups` keys are NOT
    # supported. A config that only uses them yields an empty tiles list.
    config = parse_dashboard(
        {"services": [{"name": "Plex", "url": "https://plex.lan"}]}
    )
    assert config.tiles == []
    assert config.tile_groups == []


def test_non_mapping_root_raises():
    with pytest.raises(ConfigValidationError):
        parse_dashboard([1, 2, 3])


def test_missing_bookmark_label_raises():
    with pytest.raises(ConfigValidationError):
        parse_dashboard(
            {
                "bookmark_groups": [
                    {"name": "G", "bookmarks": [{"url": "https://x.com"}]}
                ]
            }
        )


def test_group_collapsed_true_parses():
    config = parse_dashboard(
        {"bookmark_groups": [{"name": "G", "collapsed": True, "bookmarks": []}]}
    )
    assert config.bookmark_groups[0].collapsed is True


def test_group_collapsed_false_or_absent_is_open():
    config = parse_dashboard(
        {
            "bookmark_groups": [
                {"name": "G1", "collapsed": False, "bookmarks": []},
                {"name": "G2", "bookmarks": []},
            ]
        }
    )
    assert config.bookmark_groups[0].collapsed is False
    assert config.bookmark_groups[1].collapsed is False


def test_group_collapsed_null_is_open():
    config = parse_dashboard(
        {"bookmark_groups": [{"name": "G", "collapsed": None, "bookmarks": []}]}
    )
    assert config.bookmark_groups[0].collapsed is False


def test_group_collapsed_non_boolean_raises():
    with pytest.raises(ConfigValidationError):
        parse_dashboard(
            {"bookmark_groups": [{"name": "G", "collapsed": "yes", "bookmarks": []}]}
        )


def test_tile_group_missing_name_raises():
    with pytest.raises(ConfigValidationError):
        parse_dashboard(
            {"tile_groups": [{"tiles": [{"name": "A", "url": "https://a.lan"}]}]}
        )


def test_tile_group_non_list_tiles_raises():
    with pytest.raises(ConfigValidationError):
        parse_dashboard({"tile_groups": [{"name": "G", "tiles": "not-a-list"}]})


def test_tile_groups_must_be_a_list():
    with pytest.raises(ConfigValidationError):
        parse_dashboard({"tile_groups": "not-a-list"})


def test_tile_group_empty_tiles_is_valid():
    config = parse_dashboard({"tile_groups": [{"name": "G"}]})
    assert config.tile_groups[0].name == "G"
    assert config.tile_groups[0].tiles == []


def test_tile_group_invalid_nested_tile_raises():
    with pytest.raises(ConfigValidationError):
        parse_dashboard(
            {"tile_groups": [{"name": "G", "tiles": [{"name": "Bad", "url": "nope"}]}]}
        )
