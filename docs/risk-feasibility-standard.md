# System Builder – Risk- och feasibility-arbete

## 1. Syfte

System Builder ska identifiera och hantera osäkerheter som kan göra implementation dyr, osäker eller felriktad.

Risk/feasibility-arbetet ska svara på:

- Finns tekniska antaganden som ännu inte är bevisade?
- Finns externa beroenden som kan blockera lösningen?
- Finns data-, säkerhets-, deployment- eller migrationsrisker?
- Behövs spike, PoC eller tidig verifiering?
- Är risken accepterad, reducerad, överförd eller blockerande?

Målet är inte att skapa ett tungt riskregister för alla projekt, utan att upptäcka viktiga osäkerheter innan de cementeras i arkitektur eller implementation.

## 2. Grundprincip

> Hög osäkerhet ska hanteras tidigt. Dokumentationsnivån ska vara proportionerlig mot sannolik konsekvens.

System Builder ska inte behandla en kritisk teknisk eller operativ osäkerhet som en fotnot i slutet av planen.

## 3. När risk/feasibility ska bedömas

Bedömningen görs särskilt när projektet innehåller:

- nytt eller okänt externt API,
- datamigration,
- autentisering/behörighet,
- känslig data eller personuppgifter,
- hög tillgänglighet,
- prestandakrav,
- filuppladdning/exekvering,
- tredjepartskod med oklar licens,
- ny deploymentplattform,
- stateful workloads,
- extern databas,
- avancerad nätverksåtkomst,
- svår rollback,
- integrationskedjor med flera system.

För små lågriskprojekt får bedömningen vara mycket kort.

## 4. Riskkategorier

System Builder ska minst kunna resonera över:

### 4.1 Technical feasibility

Exempel:

- fungerar valt bibliotek/API för behovet?
- klarar teknikstacken deploymentmiljön?
- finns begränsningar i runtime, storage eller nätverk?

### 4.2 Integration

Exempel:

- rate limits,
- auth-flöden,
- API-stabilitet,
- timeout,
- idempotency,
- tredjepartsdrift.

### 4.3 Data

Exempel:

- datakvalitet,
- schemaändring,
- migration,
- backup/restore,
- retention,
- ownership.

### 4.4 Security

Exempel:

- secrets,
- trust boundaries,
- input validation,
- access control,
- unsafe file handling,
- dependency risk.

### 4.5 Operations / deployment

Exempel:

- persistent storage,
- health checks,
- startup order,
- external database,
- reverse proxy/TLS,
- rollback.

### 4.6 Performance / scale

Exempel:

- latency,
- throughput,
- concurrency,
- memory,
- large files,
- batchvolym.

### 4.7 Legal / licensing / policy

När användaren eller projektunderlag gör det relevant:

- licensrestriktioner,
- data residency,
- policykrav,
- regulatoriska constraints.

System Builder ska inte fabricera juridiska krav.

## 5. Risk-ID

När separat riskspårning tillför värde används stabila ID:n:

- `RISK-001`
- `RISK-002`

Små projekt behöver inte ID-sätta triviala risker.

## 6. Enkel riskmodell

En risk bör normalt beskrivas med:

- ID,
- kategori,
- antagande/risk,
- trigger/evidence,
- sannolikhet,
- konsekvens,
- nivå,
- hantering,
- owner/ansvar när relevant,
- kopplade krav/plansteg,
- status.

Rekommenderade värden:

### Probability

- low
- medium
- high

### Impact

- low
- medium
- high

### Status

- open
- mitigated
- accepted
- blocked
- closed

## 7. Risknivå

System Builder får använda en enkel matris:

| Probability | Impact | Result |
|---|---|---|
| low | low | low |
| low | medium | low/medium |
| low | high | medium |
| medium | low | low/medium |
| medium | medium | medium |
| medium | high | high |
| high | low | medium |
| high | medium | high |
| high | high | critical |

Syftet är prioritering, inte falsk precision.

## 8. Feasibility question

En feasibility-fråga ska vara konkret.

Svagt:

> Kan detta fungera?

Bra:

> Kan GitHub API-flödet skapa repository och ladda upp hela projektträdet inom relevanta rate limits för projekt upp till definierad storlek?

Bra:

> Kan tjänsten köras stateless i Coolify när alla persistenta filer flyttas till extern storage/database?

## 9. Hanteringsstrategier

En risk kan:

### Accept

Risken är känd och tolererbar.

### Mitigate

Design eller implementation minskar sannolikhet/konsekvens.

### Avoid

Lösningen ändras så att risken tas bort.

### Transfer / externalize

Ansvar flyttas till extern tjänst/plattform när det är ett medvetet designval.

### Block

Implementation ska inte fortsätta genom den riskpåverkade delen innan frågan är löst.

## 10. Spike

En spike är ett tids-/scope-avgränsat utvecklingssteg som producerar kunskap, inte produktionsfunktionalitet.

En bra spike ska ha:

