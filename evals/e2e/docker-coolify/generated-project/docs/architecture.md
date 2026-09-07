# Architecture – Docker/Coolify E2E

## Runtime
Single stateless Python HTTP service.

## Persistence
Relationsdata, when used, is held in external PostgreSQL. The app image does not contain PostgreSQL server.

## Deployment
Target profile: `coolify-external-postgresql`.

The application listens on `0.0.0.0:8080`.
Coolify owns reverse proxy and TLS.
Runtime configuration and secrets are injected by the platform.

## Storage
No persistent local application files.

## Health
`GET /health` returns HTTP 200.
