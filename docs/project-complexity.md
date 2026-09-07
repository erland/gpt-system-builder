# System Builder – Projektkomplexitet och adaptiv process

## 1. Syfte

Detta dokument definierar hur System Builder klassificerar ett projekt eller en förändringsserie som `small`, `medium` eller `large` och hur process, dokumentation och verifiering anpassas efter nivån.

Målet är tvådelat:

- små och lågriskprojekt ska inte belastas med onödig process eller tomma dokument,
- större eller riskfyllda projekt ska inte tappa viktiga kontrollpunkter bara för att användaren beskriver uppdraget kortfattat.

Komplexitetsnivån är ett styrvärde för **hur mycket explicit struktur som behövs**, inte ett värdeomdöme om systemet.

## 2. Grundprincip

Klassificera efter **samlad leveranskomplexitet och risk**, inte enbart efter kodmängd, antal filer eller teamstorlek.

Bedöm minst följande dimensioner när de är relevanta:

- funktionell bredd,
- antal aktörer och användarflöden,
- integrationsytor,
- datamodell och migrationsbehov,
- autentisering och behörighet,
- känslig data/personuppgifter,
- säkerhetskonsekvens,
- prestanda/tillgänglighetskrav,
- deploymenttopologi,
- extern infrastruktur,
- antal tekniska komponenter,
- osäkra eller oprövade teknikval,
- förändringens påverkan på ett befintligt system,
- rollback-/migrationsrisk,
- regulatoriska eller organisatoriska constraints som användaren anger.

En enskild högriskdimension får höja klassificeringen även om resten av projektet är litet.

## 3. Klassificeringsmodell

### 3.1 `small`

Typiska kännetecken:

- ett fåtal tydliga användarflöden,
- få komponenter,
- inga eller få enkla integrationer,
- låg data- och migrationsrisk,
- normal autentisering eller ingen autentisering,
- enkel deployment,
- låg regulatorisk/säkerhetsmässig konsekvens,
- tekniska val är välkända,
- ändringen är lokal och lätt att verifiera.

Exempel:

- liten intern webbapp,
- enkel REST-tjänst med extern PostgreSQL,
- mindre funktion i ett befintligt system,
- stateless tjänst för Docker/Coolify med ett fåtal endpoints.

`small` betyder inte att dokumentation saknas. Det betyder att dokument kan vara korta och vissa områden kan kombineras om det ökar tydligheten.

### 3.2 `medium`

Typiska kännetecken:

- flera användarflöden eller aktörer,
- flera interna komponenter,
- en eller flera viktiga integrationer,
- persistent data med tydlig modell,
- autentisering/behörighet med flera roller,
- migrations- eller kompatibilitetsbehov,
- containeriserad deployment med flera beroenden,
- högre krav på testbarhet, drift eller releasekontroll,
- förändringen påverkar flera delar av ett befintligt system.

Detta är System Builders normala fulla arbetsnivå.

### 3.3 `large`

Typiska kännetecken:

- många aktörer eller domäner,
- flera tjänster eller större komponentlandskap,
- flera kritiska integrationer,
- omfattande datamodell eller komplex migration,
- höga säkerhets-/behörighetskrav,
- känsliga data eller betydande regulatoriska constraints,
- höga tillgänglighets-/prestandakrav,
- komplex deployment/infrastruktur,
- betydande teknisk osäkerhet,
- stor påverkan på befintlig arkitektur,
- rollback eller release innebär betydande verksamhetsrisk.

`large` ska normalt ge fler explicita gates, fler ADR/change records och större krav på spårbarhet och specialistgranskning.

## 4. Klassificeringsregler

### 4.1 Default

Om informationen är tillräcklig för att göra en rimlig bedömning ska System Builder **klassificera utan att fråga användaren**.

### 4.2 Fråga endast när det påverkar arbetssättet materiellt

Ställ en kompletterande fråga endast när:

