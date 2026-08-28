from pathlib import Path

from app import create_app

APP_JS = Path(__file__).resolve().parents[2] / "app" / "static" / "app.js"


def _group_toggle_markup(data, client):
    return client.get("/").get_data(as_text=True)


def test_groups_have_toggle_buttons(tmp_path):
    import yaml

    path = tmp_path / "config.yaml"
    path.write_text(
        yaml.safe_dump(
            {"bookmark_groups": [{"name": "Media", "bookmarks": [
                {"label": "YT", "url": "https://youtube.com"}]}]},
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    app = create_app(config_path=str(path))
    html = app.test_client().get("/").get_data(as_text=True)

    # A toggle button/control and an associated content wrapper are rendered
    assert "data-group-toggle" in html
    assert "data-group-content" in html


def test_groups_have_stable_state_key(tmp_path):
    import yaml

    path = tmp_path / "config.yaml"
    path.write_text(
        yaml.safe_dump(
            {"bookmark_groups": [{"name": "Finance", "bookmarks": [
                {"label": "Bank", "url": "https://bank.com"}]}]},
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    app = create_app(config_path=str(path))
    html = app.test_client().get("/").get_data(as_text=True)

    # The JS persists state keyed by a stable group identifier so it survives
    # across renames/refreshes.
    assert 'data-group-id="Finance"' in html


def test_app_js_implements_localstorage_persistence():
    source = APP_JS.read_text(encoding="utf-8")
    # Group state persists across visits via localStorage.
    assert "localStorage" in source
    # The toggle is wired via data attributes consumed by the JS.
    assert "data-group-toggle" in source
    # The collapse target is resolved from the toggle's data-bs-target.
    assert "data-bs-target" in source
    # Bootstrap Collapse drives show/hide; its events persist state.
    assert "bootstrap.Collapse" in source
    assert "show.bs.collapse" in source
    assert "hide.bs.collapse" in source
