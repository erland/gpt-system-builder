# System Builder – Development plan-kontrakt

## 1. Syfte

`docs/development-plan.md` är canonical människoläsbar beskrivning av **vad som ska byggas, i vilken ordning och varför**.

Planen ska vara:

- uppdelad i små, verifierbara steg,
- begriplig för människa och GPT,
- tillräckligt detaljerad för `"Gör nästa steg"`,
- stabil nog för att återuppta arbete utan konversationsminne,
- flexibel nog att kunna revideras när ny evidens uppstår.

Planen ska inte vara primär källa för faktisk exekveringsstatus när `.system-builder/work-status.yaml` finns.

## 2. Grundprincip

> Planen beskriver arbetets avsikt och struktur. Work status beskriver det faktiska utfallet.

`docs/development-plan.md` svarar på:

- vad är nästa avsedda leveranssteg?
- varför finns steget?
- vad ingår?
- vad måste vara sant innan steget börjar?
- hur verifieras steget?
- när är steget klart?

`.system-builder/work-status.yaml` svarar på:

- vilket steg är valt?
- vilka steg är faktiskt completed?
- finns blockerare?
- vad är nästa rekommenderade steg?
- vad blev senaste verifieringsresultatet?

## 3. Planstruktur

En development plan ska normalt innehålla:

```text
# Development Plan

## Goal and delivery scope
## Planning assumptions
## Step overview
## Development steps
## Cross-cutting verification
## Plan-change rules
```

För små projekt får strukturen komprimeras.

## 4. Steg-ID

Varje utvecklingssteg som behöver stabil referens ska ha ID:

- `DEV-001`
- `DEV-002`

ID ska:

- vara unikt,
- aldrig återanvändas för annan innebörd,
- förbli stabilt om stegets titel justeras,
- kunna refereras från traceability och work status.

## 5. Obligatoriskt innehåll per steg

Varje steg ska normalt innehålla:

### ID och titel

Exempel:

`## DEV-014 – Containerisera backend`

### Mål

Kort beskrivning av vilket utfall steget ska skapa.

### Scope

Vad som ingår och inte ingår.

### Förutsättningar

Vad som måste vara sant innan steget kan utföras säkert.

### Implementation

Vilka delar som sannolikt ska förändras eller skapas.

Detta ska beskrivas på tillräcklig nivå för att styra arbetet utan att bli rad-för-rad-instruktion.

### Verifiering

Hur steget ska kontrolleras.

Exempel:

- build,
- unit tests,
- integration tests,
- lint,
- typecheck,
- container build,
- schema validation,
- manuell acceptance.

### Klart-kriterier

Objektiva kriterier som måste vara uppfyllda innan steget får markeras completed.

### Beroenden

Tidigare steg, externa beslut eller blockerare som påverkar steget.

## 6. Rekommenderad stegmall

```markdown
## DEV-XXX – <Title>

### Mål

...

### Scope

**Ingår**
- ...

**Ingår inte**
- ...

### Förutsättningar

- ...

### Implementation

- ...

### Verifiering

- ...

### Klart-kriterier

- [ ] ...
- [ ] ...

### Beroenden

- ...
```

## 7. Lagom storlek

Ett normalt plansteg ska kunna genomföras i en separat prompt/körning.

Ett steg är sannolikt för stort om det:

- innehåller flera oberoende funktionella förändringar,
- förändrar både stor arkitektur och flera produktflöden samtidigt,
- kräver flera separata riskfyllda migrationer,
- inte kan verifieras som en sammanhängande enhet,
- sannolikt lämnar projektet i halvfärdigt läge.

Ett steg är sannolikt för litet om det:

- endast ändrar trivial formatting,
- bara skapar en fil som inte har fristående värde,
- inte kan verifieras meningsfullt,
- bara är en mekanisk del av ett naturligt sammanhängande steg.

## 8. Vertikala steg

När praktiskt ska steg ge ett användbart end-to-end-resultat.

Föredra exempelvis:

> Implementera listning av projekt med API, UI och verifiering

framför:

> Skapa alla controllers  
> Skapa alla services  
> Skapa alla UI-komponenter

om den horisontella uppdelningen inte ger bättre riskkontroll.

Undantag är motiverade för:

- riskreducering,
- migrering,
- säkerhetsgrund,
- testskydd,
- gemensam infrastruktur,
- plattformsförberedelser.

## 9. Förberedande steg

Ett separat förberedande steg är motiverat när det:

- etablerar test baseline,
- skapar en migration som måste ske före funktion,
- bevisar ett osäkert API/teknikval,
- skapar nödvändig deploymentgrund,
- minskar risken i efterföljande steg.

Förberedande steg ska ha eget verifierbart resultat.

## 10. Risk-first-planering

Planordning ska inte enbart följa användarflöde.

Hög osäkerhet kan motivera tidiga:

- spikes,
- PoC,
- integration tests,
- migrationsprov,
- security checks,
- deployment proofs.

System Builder ska hellre upptäcka en blockerande teknisk risk i DEV-003 än efter DEV-020.

## 11. Verifierbarhet

Varje steg ska ha verifiering som motsvarar dess risk.

Exempel:

### Dokumentationssteg

- strukturell validering,
- consistency check.

### Backendfunktion

- unit/integration tests,
- API test,
- build.

### UI-funktion

- component/e2e där relevant,
- typecheck/build,
- manuell acceptance vid behov.

### Containerisering

- image build,
- container startup,
- health endpoint.

### Migration

