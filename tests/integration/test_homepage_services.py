from pathlib import Path

import yaml

from app import create_app

EXAMPLE_YAML = Path(__file__).resolve().parents[2] / "config" / "example.yaml"


def test_homepage_renders_all_example_services():
    with open(EXAMPLE_YAML, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    app = create_app(config_path=str(EXAMPLE_YAML))
    html = app.test_client().get("/").get_data(as_text=True)

    configured_names = [s["name"] for s in data.get("services", [])]
    assert configured_names, "example config should have services"
    for name in configured_names:
        assert name in html
