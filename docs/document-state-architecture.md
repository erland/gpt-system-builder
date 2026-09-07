# System Builder – Dokument- och state-arkitektur

## 1. Syfte

Detta dokument definierar hur System Builder ska dela upp information mellan människolästa dokument, maskinläsbart tillstånd och valideringskontrakt.

Målet är att:

- varje informationskategori ska ha en tydlig canonical källa,
- undvika dubbla sanningskällor,
- göra `"Gör nästa steg"` robust utan konversationsminne,
- hålla current-state-dokument läsbara för människor,
- göra status, spårbarhet och deploymentval entydiga för maskinell behandling,
- bevara historiska beslut utan att current-state-dokument blir loggböcker.

## 2. Grundprincip

> **Markdown beskriver intent, krav, design och vägledning. YAML beskriver maskinellt tillstånd, strukturerad konfiguration och spårbarhet. JSON Schema validerar YAML-kontrakten.**

System Builder ska inte skapa parallella Markdown- och YAML-versioner av samma innehåll.

Exempel som ska undvikas:

```text
functional-specification.md
functional-specification.yaml
```

om båda innehåller samma kravtext.

## 3. Informationsklasser

System Builder skiljer mellan fyra huvudklasser:

1. **Current-state documentation** – hur systemet avses fungera nu.
2. **Historical records** – varför och hur viktiga beslut/förändringar gjordes.
3. **Machine state** – var utvecklingsarbetet faktiskt befinner sig.
4. **Machine configuration/traceability** – strukturerade val och relationer som behöver tolkas entydigt.

---

# 4. Current-state documentation

Current-state-dokument ska beskriva systemets aktuella avsedda läge efter genomförda förändringar.

Canonical format: **Markdown**.

## 4.1 Funktionell specifikation

Canonical fil:

`docs/functional-specification.md`

Innehåller:

- syfte,
- scope,
- aktörer,
- användningsfall,
- funktionella krav,
- affärsregler,
- informationsbehov,
- integrationer,
- behörighet,
- fel/undantag,
- icke-funktionella krav,
- acceptance criteria,
- out of scope,
- öppna frågor.

Krav kan ha stabila ID:n som `FR-001`.

Själva kravtexten ska inte dupliceras i YAML.

## 4.2 Arkitektur

Canonical fil:

`docs/architecture.md`

Innehåller:

- systemkontext,
- komponenter,
- ansvar,
- dataflöden,
- datamodell på hög nivå,
- integrationer,
- säkerhetsprinciper,
- deploymentmodell,
- tekniska huvudval,
- trade-offs.

Arkitekturen beskriver **nuvarande målarkitektur/current state**, inte kronologin över alla tidigare beslut.

## 4.3 Development plan

Canonical fil:

`docs/development-plan.md`

Innehåller:

- plansteg,
- mål,
- scope,
- förutsättningar,
- implementation,
- verifiering,
- klart-kriterier,
- beroenden.

Planen beskriver **vad som ska göras och varför**.

Planens faktiska exekveringsstatus ska inte vara canonical här.

## 4.4 Teststrategi

Canonical fil när separat dokument krävs:

`docs/test-strategy.md`

För små projekt får motsvarande innehåll ligga i development plan om separat dokument inte tillför värde.

## 4.5 Konfiguration, installation och drift

Canonical filer när relevanta:

- `docs/configuration.md`
- `docs/installation.md`
- `docs/operations.md`

De ska beskriva aktuell produkt och aktuell deploymentmodell.

---

# 5. Historical records

Historiska dokument ska bevara rationale och förändringshistorik utan att bli current-state source of truth.

Canonical format: **Markdown**.

## 5.1 Architecture Decision Records

Plats:

`docs/architecture-decisions/ADR-xxx-*.md`

ADR beskriver:

- beslut,
- kontext,
- alternativ,
- rationale,
- konsekvenser,
- status.

När ett ADR ändrar arkitekturen ska `docs/architecture.md` uppdateras till resultatet av beslutet.

## 5.2 Product decisions

Canonical fil:

`docs/product-decisions.md`

Används för viktiga funktionella eller produktmässiga beslut som behöver historik men inte hör hemma som löpande resonemang i functional spec.

## 5.3 Change requests

För större förändringar:

```text
docs/changes/
  CR-001-<slug>/
    request.md
    impact-analysis.md
```

Change request-historik får inte ersätta uppdatering av current-state-dokument.

När förändringen är klar ska berörda canonical current-state-dokument beskriva det nya läget.

