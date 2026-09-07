# Coolify Deployment Profile – Example

## Profile

coolify-external-postgresql

## Application

- artifact: Docker image built from repository Dockerfile
- Dockerfile: `Dockerfile`
- internal port: 8080
- bind address: `0.0.0.0`
- stateless: yes
- runtime user: non-root `appuser`

## Database

- type: external PostgreSQL
- provisioned by: Coolify Database service
- connection model: internal/private hostname and runtime credentials
- public exposure: no

## Runtime configuration

### Non-secret
- `PORT=8080`
- `PUBLIC_BASE_URL=https://example.apps.example.org`
- `LOG_LEVEL=INFO`

### Secrets
- `DATABASE_PASSWORD`
- `GITHUB_APP_PRIVATE_KEY`

## Domain / proxy / TLS

- public hostname: `example.apps.example.org`
- public base URL: `https://example.apps.example.org`
- reverse proxy owner: Coolify
- TLS owner: Coolify

## Health

- path: `/q/health`
- expected status: HTTP 200
- configured in Coolify: yes

## Persistence

- database: external PostgreSQL
- volumes: none
- temporary files: ephemeral container filesystem only

## Migrations

- strategy: controlled Flyway migration before application traffic
- rollback/restore: previous image tag plus PostgreSQL backup restore for non-compatible migration

## Build / deploy

- source: Git
- build command/image: Coolify builds repository Dockerfile
- redeploy required after config changes: yes

## Verification

- image build: pass
- startup: pass
- DB connectivity: pass
- migration: pass
- health: pass
- public HTTPS: pass
- restart/redeploy: pass without durable data loss

## Troubleshooting

- DNS: public A/AAAA record must point to the address that reaches the Coolify server/proxy
- 404/proxy: verify domain assignment, service, internal port, bind address and app route
- startup: inspect container logs and required runtime variables
- database: verify internal host, credentials and PostgreSQL service health

## Live verification status

verified
