# System Builder Knowledge Bundle

Class: reference

---

## Source: `docs/deployment-packaging-patterns.md`

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

---

## Source: `docs/docker-baseline.md`

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

---

## Source: `docs/coolify-profile.md`

# System Builder – Coolify-profil

## 1. Syfte

Coolify-profilen definierar hur System Builder ska designa, paketera, konfigurera och verifiera en applikation som ska köras i Coolify.

Profilen bygger på Docker-baslinjen men gör målplattformens ansvar explicit.

## 2. Grundprincip

> Appen är en containeriserad tjänst. Databas, reverse proxy, TLS och runtime-konfiguration hanteras separat av plattformen.

## 3. Canonical profil

Profil-ID:

`coolify-external-postgresql`

Använd när:
- applikationen körs i Coolify,
- relationsdata lagras i PostgreSQL,
- PostgreSQL körs som separat Coolify-databastjänst eller annan extern PostgreSQL,
- appen distribueras som Docker/OCI-image.

## 4. App image

App image ska:

- innehålla applikation + runtime,
- inte innehålla PostgreSQL-server,
- vara stateless där praktiskt,
- köra non-root där praktiskt,
- lyssna på en tydlig intern port,
- ha health endpoint,
- ta runtime config från environment/secrets.

## 5. PostgreSQL

PostgreSQL ska köras separat.

Tillåtna patterns:
- Coolify Database service,
- annan extern PostgreSQL-tjänst.

Inte tillåtet:
- PostgreSQL installerad i app image,
- implicit SQLite som ersätter avsedd PostgreSQL utan explicit arkitekturbeslut.

## 6. Databasanslutning

Appen ska konfigureras via exempelvis:

- `DATABASE_URL`,
- `DATABASE_HOST`,
- `DATABASE_PORT`,
- `DATABASE_NAME`,
- `DATABASE_USER`,
- `DATABASE_PASSWORD`.

Exakt modell styrs av stack.

Credentials ska vara runtime secrets.

## 7. Databasnätverk

Föredra privat/intern anslutning mellan app och DB.

PostgreSQL ska normalt inte exponeras publikt mot Internet.

Publik DB-exponering kräver explicit behov och security review.

## 8. Reverse proxy

Coolify hanterar normalt reverse proxy.

Appen ska:
- lyssna på intern port,
- inte själv terminera publik TLS som default,
- acceptera forwarded host/proto korrekt om framework kräver konfiguration.

## 9. TLS

Coolify äger normalt TLS-certifikat och HTTPS-terminering.

Appen kör normalt HTTP internt bakom proxy.

Undvik dubbel TLS-terminering om inget specifikt krav finns.

## 10. Domain

Domän konfigureras i Coolify.

System Builder ska dokumentera:

- public hostname,
- public base URL,
- internal app port,
- callback/redirect URLs,
- CORS/origin implications.

DNS måste peka mot den externa adress som faktiskt leder till Coolify-instansen.

## 11. DNS

Coolify kan rapportera DNS mismatch om resolver/instans ser annan adress än den publika DNS-konfigurationen.

System Builder ska skilja mellan:

- publik DNS record,
- intern/private IP,
- Coolify server public IP,
- proxy/domain configuration.

Den ska inte anta att en intern IP är korrekt publik DNS target.

## 12. Internal port

Appens interna port ska vara konsekvent mellan:

- application runtime,
- Dockerfile,
- Coolify service configuration,
- health check.

Exempel:
`8080`.

## 13. Port exposure

Appporten behöver normalt inte publiceras direkt till Internet.

Coolify proxy routar trafik till intern serviceport.

Undvik extra host port mappings om plattformen inte kräver dem.

## 14. Health check

Health endpoint ska:

- vara utan authentication om plattformen behöver nå den internt,
- inte läcka secrets,
- vara snabb,
- returnera korrekt statuskod.

Exempel:
- `/health`
- `/q/health`
- `/actuator/health`

## 15. Health ownership

Coolify konfigureras med appens health endpoint.

