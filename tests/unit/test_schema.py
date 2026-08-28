import pytest

from app.schema import ConfigValidationError, parse_dashboard


def test_valid_full_config():
    data = {
        "title": "My Lab",
        "services": [{"name": "Plex", "url": "https://plex.lan:32400", "icon": "plex"}],
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
    assert len(config.services) == 1
    assert config.services[0].name == "Plex"
    assert config.services[0].icon == "plex"
    assert len(config.bookmark_groups) == 1
    assert config.bookmark_groups[0].name == "Media"
    assert config.bookmark_groups[0].bookmarks[0].label == "YouTube"


def test_empty_config_returns_defaults():
    config = parse_dashboard({})
    assert config.title == "Home Lab"
    assert config.services == []
    assert config.bookmark_groups == []


def test_none_config_returns_defaults():
    config = parse_dashboard(None)
    assert config.title == "Home Lab"
    assert config.services == []


def test_missing_service_name_raises():
    with pytest.raises(ConfigValidationError):
        parse_dashboard({"services": [{"url": "https://example.com"}]})


def test_invalid_service_url_raises():
    with pytest.raises(ConfigValidationError):
        parse_dashboard({"services": [{"name": "Bad", "url": "not-a-url"}]})


def test_non_http_url_raises():
    with pytest.raises(ConfigValidationError):
        parse_dashboard({"services": [{"name": "Ftp", "url": "ftp://example.com"}]})


def test_unknown_top_level_keys_ignored():
    config = parse_dashboard({"unknown_key": "ignored", "services": []})
    assert config.services == []


def test_non_mapping_root_raises():
    with pytest.raises(ConfigValidationError):
        parse_dashboard([1, 2, 3])


def test_missing_bookmark_label_raises():
    with pytest.raises(ConfigValidationError):
        parse_dashboard(
            {"bookmark_groups": [{"name": "G", "bookmarks": [{"url": "https://x.com"}]}]}
        )
