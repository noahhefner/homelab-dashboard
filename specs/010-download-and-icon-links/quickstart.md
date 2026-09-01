# Quickstart: Verify Download Config & Icon Links

**Feature**: [spec.md](spec.md) · **Phase 1** · **Date**: 2026-08-31

This guide validates the feature end-to-end. Detailed contracts are in
[contracts/config-download.md](contracts/config-download.md); data/payload semantics in
[data-model.md](data-model.md).

## Prerequisites

- `uv sync` (Python deps) and `pnpm install && pnpm provision` (existing Bootstrap/Icons
  assets). **No new frontend dependency or build step is required** (read-only route +
  static template content).
- The app runs against a config file (see `ConfigLoader` / `CONFIG_PATH`).

## Setup

1. Point the app at a config file (default `config/example.yaml`).
2. This feature works whether or not the `editor` flag is enabled — test both.

## Validation scenarios

### 1. Download returns exact on-disk bytes + correct filename (FR-001/002/003)

```bash
uv run pytest tests/integration/test_config_download.py -k "bytes and filename"
```

**Expected**: `GET /config/download` returns `200`; `Content-Disposition` is
`attachment; filename="<basename of the config path>"` (e.g., `example.yaml`); the body is
byte-for-byte identical to the config file on disk.

### 2. Works in read-only mode (FR-004)

```bash
uv run pytest tests/integration/test_config_download.py -k "readonly"
```

**Expected**: With no `editor` flag, `GET /config/download` still returns the exact bytes,
and `GET /config` still shows the download button and icon links.

### 3. Unreadable config → clear error, no empty download (FR-005)

```bash
uv run pytest tests/integration/test_config_download.py -k "unreadable"
```

**Expected**: When the config file is missing/unreadable, download returns a non-`200`
error with a clear message, and never an empty `200` attachment.

### 4. Page renders download button + icon links in both modes (FR-001/006/008)

```bash
uv run pytest tests/integration/test_config_download.py -k "renders"
```

**Expected**: `GET /config` includes the "Download config" control and both icon-source
links (`dashboardicons.com`, `homarr-labs/dashboard-icons`) when editing is enabled **and**
when it is disabled.

### 5. Icon links open in a new tab, safely (FR-007)

```bash
uv run pytest tests/integration/test_config_download.py -k "newtab"
```

**Expected**: Each icon-source anchor has `target="_blank"` and `rel="noopener noreferrer"`.

## Acceptance checklist

- [x] `GET /config/download` returns the exact on-disk bytes with the basename filename.
- [x] Works in both editing and read-only modes.
- [x] Unreadable config yields a clear error, never an empty/partial download.
- [x] `GET /config` shows the download button and both icon links in both modes.
- [x] Icon links open in a new tab with `noopener noreferrer`.
- [x] Filename is derived server-side from the config path (no client-supplied input).
