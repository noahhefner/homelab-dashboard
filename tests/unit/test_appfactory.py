import os
import tempfile

import pytest

from app import create_app
from app.config import DEFAULT_CONFIG_PATH


def test_create_app_sets_default_config_path():
    with tempfile.TemporaryDirectory() as tmp:
        os.environ.pop("CONFIG_PATH", None)
        app = create_app()
        assert app is not None
        assert app.config["CONFIG_PATH"] == DEFAULT_CONFIG_PATH


def test_create_app_uses_explicit_config_path():
    app = create_app(config_path="/tmp/custom/config.yaml")
    assert app.config["CONFIG_PATH"] == "/tmp/custom/config.yaml"


def test_create_app_uses_env_config_path():
    os.environ["CONFIG_PATH"] = "/tmp/env/config.yaml"
    try:
        app = create_app()
        assert app.config["CONFIG_PATH"] == "/tmp/env/config.yaml"
    finally:
        os.environ.pop("CONFIG_PATH", None)


def test_create_app_registers_routes():
    app = create_app(config_path="/tmp/custom/config.yaml")
    client = app.test_client()
    # Health route registered on foundation
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.data.rstrip() in (b"OK", b"ok")
