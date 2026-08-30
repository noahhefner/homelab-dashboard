import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
ASSET_CSS = Path("app/static/bootstrap/css/bootstrap.min.css")
ASSET_JS = Path("app/static/bootstrap/js/bootstrap.bundle.min.js")
ICONS_CSS = Path("app/static/bootstrap-icons/bootstrap-icons.min.css")
ICONS_FONT_WOFF2 = Path("app/static/bootstrap-icons/fonts/bootstrap-icons.woff2")
ICONS_FONT_WOFF = Path("app/static/bootstrap-icons/fonts/bootstrap-icons.woff")


@pytest.fixture(scope="module")
def provisioned():
    """Run the provisioning command, returning the repo root."""
    result = subprocess.run(
        ["pnpm", "provision"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    return ROOT


# --- US1: provisioning correctness ------------------------------------------


def test_provisioned_assets_exist(provisioned):
    assert (ROOT / ASSET_CSS).is_file()
    assert (ROOT / ASSET_JS).is_file()
    assert (ROOT / ICONS_CSS).is_file()
    assert (ROOT / ICONS_FONT_WOFF2).is_file()
    assert (ROOT / ICONS_FONT_WOFF).is_file()


# --- US2: declarative, pinned version ---------------------------------------


def test_reprovision_is_idempotent(provisioned):
    first_css = (ROOT / ASSET_CSS).read_bytes()
    result = subprocess.run(
        ["pnpm", "provision"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert (ROOT / ASSET_CSS).read_bytes() == first_css
    assert (ROOT / ASSET_JS).is_file()
    assert (ROOT / ICONS_CSS).is_file()
    assert (ROOT / ICONS_FONT_WOFF2).is_file()


# --- US3: assets stay out of version control --------------------------------


def test_provisioned_assets_are_gitignored(provisioned):
    checks = subprocess.run(
        ["git", "check-ignore", str(ROOT / ASSET_CSS)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    assert checks.returncode == 0, "expected the CSS asset to be gitignored"

    icons_checks = subprocess.run(
        ["git", "check-ignore", str(ROOT / ICONS_CSS)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    assert icons_checks.returncode == 0, (
        "expected the Bootstrap Icons CSS asset to be gitignored"
    )


def test_manifest_and_lockfile_are_tracked(provisioned):
    out = subprocess.run(
        ["git", "ls-files", "package.json", "pnpm-lock.yaml"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    assert "package.json" in out.stdout
    assert "pnpm-lock.yaml" in out.stdout


# --- Bootstrap Icons: pinned dependency + provisioned (feature 005) ----------


def test_bootstrap_icons_dependency_is_tracked(provisioned):
    out = subprocess.run(
        ["git", "ls-files", "package.json", "pnpm-lock.yaml"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    assert "package.json" in out.stdout
    pkg = (ROOT / "package.json").read_text()
    assert "bootstrap-icons" in pkg
