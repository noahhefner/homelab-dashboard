import tempfile
from pathlib import Path

import pytest
import yaml

from app import create_app


def _write_config(tmpdir, data):
    path = Path(tmpdir) / "config.yaml"
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return str(path)


@pytest.fixture
def client_with_services(tmpdir):
    data = {
        "title": "Test Lab",
        "services": [
            {"name": "Plex", "url": "https://plex.lan:32400", "icon": "https://cdn.example.com/plex.png"},
            {"name": "Nextcloud", "url": "https://cloud.lan", "icon": "nextcloud"},
            {"name": "<script>alert('x')</script>", "url": "https://unsafe.lan"},
        ],
    }
    app = create_app(config_path=_write_config(tmpdir, data))
    return app.test_client()


def test_services_render_name_and_url(client_with_services):
    resp = client_with_services.get("/")
    html = resp.get_data(as_text=True)
    assert resp.status_code == 200
    assert "Plex" in html
    assert "https://plex.lan:32400" in html
    assert "Nextcloud" in html


def test_service_with_icon_url_renders_img(client_with_services):
    html = client_with_services.get("/").get_data(as_text=True)
    assert "https://cdn.example.com/plex.png" in html


def test_service_without_url_icon_renders_monogram(client_with_services):
    html = client_with_services.get("/").get_data(as_text=True)
    # 'N' is the first letter of Nextcloud, which lacks a URL icon -> monogram
    assert "N" in html


def test_service_names_are_html_escaped(client_with_services):
    html = client_with_services.get("/").get_data(as_text=True)
    assert "<script>alert('x')</script>" not in html
    assert "&lt;script&gt;" in html and "&lt;/script&gt;" in html


def test_service_links_open_in_new_tab(client_with_services):
    html = client_with_services.get("/").get_data(as_text=True)
    assert "target=\"_blank\"" in html
    assert "noopener" in html


# --- Service logos: any remote URL renders as a logo image (US1) ------------

def test_service_with_any_remote_url_icon_renders_img_logo(tmpdir):
    url = "https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/svg/plex.svg"
    data = {
        "services": [
            {"name": "Plex", "url": "https://plex.lan:32400", "icon": url},
        ]
    }
    app = create_app(config_path=_write_config(tmpdir, data))
    html = app.test_client().get("/").get_data(as_text=True)
    # Any arbitrary https URL is rendered as an <img> logo, not a monogram.
    assert '<img src="%s"' % url in html
    assert "service-icon" in html


def test_non_url_icon_renders_monogram_not_img(tmpdir):
    data = {
        "services": [
            {"name": "Nextcloud", "url": "https://cloud.lan", "icon": "nextcloud"},
        ]
    }
    app = create_app(config_path=_write_config(tmpdir, data))
    html = app.test_client().get("/").get_data(as_text=True)
    # A plain-word (non-URL) icon must NOT become an <img src>; it shows a monogram.
    assert 'src="nextcloud"' not in html
    assert '<span class="service-monogram">N</span>' in html


def test_unsafe_icon_value_not_rendered_as_img_src(tmpdir):
    data = {
        "services": [
            {"name": "Unsafe", "url": "https://unsafe.lan", "icon": "javascript:alert(1)"},
        ]
    }
    app = create_app(config_path=_write_config(tmpdir, data))
    html = app.test_client().get("/").get_data(as_text=True)
    # Unsafe / non-http(s) icon values are never emitted as an image source.
    assert 'src="javascript:' not in html
    assert '<span class="service-monogram">U</span>' in html
