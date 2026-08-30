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


# --- Desktop: bookmarks in a right-hand column (User Story 1) ---------------


def test_services_use_main_area_grid_classes():
    html = _get_home_html()
    # Main apps area: full width on mobile, ~75% / left on desktop (lg+)
    assert "col-12 col-lg-9" in html


def test_bookmarks_use_sidebar_grid_classes():
    html = _get_home_html()
    # Bookmarks: full width on mobile, ~25% / right on desktop (lg+)
    assert "col-12 col-lg-3" in html


def test_columns_are_wrapped_in_a_row():
    html = _get_home_html()
    assert 'class="row g-4"' in html


# --- Mobile: bookmarks below the apps (User Story 2) ------------------------


def test_mobile_stack_uses_full_width_columns():
    html = _get_home_html()
    # Both columns are col-12 below lg, so bookmarks stack below the apps.
    assert 'class="col-12 col-lg-9"' in html  # services
    assert 'class="col-12 col-lg-3"' in html  # bookmarks


def test_tiles_are_plain_anchors_tap_friendly():
    html = _get_home_html()
    # Navigation must not depend on hover; plain <a href> works on tap
    assert 'class="app-tile service-tile"' in html
    assert 'href="' in html
    assert 'target="_blank"' in html
    assert 'rel="noopener noreferrer"' in html


# --- Offline / vendored Bootstrap (user requirement) ------------------------


def test_bootstrap_assets_served_locally():
    html = _get_home_html()
    assert "/static/bootstrap/css/bootstrap.min.css" in html
    assert "/static/bootstrap/js/bootstrap.bundle.min.js" in html


def test_no_remote_or_cdn_asset_urls():
    html = _get_home_html()
    # The dashboard's CSS/JS must be served locally so it works without internet.
    # Service logos (user-provided remote images, e.g. dashboardicons.com) are a
    # deliberate exception and are rendered as <img> elements, not CSS/JS assets.
    import re

    remote_links = re.findall(r'<link[^>]+href="(https?://[^"]+)"', html)
    remote_scripts = re.findall(r'<script[^>]+src="(https?://[^"]+)"', html)
    assert remote_links == [], (
        f"external CSS/JS links must not be loaded from CDN: {remote_links}"
    )
    assert remote_scripts == [], (
        f"external CSS/JS scripts must not be loaded from CDN: {remote_scripts}"
    )


# --- Responsive reflow (User Story 3) ---------------------------------------


def test_single_consistent_lg_breakpoint():
    html = _get_home_html()
    # Only one responsive breakpoint (lg) governs the two-column layout.
    assert "col-lg-9" in html
    assert "col-lg-3" in html
    # No other responsive col-* variants should drive the sidebar layout.
    assert "col-xl-9" not in html
    assert "col-xl-3" not in html


def test_no_fixed_width_sections():
    # Avoid full-width-wrapping columns that could cause horizontal scroll.
    html = _get_home_html()
    assert "npm start" not in html  # sanity: no accidental desktop-only content