- migration up,
- rollback/restore strategy där relevant,
- dataintegritet.

## 12. Klart-kriterier

Klart-kriterier ska vara observerbara.

Svagt:

- "koden är bra"
- "arkitekturen känns rätt"

Bra:

- build passerar,
- endpoint returnerar definierat resultat,
- traceability uppdaterad,
- migration kan köras mot testdatabas,
- health endpoint svarar,
- current-state docs är uppdaterade.

## 13. Beroenden

Beroenden ska vara explicita när de påverkar ordning.

Exempel:

```text
Depends on:
- DEV-003
- ADR-002 accepted
- external API access available
```

Om ett beroende saknas får steget inte väljas som nästa bara för att det ligger först numeriskt.

## 14. Plan vs status

Planen ska inte vara den enda statuskällan.

När `.system-builder/work-status.yaml` finns gäller:

- checklistor i planen är sekundära,
- `completed` bestäms av work status och faktisk verifiering,
- `next recommended` bestäms av status + plan + blockerare,
- en konflikt mellan plan och status ska hanteras explicit.

## 15. "Gör nästa steg"

När användaren ber om nästa steg ska System Builder:

1. läsa plan,
2. läsa work status,
3. kontrollera blockerare och drift,
4. välja första säkra rekommenderade steg,
5. låsa det som `selected_step`,
6. genomföra endast det steget,
7. verifiera,
8. uppdatera docs/status,
9. package/commit,
10. stoppa.

Planordning är en stark default, inte en ursäkt att ignorera blockerare.

## 16. Planändringar

Planen får ändras när ny evidens visar att det minskar risk eller förbättrar leveransen.

Tillåtna ändringar:

- dela steg,
- slå ihop steg,
- lägga till steg,
- ta bort framtida steg,
- omprioritera framtida steg.

Regler:

- ändringen ska motiveras,
- redan avslutade steg ska inte skrivas om som om planen alltid såg annorlunda ut,
- stabila ID:n återanvänds inte för ny innebörd,
- traceability och work status ska uppdateras vid behov.

## 17. Step split

Dela ett steg när:

- scope expanderar väsentligt under implementation,
- flera oberoende beteenden upptäcks,
- verifiering blir svår som en enhet,
- en ny blockerande risk hittas.

Det ursprungliga steget kan:

- behålla en mindre scope,
- ersättas av nya framtida steg,
- markeras blocked tills split är dokumenterad.

## 18. Step merge

Slå ihop framtida steg endast när:

- de inte ger fristående värde,
- samma implementation/verifiering naturligt täcker båda,
- separationen skulle skapa artificiell overhead.

Avslutade steg ska inte retroaktivt mergas.

## 19. CREATE-plan

CREATE-planen ska normalt gå från foundation till användbar funktionalitet.

En typisk ordning:

1. project skeleton,
2. critical technical risk,
3. core domain/data,
4. first vertical flow,
5. remaining must flows,
6. security/operability hardening,
7. packaging/deployment,
8. acceptance/release readiness.

Exakt ordning ska styras av systemets behov.

## 20. CHANGE-plan

CHANGE-planen ska fokusera på påverkan och minimal säker väg.

Typiskt:

1. baseline/impact,
2. schema/data changes,
3. backend/domain change,
4. UI/integration change,
5. migration/compatibility,
6. regression/acceptance,
7. docs/deployment updates.

Små ändringar kan naturligtvis kräva bara ett eller två steg.

## 21. IMPROVE-plan

IMPROVE ska skilja beteendebevarande arbete från funktionell förändring.

Typiskt:

1. baseline,
2. characterization tests vid behov,
3. avgränsad refaktorering,
4. verification,
5. documentation only if architecture/operations changed.

## 22. Small-project-regel

För small-projekt får development plan vara kort.

Exempel:

```text
DEV-001 – Project skeleton
DEV-002 – Core API
DEV-003 – UI flow
DEV-004 – Docker packaging
DEV-005 – Release readiness
```

Men varje steg ska fortfarande ha:

- mål,
- verifiering,
- klart-kriterier.

## 23. Anti-patterns

Undvik planer som:

### Är bara en TODO-lista

> - backend  
> - frontend  
> - database

### Är för stora

> DEV-001 – Bygg hela systemet

### Är för tekniskt mikrostyrda

> skapa klass X, metod Y, variabel Z

om detta inte är nödvändigt för ett specifikt kontrakt.

### Saknar verifiering

Ett steg utan klart-kriterier är svårt att exekvera säkert.

### Blandar orelaterat arbete

> Lägg till login, uppgradera React och refaktorera databasen.

### Har dold scope

Framtida idéer ska inte implementeras bara för att de "ändå ligger nära".

## 24. Kvalitetskriterier

En development plan är tillräckligt bra när:

1. nästa steg kan väljas entydigt,
2. varje steg har tydligt mål och scope,
3. varje steg är verifierbart,
4. klart-kriterier är objektiva,
5. viktiga beroenden är synliga,
6. riskreducerande arbete ligger tidigt när det behövs,
7. stegen är lagom stora för en körning,
8. planen kan revideras utan att historiken förstörs,
9. status är separerad från plantexten.

## 25. Exit-kriterier för planeringsfasen

Planeringsfasen är klar när:

- första säkra development step kan väljas,
- must-scope har täckning i planen,
- blockerande risker har egna steg eller är explicit blockerande,
- varje tidigt steg har verifiering och klart-kriterier,
- planen är konsistent med functional spec, architecture och deploymentförutsättningar.
