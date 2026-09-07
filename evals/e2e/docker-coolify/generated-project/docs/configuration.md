# Configuration

## Overview
Coolify runtime configuration for the application.

## Runtime variables

| Variable | Required | Secret | Default | Description |
|---|---|---|---|---|
| `PORT` | no | no | `8080` | Internal application port |
| `DATABASE_URL` | yes | no | - | External PostgreSQL URL |
| `DATABASE_USER` | yes | no | - | PostgreSQL user |
| `DATABASE_PASSWORD` | yes | yes | - | PostgreSQL password |
| `PUBLIC_BASE_URL` | yes | no | - | Public HTTPS base URL |

## Secrets
`DATABASE_PASSWORD` is configured in Coolify, never committed.

## Defaults
`PORT=8080`.

## Environment-specific behavior
Production uses external PostgreSQL and Coolify-managed routing/TLS.

## External services
External PostgreSQL.

## Validation / startup behavior
Required DB configuration must be present before DB-backed features are enabled.

## Example configuration
See `.env.example`; replace placeholders in runtime secret configuration.
