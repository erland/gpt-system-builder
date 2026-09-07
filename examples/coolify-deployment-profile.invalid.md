# Coolify Deployment Profile – Invalid

## Profile

coolify-external-postgresql

## Application

- artifact: Docker
- Dockerfile: Dockerfile
- internal port: 8080
- bind address: `127.0.0.1`
- stateless: no
- runtime user: root

## Database

- type: PostgreSQL
- provisioned by: app image
- connection model: localhost
- public exposure: yes

## Runtime configuration

### Non-secret
- PORT

### Secrets
- PASSWORD

## Domain / proxy / TLS

- public hostname: example.org
- public base URL: http://example.org
- reverse proxy owner: app
- TLS owner: app

## Health

- path: none
- expected status: none
- configured in Coolify: no

## Persistence

- database: local
- volumes: none
- temporary files: local

## Migrations

- strategy: none
- rollback/restore: none

## Build / deploy

- source: Git
- build command/image: Dockerfile
- redeploy required after config changes: yes

## Verification

- image build: unknown
- startup: unknown
- DB connectivity: unknown
- migration: unknown
- health: unknown
- public HTTPS: unknown
- restart/redeploy: unknown

## Troubleshooting

- DNS: none
- 404/proxy: none
- startup: none
- database: none

## Live verification status

pending
