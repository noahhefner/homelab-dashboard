import pytest
import yaml

from app.editor import (
    ConfigEditorError,
    download_content,
    read_backup,
    read_raw,
    validate_content,
    write_atomic,
)


def _valid_config():
    return "title: Homelab\ntiles:\n  - name: Plex\n    url: https://plex.lan\n"


# --- validate_content ---


def test_valid_content_returns_none():
    assert validate_content(_valid_config()) is None


def test_empty_content_rejected():
    assert validate_content("") is not None
    assert validate_content("   \n\t ") is not None


def test_malformed_yaml_rejected_with_specific_message():
    error = validate_content("tiles:\n  - name: [unclosed")
    assert error is not None
    assert "YAML" in error


def test_valid_yaml_format_violation_rejected():
    error = validate_content('title: Homelab\ntiles: "a string, not a list"')
    assert error is not None
    assert "tiles" in error


# --- write_atomic / atomic write + round-trip ---


def test_write_atomic_writes_validated_content(tmp_path):
    cfg = tmp_path / "config.yaml"
    cfg.write_text(_valid_config(), encoding="utf-8")

    new_content = "title: New\ntiles: []\n"
    write_atomic(str(cfg), new_content)

    assert cfg.read_text(encoding="utf-8") == new_content


def test_write_atomic_rejects_invalid_and_preserves_previous(tmp_path):
    cfg = tmp_path / "config.yaml"
    cfg.write_text(_valid_config(), encoding="utf-8")
    original = cfg.read_text(encoding="utf-8")

    with pytest.raises(ConfigEditorError):
        write_atomic(str(cfg), "tiles:\n  - name: [unclosed")

    assert cfg.read_text(encoding="utf-8") == original


def test_write_atomic_preserves_bytes_exactly(tmp_path):
    cfg = tmp_path / "config.yaml"
    content = (
        "title: Homelab\n"
        "\n"
        "# a comment with  trailing spaces   \n"
        "tiles:\n"
        '  - name: "Quoted"\n'
        "    url: https://plex.lan\n"
        "\n"
    )
    cfg.write_text(content, encoding="utf-8")

    write_atomic(str(cfg), content)
    assert cfg.read_text(encoding="utf-8") == content


def test_write_atomic_creates_backup_of_previous(tmp_path):
    cfg = tmp_path / "config.yaml"
    cfg.write_text(_valid_config(), encoding="utf-8")

    new_content = "title: New\ntiles: []\n"
    write_atomic(str(cfg), new_content)

    backup = read_backup(str(cfg))
    assert backup is not None
    assert backup == _valid_config()


def test_read_backup_none_when_missing(tmp_path):
    cfg = tmp_path / "config.yaml"
    cfg.write_text(_valid_config(), encoding="utf-8")
    assert read_backup(str(cfg)) is None


def test_recover_restores_last_known_good(tmp_path):
    cfg = tmp_path / "config.yaml"
    cfg.write_text(_valid_config(), encoding="utf-8")

    # First save: previous (_valid_config) becomes the backup.
    write_atomic(str(cfg), "title: Second\ntiles: []\n")
    # Second save: "Second" becomes the backup.
    write_atomic(str(cfg), "title: Third\ntiles: []\n")

    backup = read_backup(str(cfg))
    assert backup is not None
    assert "Second" in backup
    assert "Third" not in backup

    # Restore the last-known-good over the current file.
    write_atomic(str(cfg), backup)
    assert cfg.read_text(encoding="utf-8") == backup


# --- read_raw ---


def test_read_raw_returns_current_text(tmp_path):
    cfg = tmp_path / "config.yaml"
    cfg.write_text(_valid_config(), encoding="utf-8")
    assert read_raw(str(cfg)) == _valid_config()


def test_read_raw_missing_file_raises(tmp_path):
    with pytest.raises(ConfigEditorError):
        read_raw(str(tmp_path / "missing.yaml"))


# --- download_content ---


def test_download_content_returns_bytes_and_basename(tmp_path):
    content = "title: Homelab\ntiles: []\n"
    cfg = tmp_path / "site.yaml"
    cfg.write_text(content, encoding="utf-8")

    data, filename = download_content(str(cfg))

    assert data == content.encode("utf-8")
    assert data == cfg.read_bytes()
    assert filename == "site.yaml"


def test_download_content_preserves_exact_bytes(tmp_path):
    content = (
        "title: Homelab\n"
        "\n"
        "# comment with  trailing  spaces   \n"
        "tiles:\n"
        '  - name: "Quoted"\n'
        "    url: https://plex.lan\n"
        "\n"
    )
    cfg = tmp_path / "config.yaml"
    cfg.write_text(content, encoding="utf-8")

    data, _ = download_content(str(cfg))

    assert data == content.encode("utf-8")


def test_download_content_missing_file_raises(tmp_path):
    with pytest.raises(ConfigEditorError):
        download_content(str(tmp_path / "missing.yaml"))


# --- writable-failure (read-only) handling ---


def test_write_atomic_round_trips_yaml_safe(tmp_path):
    cfg = tmp_path / "config.yaml"
    cfg.write_text(_valid_config(), encoding="utf-8")
    write_atomic(str(cfg), _valid_config())
    parsed = yaml.safe_load(cfg.read_text(encoding="utf-8"))
    assert parsed["title"] == "Homelab"