Dockerfile `HEALTHCHECK` kan användas, men System Builder ska undvika konflikt mellan Docker- och Coolify-health.

## 16. Runtime environment

Runtime config ska sättas i Coolify environment configuration.

Kategorier:

### Non-secret
- `PUBLIC_BASE_URL`
- `LOG_LEVEL`
- `PORT`

### Secret
- `DATABASE_PASSWORD`
- API tokens
- OAuth client secrets
- private keys

## 17. SERVICE_FQDN / SERVICE_URL

Coolify kan generera service-relaterade environment variables beroende på service-setup.

System Builder ska:

- inte anta att auto-genererade variabler motsvarar appens egna canonical config names,
- dokumentera vilka variabler appen faktiskt läser,
- mappa plattformsvariabler endast medvetet.

## 18. Rebuild/redeploy

Ändringar i:

- domains,
- environment variables,
- Docker configuration,
- service linkage,

kan kräva redeploy/rebuild.

System Builder ska behandla "changes pending / deploy again to apply" som faktisk deployment-state, inte som kosmetisk UI-warning.

## 19. 404 efter domain-konfiguration

Vid 404 ska System Builder kontrollera i ordning:

1. DNS target,
2. Coolify domain assignment,
3. service selected for domain,
4. app internal port,
5. app bind address (`0.0.0.0`),
6. health/startup,
7. reverse proxy route,
8. application base path/routes.

Den ska inte direkt anta applikationsbugg.

## 20. Bind address

Containerappen ska normalt lyssna på `0.0.0.0`.

`localhost`/`127.0.0.1` inuti containern gör att proxy ofta inte kan nå tjänsten.

## 21. Stateless runtime

Appen ska normalt vara stateless.

Persistenta data ska ligga i:
- PostgreSQL,
- object storage,
- explicit volume.

## 22. Volumes

Lägg bara till persistent volume när appen faktiskt behöver durable files.

Dokumentera:
- mount path,
- ownership/permissions,
- backup,
- restore,
- multi-instance behavior.

## 23. Temporary files

Temporära filer kan ligga lokalt i container om de:
- kan återskapas,
- rensas,
- inte behöver överleva restart/redeploy.

## 24. Migrations

Migrationsstrategi ska vara explicit.

Patterns:

### Startup migration
Passar låg/medelrisk när framework hanterar det säkert.

### Pre-deploy/release command
Passar högre kontrollbehov.

### Manual migration
Passar high-risk/irreversible changes.

## 25. Migration safety

Vid riskfyllda schemaändringar:
- backup före migration,
- compatibility-bedömning,
- rollback/restore,
- verifiering mot representativ databas.

## 26. Startup dependencies

Appen ska hantera att PostgreSQL kan vara tillfälligt otillgänglig vid startup.

Använd:
- retries/backoff där framework stöder det,
- tydliga startup errors,
- readiness som visar faktisk tillgänglighet.

Undvik hårda fixed sleeps.

## 27. Logging

Logga till stdout/stderr.

Coolify/plattformen visar containerlogs.

Loggar ska inte innehålla:
- DB password,
- tokens,
- full private keys.

## 28. Restart behavior

Appen ska kunna startas om utan manuell lokal state.

Restart ska inte:
- förstöra persistent data,
- kräva handredigerade filer i container.

## 29. Graceful shutdown

Appen bör hantera SIGTERM och stänga DB connections/arbete ordnat när framework stöder det.

## 30. Image build

Image kan byggas:

- direkt av Coolify från Git repository,
- från Dockerfile,
- från pre-built registry image.

System Builder ska följa vald project setup.

## 31. Git repository deployment

Vid Git-baserad deployment ska repository innehålla:

- Dockerfile eller kompatibel build definition,
- `.dockerignore`,
- source,
- build config,
- inga secrets.

## 32. Registry deployment

Vid pre-built image:
- image tag ska vara versionerad,
- registry auth hanteras av Coolify/CI,
- rollback ska kunna peka på föregående tag.

