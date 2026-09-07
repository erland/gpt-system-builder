# Installation

## Prerequisites
- Coolify access
- Git repository or registry image
- External PostgreSQL service

## Obtain/build artifact
Build the repository Dockerfile or use a versioned OCI image.

## Configure runtime
Set variables from `configuration.md` in Coolify.

## External services
Provision PostgreSQL separately and keep it private/internal where possible.

## Database setup/migrations
No schema migration is required for this eval fixture.

## Start/deploy
Configure internal port `8080`, health path `/health`, domain and deploy.

## Verify installation
Verify image build, container startup, external PostgreSQL connectivity when DB-backed functionality is enabled, health HTTP 200 and public HTTPS through Coolify.

## Upgrade
Deploy a versioned image/source revision and rerun health checks.

## Uninstall/remove
Remove app separately from durable PostgreSQL data.
