# Configuration – Example

## Overview

This service runs as a stateless container in Coolify and uses external PostgreSQL.

## Runtime variables

| Variable | Required | Secret | Default | Description |
|---|---|---|---|---|
| `PORT` | no | no | `8080` | Internal application port |
| `PUBLIC_BASE_URL` | yes | no | - | Public HTTPS base URL |
| `DATABASE_URL` | yes | no | - | PostgreSQL connection URL |
| `DATABASE_USER` | yes | no | - | Application DB user |
| `DATABASE_PASSWORD` | yes | yes | - | Application DB password |

## Secrets

`DATABASE_PASSWORD` is configured in Coolify runtime secrets. No real value is stored in repository files.

## Defaults

`PORT` defaults to `8080`. Other required values have no application default.

## Environment-specific behavior

Local development may use a local PostgreSQL instance. Production uses the external PostgreSQL service.

## External services

- external PostgreSQL
- GitHub API

## Validation / startup behavior

Startup fails with a clear configuration error if required DB configuration is missing. Secret values are not printed.

## Example configuration

```text
PORT=8080
PUBLIC_BASE_URL=https://example.apps.example.org
DATABASE_URL=jdbc:postgresql://postgres:5432/app
DATABASE_USER=app
DATABASE_PASSWORD=<secret>
```