- två nivåer är ungefär lika plausibla,
- skillnaden påverkar viktiga artefakter, säkerhetskontroller eller planering,
- informationen inte kan härledas från repo, ZIP, befintliga dokument eller aktuell användarbeskrivning.

### 4.3 Högre risk vinner

Om projektet är funktionellt litet men innehåller exempelvis känsliga data, riskfylld migration eller kritisk integration ska nivån höjas.

### 4.4 CHANGE bedöms utifrån förändringens konsekvens

Ett stort befintligt system behöver inte automatiskt ge `large` för en lokal ändring. Bedöm:

- ändringens blast radius,
- arkitekturpåverkan,
- data-/migrationsrisk,
- release-/rollbackrisk,
- testbarhet.

### 4.5 Omklassificering är tillåten

Ny evidens får ändra nivån. Omklassificering ska dokumenteras när den påverkar plan eller obligatoriska artefakter.

## 5. Artefaktmatris

Legend:

- **R** = required som separat artefakt,
- **C** = required content, men får kombineras med annan canonical artefakt,
- **A** = as needed,
- **–** = normalt inte nödvändig.

| Artefakt / innehåll | Small | Medium | Large |
|---|---:|---:|---:|
| `docs/functional-specification.md` | R | R | R |
| `docs/architecture.md` | R | R | R |
| `docs/development-plan.md` | R | R | R |
| `.system-builder/project.yaml` | R | R | R |
| `.system-builder/work-status.yaml` | R | R | R |
| `.system-builder/deployment-profile.yaml` | C/A | R när deploybart system | R när deploybart system |
| `.system-builder/traceability.yaml` | A | R för fler-stegsleverans | R |
| `docs/test-strategy.md` | C | R | R |
| `docs/configuration.md` | C/A | R när konfiguration finns | R när konfiguration finns |
| `docs/installation.md` | C/A | R för körbar leverans | R för körbar leverans |
| `docs/operations.md` | C/A | R för driftad tjänst | R för driftad tjänst |
| `docs/product-decisions.md` | A | A | R/A beroende på produktbeslut |
| `docs/architecture-decisions/*.md` | A | A vid betydande beslut | R för betydande beslut |
| `docs/changes/*/request.md` | A | A | R/A för större changes |
| `docs/changes/*/impact-analysis.md` | A | R vid bred CHANGE | R vid CHANGE |
| separat riskregister | – | A | A/R vid hög risk |
| specialistgranskningar | – | A | R/A efter riskområde |

## 6. Innehållsnivå per klass

### 6.1 Small

Functional specification får vara kompakt men ska minst ge:

- mål,
- scope/out-of-scope,
- aktör eller huvudanvändare,
- must-krav,
- viktigaste acceptance criteria.

Architecture får vara kompakt men ska minst ge:

- komponenter,
- data/persistence,
- viktiga integrationer,
- deploymentval.

Development plan ska fortfarande bestå av små verifierbara steg.

Risk, teststrategi och driftaspekter får ligga som tydliga avsnitt i andra canonical dokument när separata dokument inte tillför värde.

### 6.2 Medium

Använd normalt separata canonical dokument för:

- functional specification,
- architecture,
- development plan,
- test strategy,
- deployment profile,
- configuration/installation/operations när relevanta.

Maskinläsbar traceability ska användas när leveransen omfattar flera krav och flera implementationsteg.

### 6.3 Large

Utöver medium-nivån ska System Builder normalt kräva:

- explicit kravspårbarhet,
- fler dokumenterade arkitekturbeslut,
- formellare change impact vid CHANGE,
- tydligare riskhantering,
- explicita release gates,
- specialistgranskning när ett högriskområde identifieras,
- starkare verifiering av migrations-, säkerhets- och rollbackscenarier.

## 7. Kontrollnivåer

### 7.1 Discovery

**Small:** endast frågor som påverkar scope eller implementation materiellt.

**Medium:** täck aktörer, huvudflöden, data, integrationer, deployment och viktigaste constraints.

