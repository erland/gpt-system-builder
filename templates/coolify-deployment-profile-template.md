# Coolify Deployment Profile

## Profile

coolify-external-postgresql

## Application

- artifact:
- Dockerfile:
- internal port:
- bind address:
- stateless:
- runtime user:

## Database

- type: external PostgreSQL
- provisioned by:
- connection model:
- public exposure: no

## Runtime configuration

### Non-secret
- ...

### Secrets
- ...

## Domain / proxy / TLS

- public hostname:
- public base URL:
- reverse proxy owner: Coolify
- TLS owner: Coolify

## Health

- path:
- expected status:
- configured in Coolify:

## Persistence

- database:
- volumes:
- temporary files:

## Migrations

- strategy:
- rollback/restore:

## Build / deploy

- source: Git / registry
- build command/image:
- redeploy required after config changes: yes

## Verification

- image build:
- startup:
- DB connectivity:
- migration:
- health:
- public HTTPS:
- restart/redeploy:

## Troubleshooting

- DNS:
- 404/proxy:
- startup:
- database:

## Live verification status

verified / pending