---

# 6. Machine state

Maskinläsbart state ska göra arbetet återupptagningsbart utan att modellen behöver tolka fria statusformuleringar.

Canonical format: **YAML**.

## 6.1 Project state

Planerad fil:

`.system-builder/project.yaml`

Syfte:

- identifiera projektet,
- beskriva grundläggande projekttyp,
- stack,
- source mode,
- komplexitetsnivå,
- centrala delivery-egenskaper.

Den ska innehålla fakta som behövs för maskinell styrning, inte duplicera arkitekturbeskrivningen.

## 6.2 Work status

Planerad fil:

`.system-builder/work-status.yaml`

Detta blir primär maskinläsbar källa för `"Gör nästa steg"`.

Ska minst kunna representera:

- aktiv arbetsserie,
- aktiv plan,
- completed steps,
- selected/in-progress step,
- next recommended step,
- blockers,
- senaste verifieringsstatus,
- baseline-status,
- source drift-status där relevant.

### Regel

`docs/development-plan.md` säger **vad som ska göras**.

`.system-builder/work-status.yaml` säger **var arbetet faktiskt befinner sig**.

Vid konflikt ska System Builder inte gissa. Konflikten ska hanteras innan ny implementation fortsätter.

---

# 7. Machine configuration and traceability

Canonical format: **YAML**.

## 7.1 Traceability

Planerad fil:

`.system-builder/traceability.yaml`

Syfte:

- koppla krav-ID till development steps,
- koppla krav/acceptance criteria till verifiering,
- identifiera orphan requirements,
- identifiera must-krav som inte är implementerade eller verifierade.

Traceability ska referera till ID:n och status, inte duplicera full kravtext.

Exempel:

```yaml
requirements:
  FR-001:
    development_steps:
      - DEV-006
    verification:
      - TEST-014
    status: implemented
```

## 7.2 Deployment profile

Planerad fil:

`.system-builder/deployment-profile.yaml`

Syfte:

- hålla strukturerade deploymentval konsekventa mellan arkitektur, kod, CI och dokumentation.

Kan exempelvis representera:

- packaging,
- target platform,
- runtime,
- database,
- persistence,
- networking,
- TLS/reverse proxy,
- health checks,
- registry,
- environment configuration.

Detta är en strukturerad profil, inte full installationsdokumentation.

---

# 8. JSON Schema

Maskinläsbara YAML-filer ska valideras med JSON Schema.

Planerade schemas:

```text
schemas/
  project.schema.json
  work-status.schema.json
  traceability.schema.json
  deployment-profile.schema.json
```

Schema används för att:

- fånga felaktiga state transitions,
- förhindra okända/otydliga statusvärden,
- validera required fields,
- göra regressionstester möjliga,
- ge mindre modeller ett tydligare kontrakt.

Schema ska inte användas för att tvinga människolästa Markdown-dokument till överdriven struktur.

---

# 9. Canonical mapping

| Informationskategori | Canonical källa | Format |
|---|---|---|
| Behov/problem | Functional spec / change request | Markdown |
| Funktionellt current state | `docs/functional-specification.md` | Markdown |
| Arkitektur current state | `docs/architecture.md` | Markdown |
| Aktiv utvecklingsplan | `docs/development-plan.md` | Markdown |
| Teststrategi | `docs/test-strategy.md` när separat | Markdown |
| Konfiguration | `docs/configuration.md` | Markdown |
| Installation | `docs/installation.md` | Markdown |
| Drift | `docs/operations.md` | Markdown |
| Arkitekturbeslut | `docs/architecture-decisions/*.md` | Markdown |
| Produktbeslut | `docs/product-decisions.md` | Markdown |
| Change history | `docs/changes/*/` | Markdown |
| Projektmetadata/state | `.system-builder/project.yaml` | YAML |
| Exekveringsstatus | `.system-builder/work-status.yaml` | YAML |
| Kravspårbarhet | `.system-builder/traceability.yaml` | YAML |
| Deploymentprofil | `.system-builder/deployment-profile.yaml` | YAML |
| Maskinkontrakt | `schemas/*.schema.json` | JSON Schema |

---

# 10. Regler mot dubbla sanningskällor

## 10.1 Ingen fullständig spegling

System Builder ska inte hålla samma fullständiga information i två filer bara för bekvämlighet.

Tillåtet:

- `FR-001` med full text i Markdown,
- `FR-001` som referens och status i traceability YAML.

Inte tillåtet:

