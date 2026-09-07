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
