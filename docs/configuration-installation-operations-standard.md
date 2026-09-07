# System Builder – Configuration, installation och operations-dokumentation

## 1. Syfte

System Builder ska lämna ett system som går att förstå, konfigurera, installera och driva utan att användaren behöver förlita sig på chat history.

Tre canonical current-state-dokument används när relevant:

- `docs/configuration.md`
- `docs/installation.md`
- `docs/operations.md`

Dessa dokument beskriver systemets nuvarande leverans- och driftkontrakt.

## 2. Grundprincip

> Dokumentera vad operatören behöver göra och veta, inte implementationens interna detaljer.

Information ska inte dupliceras i flera dokument utan tydlig anledning.

## 3. Ansvarsfördelning

### configuration.md

Svarar på:
- vilka runtime-inställningar finns?
- vilka är required/optional?
- vilka är secrets?
- vilka defaults finns?
- hur påverkar inställningen systemet?

### installation.md

Svarar på:
- vilka prerequisites krävs?
- hur installeras/startas systemet?
- hur ansluts externa tjänster?
- hur verifieras installationen?

### operations.md

Svarar på:
- hur övervakas och felsöks systemet?
- hur startas/restartas/redeployas det?
- hur hanteras backup/restore?
- hur körs migrationer?
- hur görs rollback?
- vilka vanliga incidenter finns?

## 4. Current-state-regel

Dokumenten ska beskriva **nuvarande avsedda system**.

Historiska beslut hör hemma i:
- ADR,
- product decisions,
- change history.

Undvik:
- "förr gjorde vi..."
- gamla env-var-namn
- stale installation steps.

## 5. Configuration – struktur

`docs/configuration.md` ska normalt innehålla:

```text
# Configuration
## Overview
## Runtime variables
## Secrets
## Defaults
## Environment-specific behavior
## External services
## Validation / startup behavior
## Example configuration
```

## 6. Runtime variables

Varje relevant variabel bör beskrivas med:

- namn,
- required/optional,
- type/format,
- default,
- secret: yes/no,
- purpose,
- example utan riktiga credentials.

Exempel:

| Variable | Required | Secret | Default | Description |
|---|---|---|---|---|
| `PORT` | no | no | `8080` | Internal listen port |
| `DATABASE_URL` | yes | no | - | PostgreSQL connection URL |
| `DATABASE_PASSWORD` | yes | yes | - | DB password |

## 7. Secrets

Secrets ska aldrig dokumenteras med verkliga värden.

Dokumentera:
- secret name,
- var den konfigureras,
- rotation ownership där relevant,
- beroende mellan secrets och funktion.

## 8. `.env.example`

När `.env`-modell används bör `.env.example` finnas.

Regler:
- säkra placeholders,
- inga riktiga tokens/passwords,
- endast aktuella canonical variable names.

## 9. Defaults

Defaults ska dokumenteras endast när de faktiskt finns i code/config.

System Builder ska inte fabricera defaults för att göra dokumentationen snygg.

## 10. Environment differences

Beskriv endast verkliga skillnader mellan local/test/prod.

Undvik olika kodbranches som miljöstrategi.

## 11. Installation – struktur

`docs/installation.md` ska normalt innehålla:

```text
# Installation
## Prerequisites
## Obtain/build artifact
## Configure runtime
## External services
## Database setup/migrations
## Start/deploy
## Verify installation
## Upgrade
## Uninstall/remove
```

## 12. Prerequisites

Exempel:
- Docker,
- Java,
- Node,
- PostgreSQL,
- Coolify access,
- GitHub integration.

Versionskrav ska vara explicit när de påverkar compatibility.

## 13. Build/install commands

Kommandon ska vara körbara och motsvara repositoryts faktiska tooling.

Undvik pseudokommandon om riktig command finns.

## 14. External services

Installation ska beskriva hur beroenden etableras på lämplig nivå:

- PostgreSQL,
- identity provider,
- GitHub integration,
- object storage.

Secrets dokumenteras genom namn/placering, inte värde.

## 15. Database installation

När DB används:

- skapa/provisionera DB,
- anslut app,
- kör migrations enligt canonical strategi,
- verifiera schema/connectivity.

## 16. Docker installation

När Docker används:

- build image,
- set runtime config,
- start container,
- verify health.

Om image kommer från registry:
- pull rätt version/tag.

## 17. Coolify installation

När Coolify används ska installationen kunna beskriva:

1. skapa app/service,
2. koppla Git repo eller registry image,
3. skapa/anslut external PostgreSQL,
4. konfigurera runtime vars/secrets,
5. ange internal port/health,
6. sätt domain,
7. deploy,
8. verifiera HTTPS/health.

## 18. Verification after install

Installation är inte klar förrän relevant verifiering passerar.

Exempel:
- health 200,
- login works,
- DB connectivity,
- core flow smoke test.

## 19. Upgrade

Dokumentera när relevant:

- backup före upgrade,
- migration order,
- new env vars,
- image/version change,
- post-upgrade verification.

