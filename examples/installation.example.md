# Installation – Example

## Prerequisites

- Coolify access
- Git repository containing the application
- Dockerfile-compatible build
- PostgreSQL service

## Obtain/build artifact

Connect the Git repository in Coolify and configure Coolify to build the repository Dockerfile.

## Configure runtime

Configure the runtime variables and secrets described in `configuration.example.md`.

## External services

Create or select a separate PostgreSQL service. Keep it private/internal unless there is a documented reason for public exposure.

## Database setup/migrations

Set the PostgreSQL connection variables and run the release's Flyway migration procedure before routing production traffic.

## Start/deploy

Set the internal application port to `8080`, configure `/q/health`, assign the public domain and deploy the service.

## Verify installation

Verify:
- container startup,
- PostgreSQL connectivity,
- migration success,
- `/q/health` returns HTTP 200,
- public HTTPS URL reaches the application.

## Upgrade

Before a migration with compatibility risk, create/verify a database backup. Deploy the new versioned image/source and run post-upgrade health and smoke checks.

## Uninstall/remove

Remove the application service separately from persistent PostgreSQL data. Delete the database only when its data is intentionally no longer required.
