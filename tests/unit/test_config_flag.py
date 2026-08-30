import yaml

from app import create_app
from app.config import ConfigLoader


def _write(path, data):
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def test_editor_disabled_by_default(tmp_path):
    cfg = tmp_path / "config.yaml"
    _write(cfg, {"services": [{"name": "One", "url": "https://one.lan"}]})
    loader = ConfigLoader(str(cfg))
    assert loader.editor_enabled() is False


def test_editor_disabled_when_flag_absent(tmp_path):
    cfg = tmp_path / "config.yaml"
    _write(cfg, {"services": []})
    loader = ConfigLoader(str(cfg))
    assert loader.editor_enabled() is False


def test_editor_enabled_when_flag_true(tmp_path):
    cfg = tmp_path / "config.yaml"
    _write(cfg, {"editor": True, "services": []})
    loader = ConfigLoader(str(cfg))
    assert loader.editor_enabled() is True


def test_editor_disabled_when_flag_false(tmp_path):
    cfg = tmp_path / "config.yaml"
    _write(cfg, {"editor": False, "services": []})
    loader = ConfigLoader(str(cfg))
    assert loader.editor_enabled() is False


def test_editor_disabled_when_flag_non_boolean(tmp_path):
    cfg = tmp_path / "config.yaml"
    _write(cfg, {"editor": "yes", "services": []})
    loader = ConfigLoader(str(cfg))
    assert loader.editor_enabled() is False


def test_editor_enabled_when_edit_config_alias_true(tmp_path):
    cfg = tmp_path / "config.yaml"
    _write(cfg, {"edit_config": True, "services": []})
    loader = ConfigLoader(str(cfg))
    assert loader.editor_enabled() is True


def test_get_config_read_only_when_disabled(tmp_path):
    cfg = tmp_path / "config.yaml"
    _write(cfg, {"services": [{"name": "One", "url": "https://one.lan"}]})
    app = create_app(config_path=str(cfg))
    client = app.test_client()

    html = client.get("/config").get_data(as_text=True)
    assert "config-editor" not in html
    assert "save-config" not in html
    assert "Editing is disabled" in html


def test_save_returns_403_when_disabled(tmp_path):
    cfg = tmp_path / "config.yaml"
    _write(cfg, {"services": [{"name": "One", "url": "https://one.lan"}]})
    original = cfg.read_text(encoding="utf-8")
    app = create_app(config_path=str(cfg))
    client = app.test_client()

    resp = client.post("/config/save", json={"content": "title: Changed\nservices: []\n"})
    assert resp.status_code == 403
    assert "disabled" in resp.get_json()["error"].lower()
    assert cfg.read_text(encoding="utf-8") == original


def test_save_empty_content_returns_400_when_enabled(tmp_path):
    cfg = tmp_path / "config.yaml"
    _write(cfg, {"editor": True, "services": []})
    app = create_app(config_path=str(cfg))
    client = app.test_client()

    resp = client.post("/config/save", json={"content": ""})
    assert resp.status_code == 400