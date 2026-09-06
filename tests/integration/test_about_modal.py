from pathlib import Path

import yaml

from app import create_app
from tests.soup_utils import parse

GITHUB_URL = "https://github.com/noahhefner/homelab-dashboard"


def _write_config(tmpdir, data):
    path = Path(tmpdir) / "config.yaml"
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return str(path)


def _page_soup(tmp_path, data, path="/"):
    app = create_app(config_path=_write_config(tmp_path, data))
    return parse(app.test_client().get(path).get_data(as_text=True))


def _modal(soup):
    return soup.select_one("#about-modal")


def _about_button(soup):
    return soup.select_one('button[data-bs-target="#about-modal"]')


# --- Modal content (feature-013 / US1) -------------------------------------


def test_about_modal_contains_title(tmp_path):
    soup = _page_soup(tmp_path, {"tile_groups": []})

    modal = _modal(soup)
    title = modal.select_one("#about-modal-title")
    assert title is not None
    assert title.get_text(strip=True) == "About"


def test_about_modal_contains_project_blurb(tmp_path):
    soup = _page_soup(tmp_path, {"tile_groups": []})

    body = _modal(soup).get_text()
    assert "home server" in body
    assert "YAML" in body


def test_about_modal_contains_config_file_guidance(tmp_path):
    soup = _page_soup(tmp_path, {"tile_groups": []})

    body = _modal(soup).get_text()
    assert "config/example.yaml" in body
    assert "CONFIG_PATH" in body


def test_homepage_opens_with_about_button_and_modal(tmp_path):
    app = create_app(config_path=_write_config(tmp_path, {"tile_groups": []}))
    response = app.test_client().get("/")

    assert response.status_code == 200
    soup = parse(response.get_data(as_text=True))
    assert _about_button(soup) is not None
    assert _modal(soup) is not None


# --- Independence: config page + existing navbar controls (FR-012) ---------


def test_config_page_has_no_about_modal_or_button(tmp_path):
    soup = _page_soup(tmp_path, {"tile_groups": []}, path="/config")

    assert _modal(soup) is None
    assert _about_button(soup) is None


def test_existing_navbar_controls_unchanged_on_homepage(tmp_path):
    soup = _page_soup(
        tmp_path,
        {
            "tile_groups": [],
            "search_engine": "https://duckduckgo.com/?q={query}",
            "editor": True,
        },
    )

    assert soup.select_one("[data-theme-toggle]") is not None
    assert soup.select_one(".config-link") is not None
    assert soup.select_one('form input[name="q"]') is not None
    assert _about_button(soup) is not None


# --- Dismissal & UX structure (feature-013 / US2) --------------------------


def test_modal_has_close_button_with_dismiss(tmp_path):
    soup = _page_soup(tmp_path, {"tile_groups": []})

    close = _modal(soup).select_one(".modal-header .btn-close")
    assert close is not None
    assert close.get("data-bs-dismiss") == "modal"


def test_only_one_about_modal_exists(tmp_path):
    soup = _page_soup(tmp_path, {"tile_groups": []})

    assert len(soup.select("#about-modal")) == 1
    assert len(soup.select('button[data-bs-target="#about-modal"]')) == 1
