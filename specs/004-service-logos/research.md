# Research: Service Logos

**Phase 0 output for `/specs/004-service-logos/plan.md`**

Purpose: resolve the technical decisions required to deliver remote-URL logos for
homelab services and to encourage dashboardicons.com as the logo source, working
within the existing Flask/Bootstrap dashboard and the Constitution's principles.

## 1. Can Any Remote URL Serve as a Logo, Given the Existing Code?

- **Decision**: Yes. Any valid absolute `http(s)` URL is already accepted as a
  service `icon` and rendered as an `<img>` logo. `app/security.py::validate_url`
  requires an `http`/`https` scheme and a non-empty netloc; `create_app` registers
  it as the Jinja `url` test, and `app/templates/index.html` renders
  `{% if service.icon and service.icon is url %}` as an `<img>` (with an `onerror`
  monogram fallback), else a monogram. Therefore "any remote logo URL should be
  supported" is a property of the current implementation.
- **Rationale**: The minimal change to satisfy FR-004 ("MUST accept any valid remote
  image URL as a service logo") is to lock this behavior in with tests and document
  it, rather than add code. This honors YAGNI (Principle V) — no new framework, no
  change to the existing URL gate.
- **Alternatives considered**:
  - Introduce a separate `logo` field: rejected (scope — user chose to extend `icon`).
  - Download/cache logos locally: rejected — adds storage, network-at-build, and
    contradicts the lean, remote-only choice.
  - Restrict to a whitelist of hosts: rejected — user explicitly wants any remote URL;
    validation remains scheme+netloc+safe-rendering, not host allow-listing.

## 2. Encouraging dashboardicons.com as the Source

- **Decision**: Recommend dashboardicons.com in the example config, README, and
  quickstart. Direct icon assets are served from the jsDelivr CDN pattern
  `https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/<svg|png>/<name>.<ext>`,
  e.g. `https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/svg/plex.svg`.
  The example config will use these URLs for the service logos.
- **Rationale**: The user explicitly asked to encourage this source. Using its real
  direct-image URL format makes the example runnable (the `<img>` loads the logo).
  It is only a recommendation (FR-007), so the dashboard must not depend on it.
- **Alternatives considered**: pointing the example to the site root
  (`https://dashboardicons.com`) — rejected, since that is an HTML page, not an image;
  the example and docs will reference the CDN asset URL pattern directly.

## 3. Fallback and Safety Guarantees

- **Decision**: Reuse the existing monogram-on-`onerror` fallback for broken logos and
  the existing `validate_url` + Jinja-escaping for safety. A non-URL `icon` value
  (e.g., a plain word) continues to render a monogram; a broken remote image triggers
  the inline `onerror` to reveal the monogram. All rendered URLs are HTML-escaped,
  and service names are escaped, so no injection (Constitution Security).
- **Rationale**: Minimal, already-tested behavior; adding any new runtime
  reachability probe would violate offline/performance constraints and YAGNI. The
  browser handles load failure via `onerror`.
- **Alternatives considered**: server-side URL HEAD checks or proxying images
  through the app — rejected (adds latency, network dependence, complexity, and is
  unnecessary since the client already degrades gracefully).

## 4. Performance with Many Logo-Bearing Services

- **Decision**: Rely on browser-native lazy loading via the existing `loading="lazy"`
  attribute on the service `<img>` elements, and on CDN edge caching for the
  recommended dashboardicons.com assets. No client-side image preloading or bundle is
  added.
- **Rationale**: Keeps the homepage fast (SC-004) without new machinery, aligning
  with the existing tile rendering and Principle V.
- **Alternatives considered**: adding a custom image loader/placeholder — rejected
  (complexity not justified; Bootstrap/app.css already style tiles and fallbacks).

## 5. Deliverable Scope

- **Decision**: Given the behavior largely exists, this feature's concrete outputs
  are: (a) tests that pin "any valid remote URL renders as a logo" + fallback +
  safety (written first), (b) an updated `config/example.yaml` demonstrating
  dashboardicons.com logo URLs, and (c) documentation (README + quickstart) covering
  how to assign a logo and where to source one. Application-code changes are only
  made if the hardening tests reveal a gap (e.g., template/schema tweak), and are
  justified by those tests.
- **Rationale**: Test-first (Principle IV) plus accuracy of developer docs (Principle
  I). Keeps the change small, reviewable, and free of speculative complexity.
- **Alternatives considered**: a larger re-architecture of icon/logo handling:
  rejected (violates YAGNI and user scope).
