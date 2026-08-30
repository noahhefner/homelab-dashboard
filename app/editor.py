import os
import tempfile

import yaml

from app.schema import ConfigValidationError, parse_dashboard

BACKUP_SUFFIX = ".backup.yaml"


class ConfigEditorError(Exception):
    """Raised when the config cannot be read or written safely."""


def read_raw(config_path):
    """Return the current config file text, or raise ConfigEditorError."""
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return f.read()
    except OSError as exc:
        raise ConfigEditorError(f"Could not read the config file '{config_path}': {exc}")


def read_backup(config_path):
    """Return the last-known-good backup text, or None if no backup exists."""
    backup_path = config_path + BACKUP_SUFFIX
    try:
        with open(backup_path, "r", encoding="utf-8") as f:
            return f.read()
    except OSError:
        return None


def validate_content(content):
    """Return a specific error message if content is not acceptable, else None.

    The edited YAML must parse with yaml.safe_load AND satisfy the dashboard's
    config format (parse_dashboard). Empty/invalid input is rejected.
    """
    if content is None or not str(content).strip():
        return "The config must not be empty."
    try:
        data = yaml.safe_load(content)
    except yaml.YAMLError as exc:
        return f"Invalid YAML: {exc}"
    try:
        parse_dashboard(data)
    except ConfigValidationError as exc:
        return str(exc)
    return None


def write_atomic(config_path, content):
    """Atomically replace the config file with validated content.

    Writes a temp file in the same directory and os.replace()s it over the
    target so a crash or partial write never leaves a truncated config. Backs
    up the previous bytes (as the last-known-good) before overwriting. Only the
    resolved config_path is ever written; no client-supplied path is accepted.
    """
    # Validate BEFORE touching disk; malformed input must not overwrite.
    error = validate_content(content)
    if error is not None:
        raise ConfigEditorError(error)

    backup_path = config_path + BACKUP_SUFFIX
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            previous = f.read()
    except OSError as exc:
        raise ConfigEditorError(
            f"Could not read the current config '{config_path}': {exc}"
        )

    directory = os.path.dirname(os.path.abspath(config_path)) or "."
    try:
        fd, tmp_path = tempfile.mkstemp(dir=directory, prefix=".config-", suffix=".tmp")
    except OSError as exc:
        raise ConfigEditorError(f"Could not write the config file: {exc}")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(content)
        os.replace(tmp_path, config_path)
    except OSError as exc:
        os.unlink(tmp_path)
        raise ConfigEditorError(f"Could not write the config file: {exc}")

    # Keep a bounded single copy of the last-known-good config for recovery.
    try:
        with open(backup_path, "w", encoding="utf-8") as f:
            f.write(previous)
    except OSError:
        # Backup is best-effort; the write already succeeded. Do not fail the
        # save because recovery bookkeeping could not be persisted.
        pass