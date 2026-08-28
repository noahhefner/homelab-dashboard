# Homelab Dashboard

A self-hosted, single-page dashboard homepage for your home server. It renders your
services and grouped bookmarks from one YAML file, served by a small Flask app inside a
single Docker container. No database, no authentication — just config.

## Features

- **Services**: clickable tiles that open in a new tab (icon image or monogram fallback).
- **Bookmark groups**: named groups with collapsible/expandable bookmarks; collapsed state
  persists across visits via `localStorage`.
- **Live reload**: edit the YAML file and refresh the browser — no restart needed.
- **Mobile responsive**: reflows to no-horizontal-scroll layout on phones; tap-friendly.
- **One config file**: everything is defined in a single YAML document.

## Requirements

- Python 3.14+ and [`uv`](https://docs.astral.sh/uv/) for local development,
  **or** Docker for running the container.
- **Node.js (≥18) and [pnpm](https://pnpm.io/)** to provision the Bootstrap
  assets. Install pnpm once if missing: `npm install -g pnpm`, or use Corepack
  (`corepack enable`). Node/pnpm are developer/build tooling only — they are not
  needed to run the deployed container.

## Configuration

Everything is configured in [`config/example.yaml`](config/example.yaml):

```yaml
title: "Home Lab"

services:
  - name: Plex
    url: "https://plex.lan:32400"
    icon: "https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/svg/plex.svg"  # logo; a monogram is shown when absent/invalid

bookmark_groups:
  - name: Media
    icon: play      # optional
    bookmarks:
      - label: YouTube
        url: "https://www.youtube.com"
      - label: Spotify
        url: "https://open.spotify.com"
```

- `icon` is treated as an image URL if it is a valid `http(s)` URL; otherwise the first
  letter of the name is shown as a monogram.
- When `CONFIG_PATH` is unset, it defaults to `config/example.yaml` (relative to the
  working directory).

## Service Logos

Each service can show a recognizable **logo** by setting its `icon` to any valid remote
image URL — no local files or committed binaries required. The example config uses
logos from [dashboardicons.com](https://dashboardicons.com/), a convenient, curated
source of service logos (direct assets use the jsDelivr pattern
`https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/svg/<name>.svg`).

- Any `http(s)` image URL works as a logo (e.g., your own CDN or static host).
- If a logo is absent, not a valid URL, or fails to load, the tile shows a monogram
  (first letter of the service name) — the page never breaks.
- To change a logo, edit the `icon` URL and refresh; no rebuild or restart is needed.

```yaml
services:
  - name: Plex
    url: "https://plex.lan:32400"
    icon: "https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/svg/plex.svg"
```

## Bootstrap Assets

The Bootstrap CSS/JS are **not** committed to source control. They are tracked as a
dependency in [`package.json`](package.json) (pinned version) with `pnpm`, and
provisioned into `app/static/bootstrap/` by copying the compiled files from the
installed package.

Provision on a fresh checkout:

```bash
pnpm setup        # = pnpm install && pnpm provision
```

After provisioning, `app/static/bootstrap/css/bootstrap.min.css` and
`app/static/bootstrap/js/bootstrap.bundle.min.js` exist and the page is styled.

To **update the Bootstrap version**:

```bash
pnpm add bootstrap@X.Y.Z   # updates package.json + pnpm-lock.yaml
pnpm provision             # replaces the assets with the new version
```

The manifest (`package.json`) and lockfile (`pnpm-lock.yaml`) are tracked; the
downloaded assets (`node_modules/`, `app/static/bootstrap/`) are gitignored.

## Local Run (Development)

```bash
uv sync
export CONFIG_PATH=config/example.yaml
uv run -m app.server
```

Open <http://localhost:5000>. Edit `config/example.yaml`, save, and refresh to see changes.

## Docker Run (single container)

```bash
docker build -t homelab-dashboard .
docker run --rm -p 5000:5000 \
  -v "$PWD/config/example.yaml:/app/config/example.yaml:ro" \
  homelab-dashboard
```

The image bundles `config/example.yaml` by default, so a bare `docker run -p 5000:5000
homelab-dashboard` works out of the box. Mounting your own file over it (as above) lets
you edit the config on the host and see changes on refresh.

## Docker Compose

```bash
docker compose up --build
```

The compose file mounts `./config/example.yaml` into the container read-only. Edit the
host file and refresh the browser — no container restart required.

## Tests

```bash
uv run pytest
```

Runs the contract, unit, and integration suites (config validation, parsing, live reload,
rendering, bookmark groups, and mobile layout).
