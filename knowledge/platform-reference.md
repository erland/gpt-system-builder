# Platform Reference

Class: reference

## GitHub

Repository, branch, pull request, commit och CI används som delivery state när GitHub-läge är valt. Canonical regler finns i `docs/github-mode.md`.

## Docker

Docker/OCI används som packagingform. Canonical regler finns i `docs/docker-baseline.md`.

## Coolify

Coolify kan köra app containers och separata databastjänster. Canonical målprofil finns i `docs/coolify-profile.md`. Produktdetaljer som kan ändras över tid ska verifieras mot aktuell dokumentation.

## PostgreSQL

Relationsdatabas körs normalt separat från app image. Migrations hör till applikationens releasecontract.

## Generic container platform

Anta inte plattformsspecifika capabilities utan verifiering. Beskriv image, config, secrets, health, persistence och rollout explicit.
