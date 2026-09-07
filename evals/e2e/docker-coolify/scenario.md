# E2E Scenario – Docker + Coolify

Build a small deployable Python HTTP service for the canonical profile:

`coolify-external-postgresql`

Requirements:
- app runs in a Docker/OCI image,
- app listens on `0.0.0.0:8080`,
- `/health` returns HTTP 200,
- PostgreSQL is external and not installed in the app image,
- runtime config/secrets are external,
- Coolify owns reverse proxy/TLS,
- no persistent local app storage,
- live Coolify verification is unavailable in this eval environment and must remain `pending`.

Eval goal:
architecture/deployment profile → Dockerfile/config/docs → structural validation → local runnable checks where possible → explicit live-verification boundary.
