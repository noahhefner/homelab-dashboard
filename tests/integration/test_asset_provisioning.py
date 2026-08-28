import json
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
ASSET_CSS = Path("app/static/bootstrap/css/bootstrap.min.css")
ASSET_JS = Path("app/static/bootstrap/js/bootstrap.bundle.min.js")
PACKAGE_JSON = Path("package.json")


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


# --- US2: declarative, pinned version ---------------------------------------

def test_package_json_declares_pinned_bootstrap(provisioned):
    manifest = json.loads((ROOT / PACKAGE_JSON).read_text())
    version = manifest["dependencies"]["bootstrap"]
    # Pinned exact version, not a range that would float (SC-002, FR-001).
    assert version == "5.3.3"


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


# --- US3: assets stay out of version control --------------------------------

def test_provisioned_assets_are_gitignored(provisioned):
    checks = subprocess.run(
        ["git", "check-ignore", str(ROOT / ASSET_CSS)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    assert checks.returncode == 0, "expected the CSS asset to be gitignored"


def test_manifest_and_lockfile_are_tracked(provisioned):
    out = subprocess.run(
        ["git", "ls-files", "package.json", "pnpm-lock.yaml"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    assert "package.json" in out.stdout
    assert "pnpm-lock.yaml" in out.stdout
