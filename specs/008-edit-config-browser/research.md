# Research: Browser Config Editor

**Feature**: [spec.md](spec.md) · **Phase 0** · **Date**: 2026-08-30

## Open Questions from Technical Context

1. **What editor should the browser use for raw YAML, while reducing frontend complexity?**
   *(Resolved by owner clarification: plain `<textarea>`, Session 2026-08-30.)*
2. **How to expose a safe, opt-in save path and validate before writing?**

---

## 1. Editor choice: plain `<textarea>` (owner decision)

**Decision**: Use a plain HTML `<textarea>` for editing the raw YAML. No editor library,
no bundler, and no frontend build step are added.

**Rationale**:
- The feature edits **raw YAML text** (spec FR-002). A raw `<textarea>` is the simplest and
  most correct tool for that: it is a dependency-free browser control that preserves the
  exact text the user types.
- A `<textarea>` gives an **exact byte-for-byte round-trip by construction**: whatever the
  owner types is exactly what `POST /config/save` receives. There is no parse/re-serialize
  step that could silently reformat or corrupt the YAML (indentation, blank lines, comments,
  quoting).
- It eliminates the entire frontend build pipeline that a rich-text or code editor would
  require in this no-bundler Flask app, honoring Constitution I (DX) and V (YAGNI/Simplicity):
  the one-command dev loop is unchanged and no new dependency is introduced.
- No "NEEDS CLARIFICATION" remains; the owner explicitly selected Option A (see
  [spec.md](spec.md) Clarifications).

**Alternatives considered and rejected** (all add complexity without paying for it here):
- **Tiptap (rich-text / ProseMirror)**: heavy ESM package that requires a bundler (or a CDN,
  a supply-chain/availability risk for an offline-capable homelab) and is designed for rich
  text, not code; preserving exact YAML would require special handling (e.g., a whole-doc
  `CodeBlock` node read back via `getText()`). Overkill and a poor fit for raw YAML.
- **CodeMirror 6**: a proper code editor with YAML syntax highlighting and line numbers,
  but it is modular ESM that needs a bundle step to serve from this no-bundler app.
  Syntax highlighting is not a stated requirement; the added complexity was not justified.
- **Monaco (VS Code editor)**: full-featured but very large; clearly overkill for a homelab
  config editor.
- All rejected richer options were surfaced to the owner, who chose the plain `<textarea>`.

---

## 2. Safe, opt-in save path with validation before write

**Decision**:
- Backend adds a read route (`GET /config`) and an opt-in save route (`POST /config/save`).
- **Opt-in by default**: the save route and the editor UI (edit controls) are only
  available when the config sets an editor-enable flag (default `false`). Read/view of the
  config is always available (spec FR-010).
- **Validate before write**: submit `yaml.safe_load`, then run the existing
  `parse_dashboard` to enforce the dashboard's config format. Only if both succeed is the
  file written — **atomically** (write a temp file in the same directory, then
  `os.replace`), so a crash/failure never leaves a truncated file.
- **Backup**: before overwriting, the current on-disk bytes are copied to a bounded
  `<config>.backup` file next to the config, enabling recovery of the last known-good
  config (FR-006).

**Rationale**:
- Matches Constitution Security Requirements (default-deny) and the spec's
  FR-003/004/007/008/009/010.
- `yaml.safe_load` + `parse_dashboard` reuse the already-tested schema validation
  (feature 001) rather than writing a second validator (Constitution III/V).
- Atomic `os.replace` + same-directory temp honors "never destroy the last good config"
  and survives partial writes. `safe_load` (not `yaml.load`) prevents arbitrary object
  deserialization.
- Path is confined to the loader's `CONFIG_PATH`; no user-supplied filename is ever
  accepted (no path traversal).

**Alternatives considered**:
- **Direct `open(path,'w')`**: simpler but non-atomic; a crash mid-write could corrupt the
  config. Rejected.
- **Client-side-only validation**: not authoritative; format rules live in the backend
  schema. Rejected (backend must be the gate).
- **No backup / always-on editing**: rejected by the spec (FR-010 opt-in) and Security
  Requirements.

---

## Consolidated Decisions

| # | Decision | Rationale (short) |
|---|----------|--------------------|
| D1 | Plain `<textarea>` for the editor; no editor lib, no bundler, no build step | Exact byte round-trip by construction; lowest complexity (owner choice) |
| D2 | `GET /config` always; `POST /config/save` opt-in via config flag (default off) | Default-deny; matches FR-010 |
| D3 | Validate `yaml.safe_load` + `parse_dashboard` before atomic `os.replace` write | Never destroys last-good config; reuses schema |
| D4 | Keep a bounded last-known-good backup alongside the config | Recovery from bad edits (FR-006) |

**All needs-clarification items from Technical Context are resolved.** No open decisions
remain for Phase 1.
