# System Builder – Docker-baslinje

## Syfte
Docker-baslinjen definierar en säker, reproducerbar och driftbar OCI/Docker-leverans när container är vald deploymentform.

## Grundprincip
> App image innehåller applikation och runtime – inte databasserver, secrets eller miljöspecifik driftstate.

## Dockerfile
Dockerfile ska normalt använda explicit base image-version, `WORKDIR`, multi-stage när buildverktyg inte behövs i runtime, begränsad `COPY`, non-root runtime där praktiskt och exec-form `ENTRYPOINT`/`CMD`.

## Base images
Använd etablerade images och explicit version/tag. Undvik `latest` som enda versionsstyrning. Välj kompatibilitet och underhållbarhet framför onödigt minimal image.

## Multi-stage
Separera build och runtime när det minskar storlek och attackyta. Endast byggresultatet kopieras till runtime stage.

## Non-root
Runtime ska normalt köra som non-root. Undantag ska vara motiverade.

## COPY och cache
Kopiera dependency manifests/lockfiles före source när det förbättrar cache. Undvik `COPY . /` utan starkt skäl.

## .dockerignore
Containerprojekt ska ha `.dockerignore` som minst skyddar `.git`, `.env`, lokala dependencies/build outputs, logs/temp och leveransarkiv. Required build inputs får inte ignoreras.

## Secrets
Secrets får inte ligga i Dockerfile, `ARG`, hårdkodad `ENV`, image layers eller frontend bundle. De tillförs vid runtime via plattform/environment/secret store.

## Runtime configuration
Miljöspecifik config kommer normalt från environment variables eller mounted config. Saknad required config ska ge tydligt fel utan secretvärden.

## Port och bind
Applikationen ska ha tydlig intern port och normalt lyssna på `0.0.0.0`. `EXPOSE` är metadata, inte publik portmappning.

## Health
Deployable services ska normalt ha snabb health endpoint utan känslig information. Dockerfile `HEALTHCHECK` används bara när det passar målplattformen; undvik dubbla motstridiga health definitions.

## Logging och filesystem
Logga normalt till stdout/stderr. Containerfilesystem antas ephemeral. Persistent files kräver explicit volume/external storage, ownership och backup/restore.

## PostgreSQL
PostgreSQL-server ska inte installeras i app image. Appen innehåller bara nödvändig klient/drivrutin och ansluter till extern PostgreSQL via runtime config/secrets.

## Migrations
Migrations kan ingå i app artifact men körs enligt vald strategi: startup, separat command/job eller kontrollerat release-steg. High-risk migrations kräver rollback/restore.

## Image identity
Använd semantic version, release tag eller commit SHA. `latest` får vara convenience men inte enda production identity. OCI labels för version/revision kan användas.

## Reproducibility
Använd lockfiles, explicit runtimeversion och canonical build commands. Build ska inte bero på en utvecklares lokala cache.

## Signals och shutdown
ENTRYPOINT/CMD ska låta SIGTERM nå applikationen. Servern bör avsluta graceful när framework stöder det.

## Docker Compose
Compose kan användas för local development/integration eller explicit standalone deployment. Lokal PostgreSQL i compose ändrar inte regeln att production app image och DB är separata.

## Coolify
För Coolify: Dockerfile bygger endast app; Coolify hanterar normalt domain/reverse proxy/TLS och runtime env/secrets; PostgreSQL är separat service; health endpoint används; appen bör vara stateless.

## Verification
När Docker finns ska minst image build, startup, health, runtime user och required config verifieras. Om Docker daemon saknas får strukturell validation användas, men System Builder får då inte påstå att image build/startup passerat.

## CREATE / CHANGE / IMPROVE
CREATE etablerar Docker tidigt om deploymentprofilen kräver det. CHANGE uppdaterar Docker när runtimekrav ändras. IMPROVE kan hårdna image med multi-stage, non-root, cache, health och externalized config utan funktionell förändring.

## Anti-patterns
Undvik `FROM ...:latest`, root runtime utan skäl, `COPY . /`, secrets via ENV/ARG, embedded PostgreSQL, implicit persistent data, loggfiler som primary logging, saknad `.dockerignore` och påstådd runtime-verifiering utan faktisk build.