## 20. Operations – struktur

`docs/operations.md` ska normalt innehålla:

```text
# Operations
## Service overview
## Health
## Logs
## Start / stop / restart
## Redeploy / upgrade
## Database operations
## Backup / restore
## Migrations
## Rollback
## Troubleshooting
## Known operational limitations
```

## 21. Health

Beskriv:
- endpoint,
- expected status,
- vad health faktiskt betyder,
- var operatören ser status.

## 22. Logs

Beskriv:
- var logs finns,
- vilka identifiers som underlättar felsökning,
- att secrets inte ska loggas,
- exempel på relevanta felkategorier.

## 23. Start / stop / restart

Beskriv faktiska commands eller plattformsåtgärder.

Exempel:
- Docker command,
- Coolify restart,
- Kubernetes rollout restart.

## 24. Redeploy

Beskriv:
- när redeploy krävs,
- vilka ändringar som triggar rebuild,
- hur man verifierar ny deployment.

## 25. Backup

Backup ownership ska vara explicit.

För PostgreSQL:
- vem/plattform gör backup?
- frekvens/policy om definierad,
- hur verifieras backup?
- var restore-procedur finns?

System Builder ska inte hitta på retention policy.

## 26. Restore

Restore-procedur ska:
- identifiera backup,
- stoppa/isolera app vid behov,
- återställa,
- verifiera schema/data,
- verifiera app health.

## 27. Migrations

Operations ska beskriva hur migrations:
- startas,
- observeras,
- felsöks,
- hanteras vid failure.

## 28. Rollback

Rollback ska minst beskriva:
- previous application version/image,
- config rollback,
- DB restore om migration inte är backwards compatible.

## 29. Troubleshooting

Troubleshooting ska ordnas efter observerbart symptom.

Exempel:

### App starts but 404
- domain/proxy
- internal port
- bind address
- app route

### App unhealthy
- logs
- required env
- DB connectivity
- migration state

### DB connection failure
- host/network
- credentials
- DB service health
- TLS requirements.

## 30. Coolify troubleshooting

Coolify-specifika cases kan inkludera:
- DNS mismatch,
- pending redeploy after domain/env change,
- 404 through proxy,
- wrong internal port,
- app bound to localhost,
- DB service unavailable.

## 31. Known limitations

Operations ska dokumentera verkliga driftbegränsningar.

Exempel:
- single instance only,
- no durable file uploads,
- manual DB restore,
- live deployment verification pending.

## 32. Security

Dokumentation får inte:
- exponera secrets,
- föreslå osäkra defaults,
- instruera public DB exposure utan behov,
- innehålla verkliga private keys/tokens.

## 33. Duplication rules

Canonical ownership:

- variable definitions → configuration.md
- install sequence → installation.md
- day-2 operations → operations.md
- deployment architecture → architecture/deployment profile
- historical rationale → ADR/product decisions/change history.

Andra dokument länkar i stället för att duplicera detaljer.

## 34. Small project

Small-projekt får kombinera dokument om det tydligt förbättrar användbarheten.

Till exempel:
- `docs/runbook.md`

Men informationstyperna configuration/install/operations ska fortfarande kunna identifieras.

## 35. Medium / large

Medium/large bör normalt ha separata dokument eftersom ansvar och förändringstakt skiljer sig.

## 36. CREATE

CREATE ska producera dokumenten före release readiness när systemet är deployable.

## 37. CHANGE

CHANGE ska uppdatera dokument om ändringen påverkar:
- config,
- installation,
- migration,
- deployment,
- operations.

## 38. IMPROVE

IMPROVE uppdaterar dem bara om teknisk drift/konfiguration faktiskt förändras.

## 39. Drift detection

System Builder ska upptäcka stale docs när:
- env var finns i code men saknas i docs,
- docs refererar borttagen var,
- port mismatch,
- health path mismatch,
- deployment profile och installation motsäger varandra.

## 40. Validation

En strukturell validator kan verifiera:
- required sections,
- tabellstruktur,
- inga obvious secretvärden,
- Coolify-sektion när profil används.

Semantisk consistency måste fortfarande bedömas mot faktisk code/config.

## 41. Release readiness

Release readiness ska blockeras om:
- required runtime config är odokumenterad,
- install inte går att följa,
- rollback/migration för riskfylld deployment saknas,
- operations saknar kritisk recovery information.

## 42. Anti-patterns

Undvik:
- README som enda runbook för komplext system,
- verkliga secrets i exempel,
- env vars utan beskrivning,
- installation utan verification,
- operations utan rollback,
- duplicerade variable lists i flera docs,
- historiska steg i current-state runbook.

## 43. Exit-kriterier för SB-27

SB-27 är klart när:
- configuration/install/operations ownership definierats,
- canonical strukturer finns,
- Coolify/Docker/PostgreSQL patterns täcks,
- duplication/current-state-regler finns,
- templates och example set finns,
- validator finns.
