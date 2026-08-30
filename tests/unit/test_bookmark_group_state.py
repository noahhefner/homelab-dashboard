from app import create_app


def test_groups_have_collapse_toggle_and_content(tmp_path):
    import yaml

    path = tmp_path / "config.yaml"
    path.write_text(
        yaml.safe_dump(
            {
                "bookmark_groups": [
                    {
                        "name": "Media",
                        "bookmarks": [{"label": "YT", "url": "https://youtube.com"}],
                    }
                ]
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    app = create_app(config_path=str(path))
    html = app.test_client().get("/").get_data(as_text=True)

    # Each group renders a Bootstrap collapse toggle button wired to a matching
    # collapse target via Bootstrap's data attributes.
    assert 'data-bs-toggle="collapse"' in html
    assert 'data-bs-target="#bookmark-collapse-1"' in html
    assert 'id="bookmark-collapse-1"' in html


def test_group_collapse_content_wired_to_target(tmp_path):
    import yaml

    path = tmp_path / "config.yaml"
    path.write_text(
        yaml.safe_dump(
            {
                "bookmark_groups": [
                    {
                        "name": "Finance",
                        "bookmarks": [{"label": "Bank", "url": "https://bank.com"}],
                    }
                ]
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    app = create_app(config_path=str(path))
    html = app.test_client().get("/").get_data(as_text=True)

    # The toggle's data-bs-target refers to the group's collapse content, and
    # the content wrapper carries the Bootstrap collapse classes.
    assert 'data-bs-target="#bookmark-collapse-1"' in html
    assert 'id="bookmark-collapse-1"' in html
    assert 'class="accordion-collapse collapse' in html
