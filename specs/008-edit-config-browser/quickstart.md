# Quickstart: Verify Edit Config From Browser

**Feature**: [spec.md](spec.md) · **Phase 1** · **Date**: 2026-08-30

This guide validates the feature end-to-end. Detailed contracts are in
[contracts/config-editor.md](contracts/config-editor.md); data/flag semantics in
[data-model.md](data-model.md).

## Prerequisites

- `uv sync` (Python deps) and `pnpm install && pnpm provision` (existing Bootstrap/Icons
  assets). No new frontend dependency or build step is required (the editor is a plain
  `<textarea>`).
- The app runs from a writable config (see `ConfigLoader` / `CONFIG_PATH`).

## Setup

1. Ensure an editor flag is absent or `false` → confirm editing is **off by default**.
2. To enable editing for a test, add `editor: true` (or the chosen flag key) at the top
   level of the config. The dashboard hot-reloads this flag.

## Validation scenarios

### 1. Read-only by default (FR-010)

```bash
uv run pytest tests/unit/test_config_flag.py -k "disabled_by_default or read_only_when_disabled"
```

**Expected**: `GET /config` renders the current YAML with **no** edit/save controls; a
direct `POST /config/save` returns `403` and leaves the file unchanged.

### 2. Exact round-trip (FR-002, FR-003, research D1)

```bash
uv run pytest tests/unit/test_editor_config.py -k "roundtrip or preserves_bytes"
```

**Expected**: The editor is a plain `<textarea>`; the value submitted on save is the exact
text typed. Save → `GET /config` returns identical bytes (no reformatting of indentation,
blank lines, comments, quoting).

### 3. Validate before write; never destroy good config (FR-003/004/007)

```bash
uv run pytest tests/unit/test_editor_config.py -k "rejects_invalid or preserves_previous"
uv run pytest tests/integration/test_config_editor_flow.py
```

**Expected**:
- Malformed YAML → `400`, previous config intact byte-for-byte.
- Valid YAML but format violation (e.g., `services: "not-a-list"`) → `400`, nothing written.
- File made read-only → `500`, existing file preserved.

### 4. End-to-end save reflected by the dashboard (FR-005, User Story 3)

1. Enable editing (`editor: true`), start the app.
2. Open `/config`, change e.g. `title:` or add a service, save.
3. **Expected**: `200`; on the next `/` load the change is visible with no restart (hot
   reload re-reads the config on mtime change).

### 5. Recovery (FR-006)

```bash
uv run pytest tests/unit/test_editor_config.py -k "backup or recover"
```

**Expected**: After a validated overwrite, a last-known-good backup exists and the owner
can restore it via the revert control.

## Acceptance checklist

- [x] Editing disabled by default; view-only when off; `403` on direct save.
- [x] Plain `<textarea>` editor shows raw YAML and round-trips bytes exactly.
- [x] Invalid YAML / format rejected with a specific message; prior config intact.
- [x] Valid save is atomic, backed up, and reflected by the dashboard without restart.
- [x] Revert restores the last-known-good config.
- [x] Output rendered back into the page is escaped; no user path is used for writes.
