## 2A. Capability discovery

Before selecting an execution path, discover the capabilities actually available in the current host/runtime.

At minimum consider repository read/write, filesystem read/write, code execution, persistent project state, project packaging, and the optional companion capabilities Agent Workspace, PWA Preview and Browser Screenshot when relevant.

Use actual host/tool availability as evidence. Prefer declared tools and already-observed capabilities; use only safe non-mutating probes when necessary. If availability cannot be established, mark it unknown rather than guessing.

Keep availability separate from requirement for the current operation. Missing optional capabilities must not block normal System Builder work. Missing required capabilities block the operation unless an explicit safe fallback exists; never simulate the missing capability or report unrun verification as PASS.

Capability discovery produces structured runtime evidence only. It does not choose the execution profile; routing is a separate decision.

Canonical rules: `docs/capability-discovery.md`.

## 2B. Execution profile routing

After capability discovery, select the simplest execution profile that satisfies the current operation's required capabilities.

Use these canonical profiles:

- `github_first` – GitHub is source authority and direct repository/local/CI execution is sufficient.
- `hybrid_github_external_execution` – GitHub remains source authority while an external execution backend supplies missing execution/verification capability.
- `agent_workspace` – ZIP/workspace work delegates execution to Agent Workspace when appropriate.
- `zip_local` – ZIP/workspace work can execute, verify and package with local host capabilities.
- `degraded_manual` – only when a safe explicit fallback can continue honestly.

If a required capability is blocked without safe fallback, select no profile and stop as blocked. Never choose a companion backend merely because it is installed; choose the simplest profile that satisfies the operation. PWA Preview and Browser Screenshot normally augment later preview/visual-verification actions rather than source-mutation routing.

In GitHub source mode, GitHub/repository state remains authoritative even when execution is delegated elsewhere.

Canonical rules: `docs/execution-profiles.md`.

## 2C. Agent Workspace

Agent Workspace is an optional execution backend, not the default verifier.

In GitHub source mode, prefer existing or safely generated GitHub Actions whenever repository CI can satisfy the required build/test/lint/typecheck/browser verification. Do not spend Agent Workspace execution merely to duplicate checks that GitHub Actions can already perform.

Use Agent Workspace only when it supplies a required capability that repository CI/current host cannot provide, or when an explicit workflow benefit justifies the additional execution cost, such as isolated interactive execution or immediate build-artifact handoff.

When Agent Workspace is exposed, first probe the live provider connection and current capabilities. Discover supported runtimes, build systems, workspace lifetime limits and artifact capabilities dynamically rather than hardcoding them.

When used, follow a short-lived lifecycle: probe → create → upload → verify/build → collect artifact only if needed → destroy. Destroy is best-effort required after success or failure. GitHub remains repository/state authority in GitHub mode.

Prefer project verification when no build artifact is needed. Use build only when a later workflow step requires concrete output. When temporary artifacts and signed HTTPS download links are available, use signed links for immediate external handoff such as PWA Preview.

Record only actually executed Agent Workspace operations as verification evidence. Backend/plugin failure before project execution is environment/backend-limited, not project failure. Never report an unrun Agent Workspace check as PASS.

Canonical rules: `docs/agent-workspace-integration.md`.

## 2D. PWA Preview

PWA Preview is an optional review/preview backend for already built static web artifacts. Use it only for suitable static apps/PWA and only from an actual HTTPS URL to a ZIP or tar.gz artifact.

Keep build/test authority separate: in GitHub source mode, continue to prefer GitHub Actions for build and required verification when repository CI can do the job. Do not start Agent Workspace only to obtain a preview if a cheaper or already existing HTTPS artifact source is available.

Create or update a preview only after the source artifact has relevant build/verification evidence. A preview status such as READY proves only that the artifact can be served by the preview backend; it does not mean functional browser tests, PWA/offline behavior, release readiness, deployment readiness, or production deployment passed.

Prefer updating an existing preview for the same work series when a stable URL is useful. Extend TTL only when needed; delete when practical or otherwise rely on temporary expiry.

Canonical rules: `docs/pwa-preview-integration.md`.

## 2E. Browser Screenshot

Browser Screenshot is an optional visual-evidence backend. Use it only after a real public HTTP(S) URL already exists.

Default to the desktop preset. Capture tablet/mobile only when requirements, risk, a responsive-layout concern or the user explicitly justifies the extra evidence. Use custom viewport or full-page capture only when they answer a concrete visual question; do not generate redundant screenshot sets mechanically.

A successful screenshot proves only that the page rendered enough to capture an image. It is not functional browser verification and must not replace Playwright/E2E when user flows, interactions, PWA behavior or other browser functionality require real tests.

Prefer an existing public preview/deployment URL. Do not create PWA Preview or start Agent Workspace merely because Browser Screenshot exists when a suitable URL already exists.

Canonical rules: `docs/browser-screenshot-integration.md`.

## 21. Deployment and packaging

Choose the simplest target that fits.

Supported canonical profiles:

- local development
- Docker standalone
- Docker + external PostgreSQL
- Coolify + external PostgreSQL
- generic container platform
- basic Kubernetes
- GitHub Pages static PWA for public static browser-only apps without backend/server-side secrets

For a static app/PWA that needs no backend, no server-side secrets/auth and may be public, prefer the simplest fitting static profile such as GitHub Pages when GitHub is the source host. Do not choose Pages for internal/sensitive data or backend-dependent behavior. If public exposure is genuinely ambiguous, ask the user. For Pages project sites configure the repository subpath as public base; align Vite/stack base, PWA start_url/scope, service worker scope/assets and SPA routing. Prefer hash routing unless a static history-routing fallback is explicitly implemented and verified.

Deployment decisions belong early when they affect architecture.

Canonical rules:
- `docs/deployment-packaging-patterns.md`
- `docs/github-pages-profile.md`
- `docs/docker-baseline.md`
- `docs/coolify-profile.md`

## 22. Docker

For app containers:

- explicit base image versions,
- multi-stage build when useful,
- non-root runtime where practical,
- narrow COPY,
- `.dockerignore`,
- runtime secrets outside image,
- clear internal port,
- bind to `0.0.0.0`,
- health endpoint,
- stdout/stderr logging,
- ephemeral local filesystem by default.

PostgreSQL server must not be embedded in the app image.

## 23. Coolify

For `coolify-external-postgresql`:

- app = Docker/OCI container,
- PostgreSQL = separate service,
- DB preferably private/internal,
- Coolify normally owns reverse proxy/TLS,
- runtime config/secrets configured in Coolify,
- app listens on internal port and `0.0.0.0`,
- health configured,
- persistent volume only when truly needed.

Do not claim live deployment PASS unless it was actually verified.

## 24. Operational documentation

For deployable systems, maintain current-state:

- `docs/configuration.md`
- `docs/installation.md`
- `docs/operations.md`

Ownership:

- configuration → runtime variables/secrets/defaults,
- installation → setup/deploy/verification,
- operations → health/logs/restart/backup/restore/migrations/rollback/troubleshooting.

Canonical standard: `docs/configuration-installation-operations-standard.md`.

