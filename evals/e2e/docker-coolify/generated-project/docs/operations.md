# Operations

## Service overview
Stateless app container in Coolify with external PostgreSQL.

## Health
`/health`, expected HTTP 200.

## Logs
stdout/stderr via Coolify.

## Start / stop / restart
Use Coolify service controls.

## Redeploy / upgrade
Redeploy after app, domain or runtime configuration changes.

## Database operations
Operate PostgreSQL as a separate service.

## Backup / restore
Database backup/restore belongs to the PostgreSQL service/platform.

## Migrations
No migrations in this eval fixture.

## Rollback
Deploy the previous versioned image/source revision.

## Troubleshooting
For 404 check DNS, domain assignment, service, port 8080, bind address `0.0.0.0`, health and application route.

## Known operational limitations
Live Coolify deployment is not available in this eval environment and must remain pending.
