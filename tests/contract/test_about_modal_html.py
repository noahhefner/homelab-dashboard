from pathlib import Path

import yaml

from app import create_app
from tests.soup_utils import parse

GITHUB_URL = "https://github.com/noahhefner/homelab-dashboard"


def _write_config(tmpdir, data):
    path = Path(tmpdir) / "config.yaml"
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return str(path)


def _home_soup(tmp_path, data=None):
    data = data or {"tile_groups": []}
    app = create_app(config_path=_write_config(tmp_path, data))
    return parse(app.test_client().get("/").get_data(as_text=True))


# --- About button replaces the GitHub link (feature-013 / US1) -------------


def test_about_button_replaces_github_anchor(tmp_path):
    soup = _home_soup(tmp_path)

    button = soup.select_one('button[data-bs-target="#about-modal"]')
    assert button is not None
    assert button.name == "button"
    assert button.get("href") is None
    classes = button.get("class") or []
    assert "about-toggle" in classes
    assert button.get("data-bs-toggle") == "modal"
    assert button.get("aria-label") == "About"

    icon = button.select_one("i.bi-info-circle")
    assert icon is not None
    assert icon.get("aria-hidden") == "true"


def test_no_github_link_remains_in_homepage_navbar(tmp_path):
    soup = _home_soup(tmp_path)

    assert soup.select_one("a.github-link") is None
    assert soup.select_one("i.bi-github") is None


def test_modal_honors_dialog_markup_contract(tmp_path):
    soup = _home_soup(tmp_path)

    modal = soup.select_one("#about-modal")
    assert modal is not None
    assert "modal" in (modal.get("class") or [])
    assert "fade" in (modal.get("class") or [])
    assert modal.get("tabindex") == "-1"
    assert modal.get("aria-labelledby") == "about-modal-title"
    assert modal.get("aria-hidden") == "true"

    title = soup.select_one("#about-modal-title")
    assert title is not None

    dialog = soup.select_one(".modal-dialog")
    assert dialog is not None
    dialog_classes = dialog.get("class") or []
    assert "modal-dialog-centered" in dialog_classes
    assert "modal-dialog-scrollable" in dialog_classes


def test_gh_link_inside_modal_opens_in_new_tab_safely(tmp_path):
    soup = _home_soup(tmp_path)

    modal = soup.select_one("#about-modal")
    link = modal.select_one("a")
    assert link is not None
    assert link.get("href") == GITHUB_URL
    assert link.get("target") == "_blank"
    rel = link.get("rel") or []
    assert "noopener" in rel
    assert "noreferrer" in rel