## 33. Environment-specific config

Skillnader mellan dev/test/prod ska ligga i Coolify/environment config, inte olika kodbranches.

## 34. CORS

Om frontend och backend har olika origins ska CORS vara explicit.

Wildcard CORS ska undvikas för authenticated APIs utan tydligt behov.

## 35. OAuth / callbacks

Public base URL och redirect URI måste matcha faktisk Coolify domain/HTTPS URL.

Vid domain change ska externa identity provider callback settings också bedömas.

## 36. WebSockets / streaming

Om appen använder WebSockets/SSE ska System Builder verifiera att proxy och appkonfiguration stödjer det.

## 37. File upload limits

För upload-appar ska gränser bedömas i:

- app,
- reverse proxy/plattform,
- eventuell ingress.

## 38. Coolify deployment verification

Minst när profil används:

1. Docker image build: PASS.
2. Container startup: PASS.
3. App lyssnar på rätt port/bind.
4. External PostgreSQL connectivity: PASS.
5. Migrations: PASS.
6. Health: PASS.
7. Public domain via Coolify proxy/TLS: PASS.
8. Secrets externalized.
9. Restart/redeploy: ingen dataförlust av durable state.

## 39. Static fallback

Om Coolify-instans inte kan nås i aktuell körning ska System Builder:

- validera Docker/profile config strukturellt,
- kontrollera env contract,
- kontrollera port/health/migration assumptions,
- markera live deployment verification som pending.

Den får inte påstå att Coolify-deploy fungerar utan live evidence.

## 40. Configuration documentation

`docs/configuration.md` ska för Coolify beskriva:

- required env vars,
- secret vs non-secret,
- internal port,
- DB settings,
- public base URL,
- health path,
- optional volume settings.

## 41. Installation documentation

`docs/installation.md` ska senare kunna beskriva:

- create app/service,
- connect Git or registry,
- create/connect PostgreSQL,
- configure env/secrets,
- set domain,
- deploy,
- verify health.

## 42. Operations documentation

`docs/operations.md` ska senare täcka:

- logs,
- restart,
- redeploy,
- health,
- DB backup/restore,
- migrations,
- rollback,
- common domain/proxy issues.

## 43. Security baseline

Coolify-profilen ska följa:

- no secrets in repo/image,
- external PostgreSQL,
- private DB network där möjligt,
- platform-managed TLS,
- minimum exposed ports,
- non-root app runtime,
- safe health endpoint.

## 44. CREATE

CREATE med Coolify target ska etablera profilen före slutligt arkitekturval.

## 45. CHANGE

CHANGE ska bedöma om förändringen kräver:

- ny env var,
- domain/callback change,
- migration,
- volume,
- port,
- health,
- redeploy.

## 46. IMPROVE

IMPROVE kan förbättra:
- image size,
- non-root,
- health,
- config externalization,
- startup reliability,
- deployment docs.

## 47. Release readiness

Coolify release readiness kräver:

- versionerad artifact/source,
- Docker verifierad,
- env contract komplett,
- DB/migration strategy verifierad,
- domain/TLS health verifierad eller explicit pending live check,
- rollback dokumenterad.

## 48. Anti-patterns

Undvik:

- PostgreSQL i app image,
- public DB port utan behov,
- hardcoded domain i source när config räcker,
- app som bara lyssnar på localhost,
- secrets i `.env` committed,
- persistent uploads i ephemeral filesystem,
- egen TLS inuti app utan behov,
- host port mapping som kringgår proxy,
- anta att "deploy finished" betyder app health PASS.

## 49. Exit-kriterier för SB-26

SB-26 är klart när:

- Coolify + external PostgreSQL pattern är explicit,
- domain/DNS/proxy/TLS ansvar definieras,
- port/bind/health definieras,
- env/secrets och SERVICE_*-princip definieras,
- migrations/storage/restart definieras,
- troubleshooting för domain/404 finns,
- live-vs-static verification är tydlig,
- profile template/example/validator finns.
