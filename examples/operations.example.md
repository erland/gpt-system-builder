# Operations – Example

## Service overview

Stateless application container in Coolify with external PostgreSQL.

## Health

Use `/q/health`. HTTP 200 means the application reports healthy without exposing secret details.

## Logs

Read application stdout/stderr through Coolify container logs. Do not log passwords, tokens or private keys.

## Start / stop / restart

Use the Coolify service controls. A restart must not lose durable application data because persistent state is stored in PostgreSQL.

## Redeploy / upgrade

Redeploy after changes to domain, runtime environment variables, Docker configuration or application version. Re-run health and core smoke checks.

## Database operations

Use the external PostgreSQL service. Application credentials should use least privilege.

## Backup / restore

Use the database platform's configured backup mechanism. For restore, isolate application traffic if required, restore the chosen backup, verify schema/data, then start/redeploy the application and check health.

## Migrations

Run Flyway according to the release procedure. If a migration fails, inspect migration logs and database state before retrying.

## Rollback

Deploy the previous image/application version. If the failed release included a non-backwards-compatible migration, restore the appropriate PostgreSQL backup according to the recovery plan.

## Troubleshooting

### Public URL returns 404

Check:
1. public DNS target,
2. Coolify domain assignment,
3. selected service,
4. internal port `8080`,
5. bind address `0.0.0.0`,
6. application route.

### Application is unhealthy

Check:
- container logs,
- required runtime variables,
- database connectivity,
- migration state.

### Database connection fails

Check:
- internal DB hostname,
- network/service state,
- credentials,
- PostgreSQL health.

## Known operational limitations

The example assumes one stateless application service and no persistent local file storage.
