# System Builder – Deployment- och packagingmönster

## Syfte

System Builder ska välja den enklaste deployment- och packagingform som uppfyller systemets krav och målmiljö. Deployment behandlas tidigt när det påverkar arkitektur, persistens, nätverk, secrets, startup, health, databas, rollback eller driftansvar.

## Canonical deploymentprofiler

1. **local development** – reproducerbar lokal start, dependencies, lokal config och tests.
2. **Docker standalone** – en containeriserad tjänst med port, health och runtime config.
3. **Docker + external PostgreSQL** – stateless app image och separat PostgreSQL.
4. **Coolify + external PostgreSQL** – app som Docker/OCI image, separat DB, Coolify äger normalt reverse proxy/TLS och environment/secrets.
5. **generic container platform** – image, port, health, persistence och external services uttrycks plattformsneutralt.
6. **basic Kubernetes** – Deployment, Service, config/secrets, readiness/liveness, resources och optional Ingress när Kubernetes faktiskt krävs.

## Packaging contract

Packaging ska ange:

- release artifact type,
- build command,
- version source,
- canonical inputs,
- generated exclusions,
- artifact verification.

Exempel är OCI image, executable JAR, static frontend bundle, Python wheel och source ZIP.

## Reproducibility

Artefakten ska så långt möjligt kunna byggas från source, lockfiles, explicita runtime/tool versions och dokumenterade commands. Lokala caches eller manuellt ändrade generated files får inte vara nödvändiga.

## Build-time och runtime configuration

Miljöspecifik configuration ska normalt ligga utanför artifact. Server-side secrets ska vara runtime configuration och aldrig byggas in i artifact.

## Environment variables

När env vars används ska `docs/configuration.md` senare beskriva namn, required/optional, format, default, secret/non-secret och säkra exempel.

## Ports och health

Deployable services ska ha tydlig listen-port och normalt health endpoint. Health får inte läcka secrets. Kubernetes kan skilja liveness och readiness; enklare Docker/Coolify kan använda en gemensam health check.

## Stateless och persistens

Web/API-tjänster bör vara stateless där praktiskt. Durable data ska ligga i databas, object storage eller explicit persistent volume. Lokalt containerfilesystem är ephemeral om inte annat är uttryckligen konfigurerat.

## PostgreSQL

PostgreSQL-server ska normalt inte ligga i app image. Appen ansluter till en separat databas med least-privilege credentials. Backup/restore ownership ska vara tydligt.

## Migrationer

Migrations följer appens releasecontract men servern ligger externt. Välj explicit mellan startup migration, separat migration command/job eller kontrollerad manuell migration. High-risk migration ska ha rollback/restore-strategi.

Vid större changes kan expand/contract användas för backwards compatibility.

## Coolify

För `coolify-external-postgresql` gäller:

- appen är Docker/OCI image,
- PostgreSQL är separat Coolify DB service eller annan extern PostgreSQL,
- app image innehåller inte PostgreSQL-server,
- reverse proxy/TLS hanteras normalt av Coolify,
- secrets och runtime config sätts i plattformen,
- health endpoint konfigureras,
- persistent volume används bara vid verkligt filpersistensbehov.

## Reverse proxy, TLS och domains

Ownership ska vara explicit. På Coolify äger plattformen normalt proxy/TLS. Domain/base URL/callback URLs/CORS ska behandlas som deployment config.

## Secrets

Secrets tillförs via platform secret store, environment, Kubernetes Secret eller external secret manager. De får inte ligga i Dockerfile, committed `.env.production` eller source literals.

## Logging och observability

Containeriserade tjänster loggar normalt till stdout/stderr. Minsta operability är meaningful logs, health och tydliga startup errors. Metrics/tracing läggs till efter behov.

## Images

Använd versions-/commitkopplade tags. `latest` får inte vara enda production identifier. Multi-stage builds och non-root runtime används där praktiskt.

## Architecture- och testkoppling

Deployment profile och architecture måste vara konsistenta. Deployment verification ska ingå i test strategy när deployment är del av release.

Typisk verification:

- image/artifact build,
- startup,
- health,
- DB connectivity,
- migrations,
- runtime configuration.

## CREATE, CHANGE och IMPROVE

**CREATE:** välj profil innan arkitekturen låses när target är känd; använd tidig deployment proof om den reducerar risk.

**CHANGE:** bedöm påverkan på env vars, ports, migrations, storage, image, health, domains och auth callbacks.

**IMPROVE:** kan omfatta mindre image, multi-stage, non-root, bättre health och externalized config utan funktionell förändring.

## Release readiness

Kontrollera:

- artifact är byggbar,
- deployment config är komplett,
- secrets är externalized,
- migration strategy finns,
- health fungerar,
- rollback/restore finns på rätt nivå,
- installation/operations docs är aktuella.

## Rollback

Minsta rollback kan vara previous image tag, config revert och DB restore vid destruktiv migration.

## Selection guide

- Local-only tool → `local-development`
- Small API utan DB → `docker-standalone`
- Web/API med relationspersistens → `docker-external-postgresql`
- Coolify target → `coolify-external-postgresql`
- Okänd managed container platform → `generic-container-platform`
- Explicit Kubernetesbehov → `kubernetes-basic`

## Anti-patterns

Undvik PostgreSQL i app image, secrets i image, implicit lokal containerpersistens, Kubernetes utan behov, endast `latest`, saknad health, deployment som motsäger architecture och artifacts som bara kan byggas på en specifik utvecklares maskin.