- tydlig fråga,
- avgränsat scope,
- expected evidence,
- exit criteria,
- beslutspunkt efter utfallet.

Exempel:

```text
DEV-004 – Verify GitHub repository upload feasibility

Question:
Can the selected API approach reliably upload repositories up to the target size?

Evidence:
- API experiment
- rate-limit observations
- failure behavior

Done when:
- approach is accepted, rejected or replaced
- result is documented
- architecture/plan updated if needed
```

## 11. PoC

PoC används när en central lösningsidé måste bevisas i kombination.

Exempel:

- auth + API + deployment,
- event flow mellan flera system,
- database migration approach,
- browser capability.

PoC-kod är inte automatiskt production-ready.

System Builder ska explicit avgöra om PoC:

- kastas,
- hårdnar till produktionskod,
- återanvänds delvis.

## 12. Risk som blockerare

En risk ska normalt blockera nästa steg om:

- utfallet kan göra vald arkitektur ogiltig,
- det finns realistisk risk för dataförlust,
- säkerhetskritisk design är oklar,
- migration inte kan återställas,
- central tredjepartskapacitet är obevisad,
- deploymentmiljön inte stödjer nödvändig runtime,
- implementation annars sannolikt måste göras om.

System Builder ska inte fortsätta numeriskt i development plan genom en sådan blockerare.

## 13. Relation till development plan

Risker ska påverka planordning.

Exempel:

```text
RISK-003: External API throughput unknown
→ DEV-002: API feasibility spike
→ DEV-005: Main integration implementation
```

Risk-first-planering är bättre än att implementera hela flödet och upptäcka problemet sist.

## 14. Relation till architecture

När riskutfall ändrar design:

- architecture.md uppdateras,
- ADR skapas om beslutet är betydande,
- development plan revideras,
- work status synkas.

Riskanalysen ska inte bli alternativ current-state-arkitektur.

## 15. Relation till functional spec

Riskarbete får inte tyst ändra funktionellt scope.

Om risk leder till att ett must-krav:

- tas bort,
- begränsas,
- skjuts upp,

ska functional spec och eventuellt product decision uppdateras.

## 16. Relation till deployment

Deploymentrisk ska bedömas tidigt när plattformen påverkar systemdesign.

Exempel för Coolify:

- extern PostgreSQL tillgänglig?
- appen stateless?
- persistent file storage behövs?
- health endpoint möjlig?
- port och reverse proxy korrekt?
- migrationsstrategi säker?

## 17. Small-project-regel

För small-projekt får risk/feasibility ligga som ett kort avsnitt i:

- architecture.md, eller
- development-plan.md.

Separat riskdokument behövs bara när antalet eller vikten av riskerna motiverar det.

## 18. Medium / large

Medium-projekt bör normalt ha explicit risksammanställning.

Large/high-risk bör normalt ha:

- stabila RISK-ID:n,
- tydlig status,
- koppling till DEV-steg,
- blockerare,
- review före release readiness.

## 19. Canonical dokument

När separat dokument behövs:

`docs/risk-feasibility.md`

Det beskriver analys och rationale.

System Builder behöver inte införa separat YAML-riskregister i första versionen; machine state för blockerare ligger i work status och relationer kan uttryckas via plan/traceability.

## 20. Rekommenderad struktur

```text
# Risk and Feasibility

## Assumptions
## Risks
## Feasibility questions
## Spikes / PoCs
## Blocking issues
## Accepted risks
## Review outcome
```

## 21. Riskpost

```markdown
### RISK-001 – <Title>

**Category:** integration  
**Probability:** medium  
**Impact:** high  
**Level:** high  
**Status:** open

**Risk / assumption**

...

**Evidence / trigger**

...

**Handling**

...

**Related requirements / steps**

- FR-...
- DEV-...
```

## 22. Anti-patterns

Undvik:

- hundratals generiska risker,
- "säkerhet kan vara ett problem" utan konkret innebörd,
- riskregister som aldrig påverkar plan,
- PoC som smygs in som produktionskod utan review,
- blockerande risker som ignoreras för att nästa plan-ID ligger numeriskt först,
- sannolikhetspoäng med falsk exakthet.

## 23. Kvalitetskriterier

Risk/feasibility är tillräckligt bra när:

1. kritiska antaganden är synliga,
2. hög osäkerhet har planerad evidens,
3. blockerande risker påverkar next-step-val,
4. spikes/PoCs har tydliga frågor och exit-kriterier,
5. arkitektur och plan uppdateras från faktiska resultat,
6. små projekt inte belastas med onödig process.

## 24. Exit-kriterier för risk/feasibility-fasen

Fasen är klar när:

- inga osynliga högriskantaganden återstår,
- blockerande osäkerhet har antingen lösts eller blivit explicit blockerare,
- högriskfrågor har riskreducerande steg,
- arkitektur och plan kan fortsätta utan att bygga på otestade kritiska antaganden.
