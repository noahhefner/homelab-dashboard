import yaml

from app import create_app
from tests.soup_utils import parse


def _home_soup(tmp_path, data):
    path = tmp_path / "config.yaml"
    path.write_text(
        yaml.safe_dump(data, sort_keys=False),
        encoding="utf-8",
    )
    app = create_app(config_path=str(path))
    return parse(app.test_client().get("/").get_data(as_text=True))


def test_groups_have_collapse_toggle_and_content(tmp_path):
    soup = _home_soup(
        tmp_path,
        {
            "bookmark_groups": [
                {
                    "name": "Media",
                    "bookmarks": [{"label": "YT", "url": "https://youtube.com"}],
                }
            ]
        },
    )

    # Each group renders a Bootstrap collapse toggle button wired to a matching
    # collapse target via Bootstrap's data attributes.
    button = soup.select_one("button.accordion-button")
    assert button is not None
    assert button.get("data-bs-toggle") == "collapse"
    assert button.get("data-bs-target") == "#bookmark-collapse-1"
    collapse = soup.select_one("#bookmark-collapse-1")
    assert collapse is not None
    assert "collapse" in (collapse.get("class") or [])


def test_group_collapse_content_wired_to_target(tmp_path):
    soup = _home_soup(
        tmp_path,
        {
            "bookmark_groups": [
                {
                    "name": "Finance",
                    "bookmarks": [{"label": "Bank", "url": "https://bank.com"}],
                }
            ]
        },
    )

    # The toggle's data-bs-target refers to the group's collapse content, and
    # the content wrapper carries the Bootstrap collapse classes.
    button = soup.select_one("button.accordion-button")
    assert button is not None
    assert button.get("data-bs-target") == "#bookmark-collapse-1"
    collapse = soup.select_one("#bookmark-collapse-1")
    assert collapse is not None
    classes = collapse.get("class") or []
    assert "accordion-collapse" in classes
    assert "collapse" in classes