**Large:** komplettera med explicita risk-/beroendefrågor och identifiera behov av specialistspår tidigt.

### 7.2 Risk / feasibility

**Small:** fokuserad check; separat artefakt behövs normalt inte.

**Medium:** explicit analys i plan/arkitektur eller separat impact/risk-del när det behövs.

**Large:** explicit riskhantering; blockers och spikes ska vara synliga och prioriterade.

### 7.3 Architecture

**Small:** systemcontext + komponenter + data + deployment kan räcka.

**Medium:** full canonical arkitekturstruktur.

**Large:** full struktur plus tydliga ADR, trade-offs, integration/deployment/security views efter behov.

### 7.4 Testing

**Small:** stegvisa tester och en kompakt teststrategi räcker ofta.

**Medium:** separat teststrategi och verifieringsmatris för centrala flöden.

**Large:** riskbaserad teststrategi, acceptance coverage, migrations-/rollbacktester och specialistkontroller där relevanta.

### 7.5 Release readiness

**Small:** kontrollera must-krav, acceptance, build/test, paketering och nödvändig installationsinformation.

**Medium:** full release-readiness-kontroll enligt end-to-end-processen.

**Large:** full kontroll plus explicit spårbarhet, risk-/specialistgates och rollback/migration readiness.

## 8. Anti-byråkratiregler

System Builder ska inte:

- skapa tomma placeholder-dokument bara för att en matris nämner dem,
- skapa separat dokument när ett kort tydligt avsnitt i en befintlig canonical artefakt är bättre,
- kräva ADR för triviala eller reversibla beslut,
- kräva riskregister för ett uppenbart lågriskprojekt,
- ställa frågor för sådant som kan härledas säkert från projektet,
- höja nivå enbart på grund av antal filer eller kodrader.

## 9. Säkerhetsventiler

Oavsett klass ska följande kunna bli blockerare:

- oklar eller osäker dataförlust/migration,
- oförstådd auth/authorization för skyddad funktion,
- kritisk extern integration som inte verifierats,
- deploymentantagande som gör leveransen okörbar,
- röda relevanta tester utan förstådd baseline,
- krav-/plan-konflikt som gör nästa steg oklart.

`small` betyder aldrig att dessa kontroller får hoppas över.

## 10. Maskinläsbar representation

När `.system-builder/project.yaml` införs ska projektklassificeringen kunna representeras ungefär så här:

```yaml
complexity:
  level: medium
  rationale:
    - multiple user flows
    - external GitHub integration
    - persistent PostgreSQL data
    - container deployment
  elevated_by:
    - integration_criticality
  last_assessed_for: initial_delivery
```

Exakt schema definieras i senare schemastag. Den människoläsbara motiveringen behöver inte dupliceras ordagrant i flera dokument.

## 11. Omklassificering under arbetet

Exempel på signaler för att höja från `small` till `medium`:

- en kritisk integration tillkommer,
- datamigration behövs,
- flera roller/behörighetsnivåer introduceras,
- deployment blir flerkomponentsbaserad,
- change blast radius visar sig vara större än väntat.

Exempel på att en planerad `medium`-leverans kan behandlas som `small`:

- scope minskas kraftigt,
- riskfyllda delar flyttas till senare release,
- deployment förenklas,
- ändringen isoleras till ett lokalt, vältestat område.

Ändringen ska påverka framtida processkrav, inte skriva om historiken för redan genomförda steg.

## 12. Beslutsregel för runtime

När System Builder startar en ny CREATE-, CHANGE- eller IMPROVE-serie ska den:

1. samla tillgänglig evidens,
2. göra en preliminär klassificering,
3. fråga endast om en materiell oklarhet återstår,
4. dokumentera nivån i projektstate när state-modellen finns,
5. använda artefakt- och kontrollmatrisen som minimum,
6. höja kontrollnivån när risk kräver det,
7. undvika dokument som saknar konkret nytta.

Detta är den canonical modellen för adaptiv process.
