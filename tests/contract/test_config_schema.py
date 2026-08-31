"""Contract test: validates the YAML config file against contracts/config-contract.md.

The config must parse into a valid DashboardConfig with the documented structure
and field rules (http/https urls, non-empty names/labels, unknown keys ignored).
"""

import re
from pathlib import Path

import pytest
import yaml

from app.config import load_dashboard_from_file
from app.schema import parse_dashboard

EXAMPLE_YAML = Path(__file__).resolve().parents[2] / "config" / "example.yaml"


def _load_raw(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def test_example_yaml_exists():
    assert EXAMPLE_YAML.exists()


def test_example_yaml_is_mapping():
    data = _load_raw(EXAMPLE_YAML)
    assert isinstance(data, dict)


def test_example_yaml_parses_to_valid_config():
    config = load_dashboard_from_file(str(EXAMPLE_YAML))
    assert config.tiles, "example config should have at least one tile"
    assert config.bookmark_groups, "example config should have at least one group"


def test_contract_fields(example_config_data):
    # Per contract: root mapping, optional title/tiles/tile_groups/bookmark_groups
    # plus the feature-008 opt-in `editor`/`edit_config` flag (data-model.md).
    allowed = {
        "title",
        "tiles",
        "tile_groups",
        "bookmark_groups",
        "editor",
        "edit_config",
    }
    assert set(example_config_data) <= allowed


def test_contract_tile_required_fields(example_config_data):
    for tile in example_config_data.get("tiles", []):
        assert tile.get("name"), "tile.name required"
        assert re.match(r"^https?://", tile.get("url", "")), "tile.url must be http(s)"


def test_contract_tile_group_required_fields(example_config_data):
    for group in example_config_data.get("tile_groups", []):
        assert group.get("name"), "tile_group.name required"
        for tile in group.get("tiles", []):
            assert tile.get("name"), "tile_group.tiles[].name required"
            assert re.match(r"^https?://", tile.get("url", "")), (
                "tile_group.tiles[].url must be http(s)"
            )


def test_contract_bookmark_urls_http(example_config_data):
    for group in example_config_data.get("bookmark_groups", []):
        assert group.get("name"), "bookmark_group.name required"
        for bookmark in group.get("bookmarks", []):
            assert bookmark.get("label"), "bookmark.label required"
            assert re.match(r"^https?://", bookmark.get("url", "")), (
                "bookmark.url must be http(s)"
            )


@pytest.fixture
def example_config_data():
    return _load_raw(EXAMPLE_YAML)


def test_parse_dashboard_accepts_example_raw_data():
    data = _load_raw(EXAMPLE_YAML)
    config = parse_dashboard(data)
    assert len(config.tiles) == len(data.get("tiles", []))
