# System Builder Knowledge Bundle

Class: reference

---

## Source: `docs/configuration-installation-operations-standard.md`

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

---

## Source: `docs/release-readiness-standard.md`

# System Builder – Release readiness och system acceptance

## 1. Syfte

Release readiness avgör om en given version faktiskt är redo att släppas.

System acceptance avgör om systemets avsedda beteende och kvalitetsnivå är tillräckligt verifierade för den aktuella releasen.

Ett grönt buildjobb är nödvändigt i många projekt men aldrig tillräckligt som enda releasebevis.

## 2. Grundprincip

> Release = uppfylld avsikt + verifierad kvalitet + driftbar leverans + inga blockerare.

## 3. Release readiness-domäner

System Builder ska bedöma minst följande när relevanta:

1. Scope completion
2. Functional acceptance
3. Non-functional acceptance
4. Verification / test evidence
5. Security
6. Risk / feasibility
7. Architecture consistency
8. Packaging
9. Deployment readiness
10. Configuration
11. Installation
12. Operations
13. Migration / rollback
14. Traceability
15. Repository hygiene
16. Known limitations
17. Version/release metadata

## 4. Must-scope

Alla Must-krav för releasen ska vara:

- implemented,
- verified,
- inte blockerade.

Should/Could får återstå om release scope tydligt säger det.

## 5. Acceptance criteria

Must-relaterade AC ska vara verifierade med:

- automated test,
- manual acceptance,
- eller kombination.

"Implemented" utan verifierad acceptance är inte fullt releaseklart.

## 6. Functional acceptance

System acceptance ska täcka de viktigaste användarflödena.

Exempel:
- core happy path,
- viktiga failure paths,
- authorization,
- persistence,
- external integrations.

## 7. Non-functional acceptance

När relevant:
- performance,
- security,
- availability,
- operability,
- scalability,
- compatibility.

NFR ska inte behandlas som prose-only om de är releasekritiska.

## 8. Test evidence

Release readiness ska sammanfatta:

- build,
- lint,
- typecheck,
- unit,
- integration,
- API,
- UI/e2e,
- security,
- deployment tests,
- manual acceptance.

Det är tillräckligt med outcome/evidence summary; full logg behöver inte dupliceras.

## 9. Required vs informational

Varje gate ska vara:

- required,
- informational.

Required failure blockerar release.

Informational warning kräver dokumenterad bedömning men blockerar inte automatiskt.

## 10. Security readiness

Minst:
- inga blockerande security findings,
- secrets externalized,
- auth/authz verifierad där relevant,
- critical security tests passerar,
- known critical vulnerabilities hanterade.

## 11. Risk readiness

Öppna risker ska vara:
- mitigated,
- accepted,
- eller explicit release-blocking.

Critical/high risk får inte tyst lämnas open.

## 12. Architecture consistency

Current-state architecture ska stämma med faktiskt system för releaserelevanta delar.

Stale architecture är blockerande när den gör deployment, security eller vidare change osäker.

## 13. Packaging readiness

Releaseartefakten ska:
- kunna byggas,
- ha tydlig version,
- kunna verifieras,
- inte innehålla secrets/temp-skräp,
- matcha delivery target.

## 14. Deployment readiness

När releasen ska deployas:
- target profile komplett,
- runtime config definierad,
- health finns,
- DB/connectivity/migrations verifierade,
- proxy/TLS/domain ansvar tydligt,
- persistence korrekt.

## 15. Live deployment verification

Om live target inte kan nås:
- markera live verification som pending,
- avgör om detta blockerar release eller endast production deployment.

Exempel:
- source release kan vara ready,
- production deployment kan fortfarande vara blocked.

## 16. Configuration readiness

Required runtime variables ska vara dokumenterade.

Secrets ska ha:
- canonical namn,
- placering/owner,
- inga verkliga värden i repo/docs.

## 17. Installation readiness

En operatör/developer ska kunna följa installationen från prerequisites till verifierad startup.

## 18. Operations readiness

För deployable system ska operations minst täcka:
- health,
- logs,
- restart/redeploy,
- migrations,
- rollback/restore där relevant,
- troubleshooting.

## 19. Migration readiness

Vid DB/schema changes:
- migration tested,
- ordering defined,
- compatibility assessed,
- backup/restore eller rollback definierad när risk kräver det.

## 20. Traceability readiness

När traceability används ska Must-krav inte vara orphaned.

Ideal chain:

`FR/NFR → AC → DEV → TEST`

## 21. Hygiene readiness

Release ska inte innehålla:
- committed secrets,
- transient artifacts utan policy,
- gamla distributionskopior,
- build output som stör source package,
- broken required links/state.

## 22. Known limitations

Kända begränsningar ska vara:
- verkliga,
- tydligt dokumenterade,
- bedömda som acceptabla för release scope.

Known limitation får inte användas som etikett för dold Must-bugg.

## 23. Release blocker

Exempel:
- Must requirement ej implementerat,
- required test FAIL,
- critical security issue,
- migration ej verifierad,
- artifact kan inte byggas,
- required config okänd,
- release deployment kan inte starta,
- state/spec motsäger faktiskt system på kritisk punkt.

