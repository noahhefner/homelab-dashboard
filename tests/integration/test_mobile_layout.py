from pathlib import Path

from app import create_app
from tests.soup_utils import parse

EXAMPLE_YAML = Path(__file__).resolve().parents[2] / "tests" / "static" / "test-config.yaml"


def _get_home_soup():
    app = create_app(config_path=str(EXAMPLE_YAML))
    return parse(app.test_client().get("/").get_data(as_text=True))


def test_viewport_meta_present_for_mobile():
    soup = _get_home_soup()
    viewport = soup.select_one('meta[name="viewport"]')
    assert viewport is not None
    assert viewport.get("content") == "width=device-width, initial-scale=1"


# --- Desktop: bookmarks in a right-hand column (User Story 1) ---------------


def test_tiles_use_main_area_grid_classes():
    soup = _get_home_soup()
    # Main apps area: full width on mobile, ~75% / left on desktop (lg+)
    tiles = soup.select_one('section[aria-label="Tiles"]')
    assert tiles is not None
    classes = tiles.get("class") or []
    assert "col-12" in classes
    assert "col-lg-9" in classes


def test_bookmarks_use_sidebar_grid_classes():
    soup = _get_home_soup()
    # Bookmarks: full width on mobile, ~25% / right on desktop (lg+)
    bookmarks = soup.select_one('aside[aria-label="Bookmarks"]')
    assert bookmarks is not None
    classes = bookmarks.get("class") or []
    assert "col-12" in classes
    assert "col-lg-3" in classes


def test_columns_are_wrapped_in_a_row():
    soup = _get_home_soup()
    assert soup.select_one(".row.g-4") is not None


# --- Mobile: bookmarks below the apps (User Story 2) ------------------------


def test_mobile_stack_uses_full_width_columns():
    soup = _get_home_soup()
    # Both columns are col-12 below lg, so bookmarks stack below the apps.
    tiles = soup.select_one('section[aria-label="Tiles"]')
    bookmarks = soup.select_one('aside[aria-label="Bookmarks"]')
    assert "col-12" in (tiles.get("class") or [])
    assert "col-12" in (bookmarks.get("class") or [])


def test_tiles_are_plain_anchors_tap_friendly():
    soup = _get_home_soup()
    # Navigation must not depend on hover; plain <a href> works on tap
    tile = soup.select_one("a.app-tile.tile")
    assert tile is not None
    assert tile.get("href")
    assert tile.get("target") == "_blank"
    rel = tile.get("rel") or []
    assert "noopener" in rel
    assert "noreferrer" in rel


# --- Offline frontend assets (user requirement) -----------------------------


def test_no_remote_or_cdn_asset_urls():
    soup = _get_home_soup()
    # The dashboard's CSS/JS must be served locally so it works without internet.
    # Tile logos (user-provided remote images, e.g. dashboardicons.com) are a
    # deliberate exception and are rendered as <img> elements, not CSS/JS assets.
    remote_links = [
        link.get("href")
        for link in soup.find_all("link")
        if (link.get("href") or "").startswith(("http://", "https://"))
    ]
    remote_scripts = [
        s.get("src")
        for s in soup.find_all("script")
        if (s.get("src") or "").startswith(("http://", "https://"))
    ]
    assert remote_links == [], (
        f"external CSS/JS links must not be loaded from CDN: {remote_links}"
    )
    assert remote_scripts == [], (
        f"external CSS/JS scripts must not be loaded from CDN: {remote_scripts}"
    )


# --- Responsive reflow (User Story 3) ---------------------------------------


def test_single_consistent_lg_breakpoint():
    soup = _get_home_soup()
    # Only one responsive breakpoint (lg) governs the two-column layout.
    tiles = soup.select_one('section[aria-label="Tiles"]')
    bookmarks = soup.select_one('aside[aria-label="Bookmarks"]')
    assert "col-lg-9" in (tiles.get("class") or [])
    assert "col-lg-3" in (bookmarks.get("class") or [])
    # No other responsive col-* variants should drive the sidebar layout.
    all_classes = [" ".join(el.get("class") or []) for el in soup.find_all(class_=True)]
    assert not any("col-xl-9" in c for c in all_classes)
    assert not any("col-xl-3" in c for c in all_classes)


# --- Header search bar hidden on mobile (feature-011) ------------------------


def test_search_bar_hidden_on_mobile_via_responsive_utilities():
    soup = _get_home_soup()
    # The search form (and its icon) are hidden below the md breakpoint and
    # shown at md+ via Bootstrap responsive display utilities (FR-011/FR-015).
    form = soup.select_one("form")
    assert form is not None
    classes = form.get("class") or []
    assert any(c.startswith("d-none") for c in classes)
    assert any("d-md" in c for c in classes)
