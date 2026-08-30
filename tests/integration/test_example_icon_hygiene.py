from pathlib import Path

import yaml

EXAMPLE_YAML = Path(__file__).resolve().parents[2] / "config" / "example.yaml"


def _is_supported_icon(value):
    # A supported icon is a full http(s) URL or absent (None).
    if value is None:
        return True
    return isinstance(value, str) and value.startswith(("http://", "https://"))


def test_example_yaml_has_no_short_word_icons():
    with open(EXAMPLE_YAML, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    short_words = []
    for gi, group in enumerate(data.get("bookmark_groups", [])):
        if not _is_supported_icon(group.get("icon")):
            short_words.append(f"bookmark_groups[{gi}].icon={group.get('icon')}")
        for bi, bookmark in enumerate(group.get("bookmarks", [])):
            icon = bookmark.get("icon")
            if not _is_supported_icon(icon):
                short_words.append(f"bookmark_groups[{gi}].bookmarks[{bi}].icon={icon}")

    assert not short_words, "Unsupported short-word icon values found:\n" + "\n".join(
        short_words
    )
