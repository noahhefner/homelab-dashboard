# Homelab Dashboard

A self-hosted, single-page dashboard homepage for your home server. It renders your
services and grouped bookmarks from one YAML file, served by a small Flask app inside a
single Docker container. No database, no authentication — just config.

<img width="1344" height="746" alt="image" src="https://github.com/user-attachments/assets/0322bad7-be54-44b8-9a9c-8213819455f6" />

## Features

- **Navbar**: a persistent Bootstrap navbar at the top with a configurable brand title
  (left) and a dark-mode toggle (right).
- **Dark mode**: switchable light/dark themes via a toggle; your choice persists across
  visits and defaults to your system preference.
- **Services**: clickable tiles that open in a new tab (icon image or monogram fallback).
- **Bookmark groups**: named groups with collapsible/expandable bookmarks (Bootstrap Icon
  chevron indicators); collapsed state persists across visits via `localStorage`.
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
    collapsed: true  # optional; start the group collapsed on load (default: open)
    bookmarks:
      - label: YouTube
        url: "https://www.youtube.com"
        icon: "https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/svg/youtube.svg"  # optional; shown next to the label
      - label: Spotify
        url: "https://open.spotify.com"
```

- A service `icon` is treated as an image URL if it is a valid `http(s)` URL; otherwise the
  first letter of the name is shown as a monogram. A bookmark `icon` is the same: a valid
  `http(s)` image URL shown next to the label, otherwise the text label alone is shown.
- `collapsed: true` makes a bookmark group start closed when the page loads; omitted
  (or `false`) groups start open. A user who manually expands/collapses a group
  overrides this default in their own browser.
- `title` sets the dashboard name shown in the navbar. If omitted, empty, or whitespace-only,
  the default **"Homelab"** is shown.
- The moon/sun button in the navbar toggles dark mode; your choice is remembered.
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

## Bookmark Icons

Each bookmark can show an icon next to its label by setting its `icon` to any valid remote
image URL — just like service logos.

- Any `http(s)` image URL works as a bookmark icon (e.g., your own CDN or static host), and
  it is shown alongside the bookmark's text label.
- If a bookmark icon is absent, not a valid URL, or fails to load, a circle with the first
  letter of the label is shown in its place (a monogram), matching the homelab service
  tiles — the page never breaks.
- Short-word icon values (e.g., `icon: youtube` or `icon: play`) are **not** supported
  anywhere in this project; always use a full image URL, or omit the `icon` field to show
  the letter monogram.
- To change a bookmark icon, edit the `icon` URL and refresh; no rebuild or restart is
  needed.

```yaml
bookmark_groups:
  - name: Media
    bookmarks:
      - label: YouTube
        url: "https://www.youtube.com"
        icon: "https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/svg/youtube.svg"
      - label: Spotify
        url: "https://open.spotify.com"   # no icon -> a circle with "S"
```

## Bootstrap Assets

The Bootstrap and Bootstrap Icons assets are **not** committed to source control. They are
tracked as dependencies in [`package.json`](package.json) (pinned versions) with `pnpm`,
and provisioned into `app/static/` by copying the compiled files from the installed
packages.

Provision on a fresh checkout:

```bash
pnpm setup        # = pnpm install && pnpm provision
```

After provisioning, `app/static/bootstrap/css/bootstrap.min.css` and
`app/static/bootstrap/js/bootstrap.bundle.min.js` exist, plus the Bootstrap Icons CSS and
fonts under `app/static/bootstrap-icons/`, and the page is styled.

To **update the Bootstrap version**:

```bash
pnpm add bootstrap@X.Y.Z   # updates package.json + pnpm-lock.yaml
pnpm provision             # replaces the assets with the new version
```

To **update Bootstrap Icons** the same way: `pnpm add bootstrap-icons@X.Y.Z` then
`pnpm provision`.

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

## Code Formatting and Linting

**Python**

```sh
# Linting
uv run ruff check
uv run ruff check --fix
# Formatting
uv run ruff format
# Type checking
uv run ty check
```

**HTML Templates**

```sh
uv run djlint . --reformat --single-attribute-per-line
```
