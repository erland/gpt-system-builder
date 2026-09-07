# Deployment and Packaging Plan – Example

## Target profile

coolify-external-postgresql

## Release artifact

- type: OCI/Docker image
- build command: `docker build -t example-service:${VERSION} .`
- version source: Git release tag

## Runtime

- runtime: Java 21
- internal port: 8080
- stateless: yes
- runtime user: non-root application user

## Configuration

### Runtime variables
- `DATABASE_URL`
- `DATABASE_USER`
- `PUBLIC_BASE_URL`

### Secrets
- `DATABASE_PASSWORD`
- `GITHUB_APP_PRIVATE_KEY`

## Persistence

- database: external PostgreSQL service
- files: temporary only
- external storage: none in first release

## Migration strategy

Flyway migrations ship with the application and run as a controlled pre-start/release step.

## Health / readiness

- health endpoint: `/q/health`
- readiness: application ready without secret details
- liveness: process/application health

## Proxy / TLS / domain

- proxy owner: Coolify
- TLS owner: Coolify
- hostname/base URL: configured per environment

## External services

- external PostgreSQL
- GitHub API

## Packaging verification

- Docker image builds
- no secrets in image layers
- application runs as non-root

## Deployment verification

- container starts
- external PostgreSQL connection succeeds
- migrations succeed
- health endpoint reports ready
- public URL works through Coolify proxy/TLS

## Rollback / restore

Deploy previous image tag. Restore database backup if a non-compatible migration must be reverted.

## Operations ownership

Coolify owns reverse proxy/TLS and service restart. Application operations documentation owns environment variables, health and migration procedures.
