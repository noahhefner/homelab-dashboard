import yaml

from app import create_app


def _write(path, data):
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def _setup_config(path, filename, data, editor=True):
    cfg = path / filename
    _write(cfg, data)
    return cfg, create_app(config_path=str(cfg))


def _download_config(editor=True):
    return {"editor": editor, "title": "Homelab", "tiles": []}


# --- US1: GET /config/download ---


def test_download_returns_exact_bytes_and_filename(tmp_path):
    content = (
        "title: Homelab\n"
        "\n"
        "# comment preserved \n"
        "tiles:\n"
        '  - name: "Plex"\n'
        "    url: https://plex.lan\n"
    )
    cfg = tmp_path / "site.yaml"
    cfg.write_text(content, encoding="utf-8")
    app = create_app(config_path=str(cfg))
    client = app.test_client()

    resp = client.get("/config/download")

    assert resp.status_code == 200
    assert resp.data.decode("utf-8") == content
    disposition = resp.headers.get("Content-Disposition", "")
    assert 'attachment; filename="site.yaml"' in disposition


def test_download_works_when_editing_disabled(tmp_path):
    content = "title: Homelab\ntiles: []\n"
    cfg = tmp_path / "config.yaml"
    cfg.write_text(content, encoding="utf-8")
    app = create_app(config_path=str(cfg))
    client = app.test_client()

    resp = client.get("/config/download")

    assert resp.status_code == 200
    assert resp.data.decode("utf-8") == content


def test_download_matches_on_disk_bytes_byte_for_byte(tmp_path):
    content = "title: Homelab\n\ntiles:\n  - name: Emby\n    url: https://emby.lan\n"
    cfg = tmp_path / "lab.yaml"
    cfg.write_text(content, encoding="utf-8")
    app = create_app(config_path=str(cfg))
    client = app.test_client()

    resp = client.get("/config/download")

    assert resp.status_code == 200
    assert resp.data == cfg.read_bytes()


# --- US1: unreadable config ---


def test_download_returns_error_when_config_unreadable(tmp_path):
    cfg = tmp_path / "missing.yaml"
    app = create_app(config_path=str(cfg))
    client = app.test_client()

    resp = client.get("/config/download")

    assert resp.status_code != 200
    # Never an empty 200 attachment.
    assert resp.data != b""


# --- US2: icon source links ---


def test_config_page_renders_icon_source_links_editing(tmp_path):
    cfg = tmp_path / "config.yaml"
    _write(cfg, _download_config(editor=True))
    app = create_app(config_path=str(cfg))
    client = app.test_client()

    html = client.get("/config").get_data(as_text=True)
    assert "Icon sources" in html
    assert "dashboardicons.com" in html
    assert "homarr-labs/dashboard-icons" in html


def test_config_page_renders_icon_source_links_readonly(tmp_path):
    cfg = tmp_path / "config.yaml"
    _write(cfg, _download_config(editor=False))
    app = create_app(config_path=str(cfg))
    client = app.test_client()

    html = client.get("/config").get_data(as_text=True)
    assert "Icon sources" in html
    assert "dashboardicons.com" in html
    assert "homarr-labs/dashboard-icons" in html


def test_icon_links_open_new_tab_safely(tmp_path):
    cfg = tmp_path / "config.yaml"
    _write(cfg, _download_config(editor=True))
    app = create_app(config_path=str(cfg))
    client = app.test_client()

    html = client.get("/config").get_data(as_text=True)
    assert 'target="_blank"' in html
    assert 'rel="noopener noreferrer"' in html


# --- US1: download button rendered in both modes ---


def test_download_button_rendered_in_both_modes(tmp_path):
    for editor in (True, False):
        cfg = tmp_path / "config.yaml"
        _write(cfg, _download_config(editor=editor))
        app = create_app(config_path=str(cfg))
        client = app.test_client()
        html = client.get("/config").get_data(as_text=True)
        assert "Download config" in html
