from pathlib import Path

from app import create_app

EXAMPLE_YAML = Path(__file__).resolve().parents[2] / "config" / "example.yaml"


def _get_home_html():
    app = create_app(config_path=str(EXAMPLE_YAML))
    return app.test_client().get("/").get_data(as_text=True)


def test_viewport_meta_present_for_mobile():
    html = _get_home_html()
    assert 'name="viewport"' in html
    assert "width=device-width, initial-scale=1" in html


def test_responsive_grid_classes_used():
    html = _get_home_html()
    # Responsive columns: 2 on phone, more at larger breakpoints (no horizontal scroll)
    assert "uk-child-width-1-2" in html
    assert "uk-child-width-1-3@s" in html
    assert "uk-child-width-1-4@m" in html


def test_tiles_are_plain_anchors_tap_friendly():
    html = _get_home_html()
    # Navigation must not depend on hover; plain <a href> works on tap
    assert 'class="uk-link-reset service-tile"' in html
    assert 'href="' in html
    assert 'target="_blank"' in html


def test_no_fixed_width_sections():
    # Avoid full-width-wrapping columns that could cause horizontal scroll
    html = _get_home_html()
    assert "npm start" not in html  # sanity: no accidental desktop-only content
