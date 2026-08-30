# Contract: Config Editor (UI + Save Endpoint)

**Feature**: [spec.md](../spec.md) · **Phase 1** · **Date**: 2026-08-30

This defines the browser-facing contract for viewing and (opt-in) editing the dashboard
config. The backend is the security/validation gate; the browser is never trusted.

---

## 1. Read / view route

**`GET /config`**

**Purpose**: Always available (spec FR-001). Returns the page that shows the current raw
config; when editing is disabled it is read-only (no edit controls / no save).

**Server → browser (payload embedded in the rendered page)**:

- `raw_config`: the current config file content (escaped) presented into the editor
  `<textarea>`.
- `editing_enabled`: boolean derived from the config flag (default `false`).
- `writable`: boolean — whether the config file is present and writable (for an accurate
  message when editing is enabled but the file cannot be written).
- `config_path`: display value of the config location (informational; never used to build
  filesystem paths client-side).

**Behavior**:
- If the config is unreadable, render an error message rather than a broken page
  (spec User Story 1, scenario 3).

---

## 2. Save route (opt-in)

**`POST /config/save`**

**Availability**: The endpoint and its UI affordance exist only when the config's editor
flag is `true`. When editing is disabled, this route responds **403** and must not write.

**Request body** (JSON):

```json
{ "content": "<full raw YAML document text, as-is>" }
```

**Success response** — `200 OK`:

```json
{ "ok": true, "message": "Saved. The dashboard will reflect the change." }
```

**Failure responses**:

| Status | Body | When |
|--------|------|------|
| `403` | `{ "ok": false, "error": "Config editing is disabled." }` | Editor flag off / absent |
| `400` | `{ "ok": false, "error": "<specific validation message>" }` | Invalid YAML or invalid dashboard config format (unchanged on disk) |
| `500` | `{ "ok": false, "error": "Could not write the config file." }` | File/dir not writable, disk failure, or path not confined |

**Guarantees** (spec FR-003/004/007/008/009/010, D4/D5 in research):
- No write occurs unless `yaml.safe_load` **and** `parse_dashboard` both pass.
- The write is atomic (`os.replace` of a same-directory temp file).
- The previous config is backed up before overwrite.
- Only the single resolved `CONFIG_PATH` is ever written; no client-supplied path is used.

---

## 3. Editor UI contract (plain `<textarea>`)

**Purpose**: Provide an exact, raw-text editor for the YAML (spec FR-002; owner chose a
plain `<textarea>` — Clarification Session 2026-08-30, Option A). No richness beyond a
plain text control; no editor library, bundler, or build step.

**Content model**:
- The editor is a single HTML `<textarea>` whose `value` is set to the current `raw_config`.
- Read-back: the submit payload `content` is exactly
  `document.querySelector('textarea#config-editor').value` — the verbatim text submitted to
  `POST /config/save`. There is no parse/re-serialize; the bytes round-trip exactly
  (research D1).

**Editing controls**:
- Initially: `<textarea value="<raw_config (escaped)>">` (server-rendered; content escaped
  with `escape_html` per FR-009).
- Save button → submit `{ content: textarea.value }`.
- Revert button (when enabled + a backup exists) → restore last-known-good from a
  `GET`-provided value or re-fetch; visually confirm before overwriting.
- While save is in flight, disable the save button to prevent double-submit.

**Client feedback**:
- On `200` → success message; the dashboard reflects the change on next load (hot reload).
- On `400` → render the server's `error` message; keep the textarea content intact.
- On `403` → clear "editing disabled" message; hide save.
- On `500` → error message; content intact.

**Styling / accessibility**: the `<textarea>` is styled via `app.css` as a scrollable
monospace block with a visible focus state (Bootstrap form/`form-control` base), and is
keyboard-usable; theme matches the dashboard.

---

## 4. Contract tests to enforce (spec FR-003/004/009/010)

1. `POST /config/save` with a valid, edited YAML returns `200` and the running dashboard
   reflects the change on the next request (hot reload).
2. `POST /config/save` with malformed YAML returns `400` and leaves the previous config
   unchanged, byte-for-byte.
3. `POST /config/save` with valid YAML but a format violation returns `400` and changes
   nothing.
4. With the editor flag absent/`false`, `POST /config/save` returns `403` and writes
   nothing; `GET /config` shows no edit controls.
5. The exact text submitted on save round-trips: `GET /config` → edit → save the same
   bytes → `GET /config` returns identical bytes (no reformatting).
6. When the config file is read-only/unwritable, save returns `500` and preserves the
   existing file.
