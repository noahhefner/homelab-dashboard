import os
import time

import yaml

from app import create_app


def _write(path, data):
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def _bump_mtime(path):
    st = path.stat()
    os.utime(path, (st.st_atime_ns / 1e9, st.st_mtime_ns / 1e9 + 2.0))


def _stale_mtime(path):
    st = path.stat()
    return path, st.st_mtime_ns


def _setup(path, data):
    _write(path, data)
    return create_app(config_path=str(path))


def _editor_config(extra_services=None, title="Homelab"):
    cfg = {"editor": True, "title": title}
    if extra_services:
        cfg["services"] = extra_services
    else:
        cfg["services"] = []
    return cfg


# --- US3: save -> reflected by dashboard ---


def test_save_reflected_on_next_request(tmp_path):
    cfg = tmp_path / "config.yaml"
    app = _setup(cfg, _editor_config(title="Before"))
    client = app.test_client()

    assert "Before" in client.get("/").get_data(as_text=True)

    resp = client.post(
        "/config/save",
        json={"content": "editor: true\ntitle: After\nservices: []\n"},
    )
    assert resp.status_code == 200

    _bump_mtime(cfg)
    time.sleep(0.01)
    html = client.get("/").get_data(as_text=True)
    assert "After" in html
    assert "Before" not in html


def test_save_round_trips_exact_bytes(tmp_path):
    cfg = tmp_path / "config.yaml"
    app = _setup(cfg, _editor_config())
    client = app.test_client()

    content = (
        "editor: true\n"
        "title: Homelab\n"
        "\n"
        "# comment preserved \n"
        "services:\n"
        "  - name: \"Plex\"\n"
        "    url: https://plex.lan\n"
    )
    resp = client.post("/config/save", json={"content": content})
    assert resp.status_code == 200

    _bump_mtime(cfg)
    time.sleep(0.01)
    html = client.get("/config").get_data(as_text=True)
    # The rendered page contains the exact text (no reformatting); quotes are
    # HTML-escaped for injection safety (FR-009).
    assert "comment preserved" in html
    assert "&#34;Plex&#34;" in html


# --- validation before write ---


def test_malformed_save_leaves_prior_config_intact(tmp_path):
    cfg = tmp_path / "config.yaml"
    app = _setup(cfg, _editor_config(title="Good"))
    client = app.test_client()
    original = cfg.read_text(encoding="utf-8")

    resp = client.post("/config/save", json={"content": "services:\n  - name: [oops"})
    assert resp.status_code == 400
    assert cfg.read_text(encoding="utf-8") == original

    _bump_mtime(cfg)
    time.sleep(0.01)
    html = client.get("/").get_data(as_text=True)
    assert "Good" in html


def test_format_violation_save_changes_nothing(tmp_path):
    cfg = tmp_path / "config.yaml"
    app = _setup(cfg, _editor_config(title="Good"))
    client = app.test_client()
    original = cfg.read_text(encoding="utf-8")

    resp = client.post(
        "/config/save",
        json={"content": "editor: true\ntitle: New\nservices: \"not-a-list\"\n"},
    )
    assert resp.status_code == 400
    assert cfg.read_text(encoding="utf-8") == original


def test_write_failure_returns_500_and_preserves_file(tmp_path):
    if os.geteuid() == 0:
        # Permission-based read-only is bypassed when running as root.
        return
    cfg = tmp_path / "config.yaml"
    app = _setup(cfg, _editor_config(title="Good"))
    client = app.test_client()
    original = cfg.read_text(encoding="utf-8")

    os.chmod(tmp_path, 0o500)

    try:
        resp = client.post(
            "/config/save",
            json={"content": "editor: true\ntitle: New\nservices: []\n"},
        )
        assert resp.status_code == 500
        assert cfg.read_text(encoding="utf-8") == original
    finally:
        os.chmod(tmp_path, 0o700)


# --- US1 view / US5 disabled ---


def test_get_config_renders_current_yaml(tmp_path):
    cfg = tmp_path / "config.yaml"
    app = _setup(cfg, _editor_config())
    client = app.test_client()

    html = client.get("/config").get_data(as_text=True)
    assert "config-editor" in html  # editing enabled -> textarea present
    assert "services: []" in html


def test_config_error_page_when_file_missing(tmp_path):
    cfg = tmp_path / "missing.yaml"
    app = _setup(cfg, _editor_config())
    cfg.unlink()
    client = app.test_client()

    html = client.get("/config").get_data(as_text=True)
    assert "Unable to load the configuration" in html


def test_homepage_links_to_config_when_editing_enabled(tmp_path):
    cfg = tmp_path / "config.yaml"
    app = _setup(cfg, _editor_config())
    client = app.test_client()

    html = client.get("/").get_data(as_text=True)
    assert "config-link" in html
    assert "Edit configuration" in html


def test_homepage_has_no_config_link_when_disabled(tmp_path):
    cfg = tmp_path / "config.yaml"
    app = _setup(cfg, {"services": []})
    client = app.test_client()

    html = client.get("/").get_data(as_text=True)
    assert "config-link" not in html
    assert "Edit configuration" not in html


# --- recovery ---


def test_save_with_stale_mtime_rejected(tmp_path):
    cfg = tmp_path / "config.yaml"
    app = _setup(cfg, _editor_config(title="Good"))
    client = app.test_client()

    _, mtime = _stale_mtime(cfg)
    # Change the file on disk after the editor was "opened" with the stale mtime.
    _write(cfg, _editor_config(title="Newer"))
    _bump_mtime(cfg)

    resp = client.post(
        "/config/save",
        json={"content": "editor: true\ntitle: Overwrite\nservices: []\n", "config_mtime": mtime},
    )
    assert resp.status_code == 409
    assert "changed on disk" in resp.get_json()["error"]


def test_save_accepts_current_mtime_as_string_like_browser(tmp_path):
    cfg = tmp_path / "config.yaml"
    app = _setup(cfg, _editor_config(title="Good"))
    client = app.test_client()

    _, mtime = _stale_mtime(cfg)
    resp = client.post(
        "/config/save",
        json={
            "content": "editor: true\ntitle: Fine\nservices: []\n",
            "config_mtime": str(mtime),
        },
    )
    assert resp.status_code == 200


def test_recover_restores_last_known_good(tmp_path):
    cfg = tmp_path / "config.yaml"
    app = _setup(cfg, _editor_config(title="Good"))
    client = app.test_client()

    client.post(
        "/config/save",
        json={"content": "editor: true\ntitle: Bad\nservices: []\n"},
    )

    resp = client.post("/config/restore")
    assert resp.status_code == 200
    restored = resp.get_json()["content"]
    assert "title: Good" in restored

    _bump_mtime(cfg)
    time.sleep(0.01)
    html = client.get("/").get_data(as_text=True)
    assert "Good" in html