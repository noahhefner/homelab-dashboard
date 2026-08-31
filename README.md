# Homelab Dashboard

A self-hosted, single-page dashboard homepage for your home server. It renders your services and grouped bookmarks from one YAML file, served by a small Flask app inside a single Docker container.

<img width="1344" height="746" alt="image" src="https://github.com/user-attachments/assets/0322bad7-be54-44b8-9a9c-8213819455f6" />

## Features

- **Services**: Clickable tiles that open in a new tab (icon image or monogram fallback).
- **Bookmark groups**: Named groups with collapsible/expandable bookmarks.
- **Live reload**: Edit the YAML file and refresh the browser — no restart needed.
- **Mobile responsive**: reflows to no-horizontal-scroll layout on phones; tap-friendly.
- **Dark mode**: Switchable light/dark themes via a toggle.
- **One config file**: Everything is defined in a single YAML document. You can even edit the YAML file directly from your browser with the built-in editor.

## Requirements

- Python 3.14+ and [`uv`](https://docs.astral.sh/uv/) for local development,
  **and/or** Docker for running the container.
- **Node.js (≥24) and [pnpm](https://pnpm.io/)** to provision the Bootstrap
  assets.

## Configuration

Everything is configured in a YAML file. See [`config/example.yaml`](config/example.yaml) for a starting point:

```yaml
title: "Home Lab"  # Title of the page
editor: true       # Enable / disable in-browser yaml editor

# Put links to your homelab services here.
services:
  - name: Plex
    url: "https://plex.lan:32400"
    # Optional: Display an icon for the service.
    icon: "https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/svg/plex.svg"  

# Place your bookmarks here, organized with groups.
bookmark_groups:
  - name: Media
    # Optional: Collapse the bookmark group on page load (default: false)
    collapsed: true
    bookmarks:
      - label: YouTube
        url: "https://www.youtube.com"
        # Optional: Display an icon for the bookmark.
        icon: "https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/svg/youtube.svg"
      - label: Spotify
        url: "https://open.spotify.com"
```

## Bootstrap Assets

The Bootstrap and Bootstrap Icons assets are **not** committed to source control. They are tracked as dependencies in [`package.json`](package.json) (pinned versions) with `pnpm`, and provisioned into `app/static/` by copying the compiled files from the installed packages.

Provision on a fresh checkout:

```bash
pnpm setup        # = pnpm install && pnpm provision
```

After provisioning, `app/static/bootstrap/css/bootstrap.min.css` and
`app/static/bootstrap/js/bootstrap.bundle.min.js` exist, plus the Bootstrap Icons CSS and fonts under `app/static/bootstrap-icons/`, and the page is styled.

## Local Run (Development)

Create a `config/local.yaml` file for testing. (`local.yaml` is gitignored).

```bash
uv sync
export CONFIG_PATH=config/local.yaml
# or use the example config
# export CONFIG_PATH=config/example.yaml
uv run -m app.server
```

Open [http://localhost:5000](http://localhost:5000). Edit your config file, save, and refresh to see changes.

## Run with Docker

Mount the directory containing your config file as a Docker volume. **Do not mount the config file directly.**

```bash
docker build -t homelab-dashboard .
docker run --rm -p 5000:5000 -e CONFIG_PATH='/app/config/example.yaml' -v "$PWD/config:/app/config" homelab-dashboard

# DO NOT DO THIS
docker run --rm -p 5000:5000 -e CONFIG_PATH='/app/config/example.yaml' -v "$PWD/config/config.yaml:/app/config/example.yaml" homelab-dashboard
```

Or use Docker Compose:

```yaml
services:
  dashboard:
    build: .
    image: homelab-dashboard
    container_name: homelab-dashboard
    ports:
      - "5000:5000"
    environment:
      - CONFIG_PATH=/app/config/example.yaml
    volumes:
      - ./config:/app/config
    restart: unless-stopped
```

## Tests

```bash
uv run pytest
```

Runs the contract, unit, and integration suites (config validation, parsing, live reload, rendering, bookmark groups, and mobile layout).

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
