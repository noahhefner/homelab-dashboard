import os
import time
from pathlib import Path

import yaml

from app.config import ConfigLoader


def _write(path, data):
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def _bump_mtime(path):
    st = path.stat()
    os.utime(path, (st.st_atime_ns / 1e9, st.st_mtime_ns / 1e9 + 2.0))


def test_loader_returns_cached_config_when_file_unchanged(tmp_path):
    cfg = tmp_path / "config.yaml"
    _write(cfg, {"services": []})
    loader = ConfigLoader(str(cfg))

    config, error = loader.get()
    assert error is None

    # No file modification -> returns same (cached) config object
    config2, _ = loader.get()
    assert config2 is config


def test_loader_reloads_on_file_change(tmp_path):
    cfg = tmp_path / "config.yaml"
    _write(cfg, {"services": [{"name": "A", "url": "https://a.lan"}]})
    loader = ConfigLoader(str(cfg))
    config, _ = loader.get()
    assert len(config.services) == 1

    _write(cfg, {
        "services": [
            {"name": "A", "url": "https://a.lan"},
            {"name": "B", "url": "https://b.lan"},
        ]
    })
    _bump_mtime(cfg)
    time.sleep(0.01)

    reloaded, error = loader.get()
    assert error is None
    assert len(reloaded.services) == 2


def test_loader_force_reload(tmp_path):
    cfg = tmp_path / "config.yaml"
    _write(cfg, {"services": []})
    loader = ConfigLoader(str(cfg))
    assert len(loader.get()[0].services) == 0

    _write(cfg, {"services": [{"name": "X", "url": "https://x.lan"}]})
    loader.reload()
    assert len(loader.get()[0].services) == 1


def test_loader_missing_file_reports_error(tmp_path):
    loader = ConfigLoader(str(tmp_path / "nope.yaml"))
    config, error = loader.get()
    assert config is None
    assert error is not None
