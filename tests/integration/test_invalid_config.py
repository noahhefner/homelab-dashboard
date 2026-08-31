from app import create_app


def test_invalid_yaml_renders_error_page(tmp_path):
    cfg = tmp_path / "config.yaml"
    cfg.write_text("tiles:\n  - name: [broken", encoding="utf-8")

    app = create_app(config_path=str(cfg))
    resp = app.test_client().get("/")

    html = resp.get_data(as_text=True)
    assert resp.status_code == 200
    assert "Configuration Error" in html


def test_missing_required_field_renders_error_page(tmp_path):
    cfg = tmp_path / "config.yaml"
    cfg.write_text("tiles:\n  - url: https://example.com\n", encoding="utf-8")

    app = create_app(config_path=str(cfg))
    html = app.test_client().get("/").get_data(as_text=True)
    assert "Configuration Error" in html


def test_missing_file_renders_error_page(tmp_path):
    missing = tmp_path / "missing.yaml"
    app = create_app(config_path=str(missing))
    html = app.test_client().get("/").get_data(as_text=True)
    assert "Configuration Error" in html