- full kravtext i både Markdown och YAML.

## 10.2 Härledda sammanfattningar

En härledd sammanfattning får finnas på flera ställen om det är tydligt vilken källa som är canonical.

Exempel:

- `architecture.md` kan säga att deployment target är Coolify,
- `deployment-profile.yaml` är canonical för den maskinella profilen,
- `installation.md` får beskriva hur profilen används.

Vid konflikt ska System Builder reparera dokumentationen från den definierade canonical källan, inte välja godtyckligt.

## 10.3 Status dupliceras inte i planen

Checkboxar i development plan får användas för läsbarhet om projektet redan har dem, men de får inte vara primär exekveringsstatus när `work-status.yaml` finns.

---

# 11. Stabil ID-strategi

Stabila ID:n används där relationer mellan artefakter behöver överleva redigeringar.

Rekommenderade prefix:

- `FR-xxx` – functional requirement
- `NFR-xxx` – non-functional requirement
- `AC-xxx` – acceptance criterion
- `DEV-xxx` – development step
- `TEST-xxx` – verifieringspunkt/testkontrakt
- `ADR-xxx` – architecture decision
- `CR-xxx` – change request
- `RISK-xxx` – explicit risk när separat identifiering behövs

ID:n ska:

- vara stabila efter att de publicerats,
- inte återanvändas för annan innebörd,
- inte ändras bara för att ordningen i dokumentet ändras.

Små projekt behöver inte ge ID till allt; ID ska införas där spårbarhet faktiskt ger nytta.

---

# 12. Current state kontra historical state

## Current-state-filer

Dessa ska uppdateras efter en färdig förändring:

- `functional-specification.md`
- `architecture.md`
- `configuration.md`
- `installation.md`
- `operations.md`
- relevant aktiv development plan/status

## Historical-filer

Dessa bevarar beslutshistorik:

- ADR,
- change requests,
- impact analyses,
- product decisions.

### Regel för CHANGE

En slutförd change får inte lämna systemet i läget:

> "CR-014 beskriver den nya funktionen, men functional-specification.md beskriver fortfarande den gamla."

När förändringen är klar måste current-state-dokumenten integrera resultatet.

---

# 13. Dokumentlivscykel

Varje canonical dokument kan vara:

- **absent** – inte relevant ännu,
- **draft** – pågående formulering,
- **current** – beskriver aktuell avsikt/current state,
- **superseded** – endast för historiska dokument där explicit ersättning är meningsfull.

System Builder ska undvika tomma placeholder-dokument bara för att en mall säger att filen "ska finnas".

---

# 14. Regler för small / medium / large

## Small

- skapa bara de dokument som tillför verkligt värde,
- teststrategi får kombineras med plan,
- riskanalys får ligga i plan/arkitektur,
- traceability.yaml kan utelämnas om stabila ID-relationer inte behövs,
- deployment-profile.yaml skapas när deploymentval påverkar implementationen.

## Medium

Normalt separata current-state-dokument och maskinstate:

- functional spec,
- architecture,
- development plan,
- work-status,
- test strategy,
- deployment profile när relevant,
- traceability när flera krav/steg behöver följas.

## Large / high risk

Normalt:

- full current-state-struktur,
- explicit traceability,
- fler ADR,
- change impact-dokument,
- formaliserade risker,
- striktare schema- och statusvalidering.

---

# 15. Source-of-truth-regel vid runtime

När System Builder arbetar i ett projekt ska den använda följande princip:

1. användarens aktuella uttryckliga instruktion,
2. repositoryts `AGENTS.md`,
3. `.system-builder/work-status.yaml`,
4. aktiv plan och övriga canonical current-state-dokument,
5. `.system-builder/project.yaml`, traceability och deploymentprofil,
6. befintlig kod/test/projektkonventioner,
7. generisk System Builder Knowledge som fallback.

Om required state-filer saknas i ett projekt som ska använda dem ska System Builder inte fabricera historik. Den ska installera/repairera state utifrån vad som faktiskt kan härledas.

---

# 16. Arkitekturens exit-kriterier

SB-05 är uppfyllt när:

- varje informationskategori har en canonical representation,
- current-state och historik är separerade,
- Markdown/YAML/JSON Schema har tydliga ansvar,
- full innehållsduplicering mellan Markdown och YAML förbjuds,
- stabil ID-strategi är definierad,
- exekveringsstatus är separerad från development plan,
- small/medium/large kan använda samma arkitektur utan att alla artefakter alltid krävs.
