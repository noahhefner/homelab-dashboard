<div align="center">

# Homelab Dashboard

![uv](https://img.shields.io/badge/uv-%23DE5FE9.svg?style=for-the-badge&logo=uv&logoColor=white)
![Python](https://img.shields.io/badge/python-%233670A0.svg?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![PNPM](https://img.shields.io/badge/pnpm-%234a4a4a.svg?style=for-the-badge&logo=pnpm&logoColor=f69220)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

</div>

A single-page dashboard for your home server. Renders your tiles and grouped bookmarks from one YAML file, served by a small Flask app inside a single Docker container.

<img width="1364" height="881" alt="image" src="https://github.com/user-attachments/assets/5dba3602-35c2-4f51-b78c-63f482cda12f" />

## Features

- **Tiles**: Clickable links that open in a new tab. A tile can point to an internal homelab service or an external service (e.g., webmail, a cloud account portal). Tiles are organized with tile groups.
- **Bookmarks**: Links to other frequently used sites in a compact sidebar. Bookmarks are organized with bookmark groups.
- **Search Bar**: Quick access to your preferred search engine.
- **Live reload**: Edit the YAML file and refresh the browser — no restart needed.
- **Mobile Friendly**: Reflows to no-horizontal-scroll layout on phones; tap-friendly.
- **Dark mode**: Switchable light/dark themes via a toggle.
- **One config file**: Everything is defined in a single YAML document. You can even edit the YAML file directly from your browser with the built-in editor.

## Requirements

- Python 3.14+ and [`uv`](https://docs.astral.sh/uv/) for local development,
  **and/or** Docker for running the container.
- **Node.js (≥24) and [pnpm](https://pnpm.io/)** to provision the Bootstrap
  assets.

## Configuration

Everything is configured in a YAML file. See [`config/example.yaml`](config/example.yaml) as a starting point:

```yaml
title: "Home Lab"  # Title of the page
editor: true       # Enable / disable in-browser yaml editor

# Search engine for the navbar search bar. A URL template containing a {query}
# placeholder; omit it to default to Google.
search_engine: "https://duckduckgo.com/?q={query}"
# Optional icon shown next to the search bar (external image URL).
search_engine_icon: "https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/svg/duckduckgo.svg"

# Tiles are organized into named groups. Tile groups are always visible (no 
# collapse/expand), unlike bookmark groups.
tile_groups:
  - name: Cloud & Webmail
    # Optional: Display an icon for the tile group.
    icon: "https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/svg/cloudstream.svg"
    tiles:
      - name: Webmail
        url: "https://mail.example.com"

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

## Local Run (Development)

**Build Frontend Bundles**

First download and bundle the frontend assets with `pnpm`. This command will download frontend dependencies from npm, bundle them, and drop the bundles into `app/static`:

```sh
pnpm build
```

You should see the following after the build finishes:

```
app/static/
├── css
│   └── app-COwDGdVP.css
├── favicon
│   ├── android-chrome-192x192.png
│   ├── android-chrome-512x512.png
│   ├── apple-touch-icon.png
│   ├── favicon-16x16.png
│   ├── favicon-32x32.png
│   ├── favicon.ico
│   └── site.webmanifest
├── fonts
│   ├── bootstrap-icons-BeopsB42.woff
│   └── bootstrap-icons-mSm7cUeB.woff2
├── js
│   └── app-hR5JlhjU.js
└── manifest.json
```

**Config File**

Optionally, create a `config/local.yaml` file for testing. (`local.yaml` is gitignored). Set the `CONFIG_PATH` environment variable.

```bash
uv sync
# Run ONE of the following:
# export CONFIG_PATH=config/local.yaml
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

[Pytest](https://docs.pytest.org/) is used as the testing framework. Run the tests with `uv` or the `test` Makefile target:

```bash
# Run tests with uv
uv run pytest

# Or use the Makefile target
make test
```

## Code Formatting and Linting

Formatting and linting commands are provided by the `Makefile`:

```sh
# Check everything
make check

# Format everything
make fix
```