## 24. Warning

Exempel:
- låg-risk docs gap,
- optional test ej körbart i aktuell miljö,
- informational dependency warning,
- live production smoke test pending men artifact release tillåten.

Warning ska ha rationale.

## 25. Readiness status

Canonical status:

- `READY`
- `READY_WITH_WARNINGS`
- `NOT_READY`

## 26. READY

Alla required gates pass.

## 27. READY_WITH_WARNINGS

Alla required gates pass, men icke-blockerande warnings finns.

Warnings måste vara dokumenterade.

## 28. NOT_READY

Minst en required gate:
- fail,
- blocked,
- unknown på kritisk punkt.

## 29. System acceptance

System acceptance är bredare än enskilda DEV-step tests.

Den ska verifiera release som helhet mot:
- goals,
- Must scope,
- acceptance criteria,
- critical NFR,
- operational readiness.

## 30. Acceptance session

För medium/large projekt kan separat acceptance session användas.

Output:
- accepted,
- accepted with limitations,
- rejected/blocking findings.

## 31. Acceptance evidence

Evidens kan vara:
- test IDs,
- CI run,
- manual scenario,
- deployment smoke test,
- migration rehearsal,
- security review.

## 32. Manual acceptance

Manuell acceptance ska dokumentera:
- scenario,
- expected,
- actual,
- result,
- date/environment när relevant.

## 33. Release candidate

En RC används när:
- alla huvudsakliga features är klara,
- systemet går in i stabilisering/acceptance,
- endast blockerfixar bör tillkomma.

## 34. RC discipline

Efter RC:
- undvik ny Should/Could-funktion,
- prioritera blockerfixar,
- kör regression,
- dokumentera förändringar mellan RC-versioner.

## 35. Versioning

Version ska följa projektets releasepolicy.

System Builder ska inte bumpa version mekaniskt per DEV-step.

Releaseversion sätts vid faktisk release/readiness.

## 36. Release notes

Release notes ska sammanfatta:
- vad som är nytt/ändrat,
- breaking changes,
- migration,
- known limitations,
- upgrade notes.

Release notes ersätter inte current-state docs.

## 37. CHANGE release readiness

Verifiera särskilt:
- change goal,
- regression,
- compatibility,
- migration,
- current-state docs.

## 38. IMPROVE release readiness

Verifiera:
- behavior preserved,
- tekniskt mål uppnått,
- regression,
- deployment/build quality om berört.

## 39. CREATE release readiness

Verifiera:
- initial Must-scope,
- core flows,
- setup,
- deployment,
- security baseline,
- runbooks.

## 40. Release readiness report

Canonical dokument när separat report behövs:

`docs/release-readiness.md`

Struktur:

```text
# Release Readiness
## Release candidate
## Scope
## Gate summary
## Acceptance
## Verification evidence
## Security / risk
## Packaging / deployment
## Documentation
## Known limitations
## Blockers
## Decision
```

## 41. Gate table

Exempel:

| Gate | Required | Result | Evidence |
|---|---|---|---|
| Must scope | yes | pass | FR-001.. |
| CI | yes | pass | workflow |
| Security baseline | yes | pass | review |
| Live deployment smoke | no | warning | pending |

## 42. Decision rule

`READY` endast om alla `Required=yes` är pass.

`READY_WITH_WARNINGS` om required pass men warnings finns.

Annars `NOT_READY`.

## 43. Release vs deploy

Det är möjligt att:
- artifact release = READY,
- production deployment = NOT_READY.

Exempel: live DNS eller target credentials saknas.

System Builder ska skilja dessa.

## 44. Partial environments

Om staging finns men prod inte kan verifieras:
- staging evidence används,
- prod-specific gates markeras separat.

## 45. User acceptance

När användarens explicita godkännande krävs ska detta vara en egen gate.

System Builder ska inte fabricera användargodkännande.

## 46. No false PASS

System Builder får aldrig markera:
- ej körd test som pass,
- ej nådd deployment som verified,
- antagande som evidence.

Använd `pending`, `unknown` eller `not run`.

## 47. Readiness och work status

När implementationen är slut ska next recommended övergå till release readiness.

Efter readiness:
- READY → release,
- READY_WITH_WARNINGS → release eller warning review enligt policy,
- NOT_READY → repair/blocker.

## 48. Release evidence retention

Repositoryt ska bevara tillräcklig sammanfattning för att förstå varför releasen godkändes.

Full CI-logg behöver normalt inte checkas in.

## 49. Anti-patterns

Undvik:
- "CI grön = releaseklar",
- release med otestad migration,
- release utan rollback för high-risk change,
- known limitation som döljer Must-fel,
- manuell acceptance utan outcome,
- påstådd prod-verifiering utan access,
- release notes som enda dokumentation.

## 50. Exit-kriterier för SB-28

SB-28 är klart när:
- readiness-domäner definierats,
- READY/READY_WITH_WARNINGS/NOT_READY definierats,
- required/informational gates finns,
- system acceptance definierats,
- release-vs-deploy skillnad finns,
- no-false-pass regel finns,
- report template/example/validator finns.
