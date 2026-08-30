import os

import yaml

from app.schema import ConfigValidationError, parse_dashboard

DEFAULT_CONFIG_PATH = "config/example.yaml"


def load_dashboard_from_file(path):
    """Read and parse a YAML config file into a DashboardConfig.

    Raises FileNotFoundError, yaml.YAMLError, or ConfigValidationError.
    """
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return parse_dashboard(data)


_EDITOR_KEYS = ("editor", "edit_config")


def _read_raw_config(path):
    """Return the raw YAML text of a config file, or None if unreadable."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except OSError:
        return None


class ConfigLoader:
    """Loads the dashboard config from a single YAML file with live reload.

    The config is re-parsed only when the file's modification time or size
    changes, so an edited (volume-mounted) file is picked up on the next page
    request without restarting the backend or container.
    """

    def __init__(self, path=DEFAULT_CONFIG_PATH):
        self.path = path
        self._stat = None
        self._config = None
        self._error = None
        self._load_if_needed(force=True)

    def _current_stat(self):
        try:
            st = os.stat(self.path)
            return (st.st_mtime_ns, st.st_size)
        except OSError:
            return None

    def _load_if_needed(self, force=False):
        stat = self._current_stat()
        if not force and stat is not None and stat == self._stat:
            return
        self._stat = stat
        if stat is None:
            self._config = None
            self._error = f"Config file not found: {self.path}"
            return
        try:
            self._config = load_dashboard_from_file(self.path)
            self._error = None
        except (yaml.YAMLError, ConfigValidationError, OSError) as exc:
            self._config = None
            self._error = f"Could not load config from {self.path}: {exc}"

    def reload(self):
        """Force a reload, discarding the cached stat check."""
        self._load_if_needed(force=True)

    def get(self):
        """Return (config, error). Config is DashboardConfig or None; error is a
        human-readable string or None."""
        self._load_if_needed()
        return self._config, self._error

    def editor_enabled(self):
        """Return True only when the config explicitly sets the edit flag to true.

        Default-deny (spec FR-010): absent, non-boolean, or false values never
        enable editing. The flag is part of the same config but is read from the
        raw YAML because parse_dashboard intentionally ignores unknown top-level
        keys.
        """
        raw = _read_raw_config(self.path)
        if raw is None:
            return False
        try:
            data = yaml.safe_load(raw)
        except yaml.YAMLError:
            return False
        if not isinstance(data, dict):
            return False
        for key in _EDITOR_KEYS:
            value = data.get(key)
            if isinstance(value, bool) and value is True:
                return True
        return False
