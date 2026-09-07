# System Builder – Funktionell specifikation

## 1. Syfte

`docs/functional-specification.md` är canonical current-state-beskrivning av **vad systemet ska göra**.

Dokumentet ska vara:

- människoläsbart,
- tillräckligt precist för arkitektur och utvecklingsplanering,
- verifierbart,
- stabilt över tid,
- uppdaterat efter genomförda funktionella förändringar.

Det ska inte vara:

- en implementation plan,
- en teknisk arkitekturbeskrivning,
- en historisk ändringslogg,
- en samling osorterade idéer.

## 2. Grundprincip

> Beskriv avsett beteende, regler, aktörer, information och acceptans utan att låsa implementation mer än nödvändigt.

System Builder ska skilja på:

- **behov** – varför något behövs,
- **funktionellt krav** – vad systemet ska kunna göra,
- **acceptance criterion** – hur vi avgör om kravet är uppfyllt,
- **design/implementation** – hur lösningen byggs.

## 3. När dokumentet ska finnas

### CREATE

Skapas innan bred implementation påbörjas.

För små projekt får det vara kompakt men ska minst täcka:

- syfte,
- scope,
- centrala aktörer/flöden,
- must-krav,
- centrala acceptance criteria,
- out of scope.

### CHANGE

Befintlig spec ska läsas och uppdateras om förändringen ändrar systemets avsedda beteende.

Större förändringar får ha en separat `docs/changes/CR-xxx-.../request.md`, men när ändringen är klar ska resultatet integreras i current-state-specen.

### IMPROVE

Ren teknisk förbättring behöver normalt inte ändra functional spec om avsett beteende är oförändrat.

## 4. Rekommenderad struktur

```text
# Funktionell specifikation

## 1. Syfte och mål
## 2. Scope
## 3. Aktörer
## 4. Centrala användningsfall
## 5. Funktionella krav
## 6. Affärsregler
## 7. Informationsbehov
## 8. Integrationer
## 9. Behörighet
## 10. Fel- och undantagsfall
## 11. Icke-funktionella krav
## 12. Acceptance criteria
## 13. Out of scope
## 14. Öppna frågor
```

Strukturen får förenklas för små projekt och utökas när domänen kräver det.

## 5. Syfte och mål

Beskriv:

- vilket problem systemet löser,
- för vem,
- vilket önskat resultat som ska uppnås,
- eventuella success criteria som är relevanta.

Undvik implementationstermer om de inte faktiskt är ett krav.

Dåligt:

> Systemet ska använda React och PostgreSQL för att ge användaren bättre överblick.

Bättre:

> Systemet ska ge användaren en samlad överblick över sina aktiva projekt och deras status.

Teknikval hör normalt hemma i arkitekturen.

## 6. Scope

Dela normalt upp i:

- **Must**
- **Should**
- **Could**
- **Out of scope**

Första release/MVP får definieras när det förbättrar tydligheten.

Scope ska göra det möjligt att säga nej till idéer som inte hör till aktuell leverans.

## 7. Aktörer

Identifiera externa roller som interagerar med systemet.

Exempel:

- administratör,
- registrerad användare,
- extern tjänst,
- batch/integrationssystem.

Beskriv aktörernas ansvar och rättigheter på verksamhetsnivå.

Tekniska komponenter ska inte listas som aktörer om de inte representerar ett externt system.

## 8. Centrala användningsfall

Beskriv de viktigaste end-to-end-flödena.

Varje use case bör normalt innehålla:

- namn,
- primär aktör,
- mål,
- preconditions när relevanta,
- huvudflöde,
- viktiga alternativ/undantag,
- resultat.

Undvik att beskriva varje knapptryckning om inte UI-beteendet är viktigt för kravet.

## 9. Funktionella krav

### 9.1 ID

Krav som behöver spårbarhet får stabila ID:n:

- `FR-001`
- `FR-002`

ID ska inte återanvändas för annan betydelse.

### 9.2 Form

Ett funktionellt krav ska:

- beskriva observerbart eller domänmässigt beteende,
- ha en tydlig aktör/systemtrigger när relevant,
- kunna kopplas till verifiering,
- undvika onödiga implementation details.

Bra:

> **FR-012 – Skapa repository**  
> En behörig användare ska kunna skapa ett nytt repository från en uppladdad projekt-ZIP.

Svagare:

> Backend ska anropa GitHub REST API med POST.

Det senare hör normalt till arkitektur/implementation.

### 9.3 Prioritet

Använd:

- `Must`
- `Should`
- `Could`

Out-of-scope uttrycks normalt inte som aktivt FR-krav.

### 9.4 Status

Specifikationen ska normalt inte använda runtime-status som `implemented` eller `verified`.

Sådan status hör hemma i `.system-builder/traceability.yaml` eller work state.

## 10. Affärsregler

Affärsregler är domänregler som gäller oberoende av UI eller implementation.

Exempel:

> **BR-001** Ett projekt får endast arkiveras av en användare med administratörsbehörighet.

Stabila ID:n används när regler behöver refereras från flera krav eller tester.

## 11. Informationsbehov

Beskriv vilken information systemet behöver hantera på konceptuell nivå.

Exempel:

- användare,
- projekt,
- repository,
- status,
- deploymentmiljö.

Här ska inte full fysisk databasschema-design göras.

## 12. Integrationer

Beskriv externa system ur ett funktionellt perspektiv:

- vilket system,
- vilket informations-/funktionsutbyte,
- riktning,
- kritiska fel-/fallback-situationer,
- eventuell användarsynlig påverkan.

Protokoll, SDK-versioner och klientbibliotek hör normalt hemma i arkitekturen.

## 13. Behörighet

Beskriv:

- vilka aktörer som får göra vad,
- ägarskap,
- synlighet,
- eventuella rollskillnader,
- vilka funktioner som kräver särskild behörighet.

Detaljerad auth-teknik hör till arkitektur.

## 14. Fel- och undantagsfall

Beskriv beteenden som är viktiga för användaren eller verksamhetsreglerna.

Exempel:

- extern integration är otillgänglig,
- uppladdad fil är ogiltig,
- objekt finns redan,
- användaren saknar behörighet,
- operation är delvis genomförd.

Felhantering ska inte bara beskrivas som "visa felmeddelande" om domänkonsekvenser finns.

## 15. Icke-funktionella krav

Använd `NFR-xxx` när spårbarhet behövs.

Vanliga områden:

- prestanda,
- tillgänglighet,
- säkerhet,
- tillgänglighet/accessibility,
- observability,
- datalagring,
- återställning,
- portability,
- driftbarhet.

Ett NFR ska vara så verifierbart som rimligt.

Svagt:

> Systemet ska vara snabbt.

Bättre:

> **NFR-003** För normala listvyer ska 95 % av serveranropen slutföras inom 500 ms vid upp till 100 samtidiga användare i avsedd produktionsmiljö.

Exakta nivåer ska inte hittas på utan användarstöd eller tydlig projektgrund.

## 16. Acceptance criteria

Acceptance criteria beskriver hur det avgörs att ett krav eller use case fungerar som avsett.

Stabila ID:n:

- `AC-001`
- `AC-002`

Ett AC ska normalt vara:

- konkret,
- observerbart,
- verifierbart,
- kopplat till ett eller flera krav.

Exempel:

> **AC-021** När en behörig användare laddar upp en giltig projekt-ZIP och väljer "Skapa repository" ska repositoryt skapas och användaren få en länk till det skapade repositoryt.

Undvik att acceptance criteria bara återupprepar kravtext ordagrant.

## 17. Out of scope

Out of scope ska vara explicit där det finns realistisk risk för missförstånd.

Exempel:

- ingen multi-tenancy i första release,
- ingen mobilapp,
- ingen automatisk produktionsdeployment,
- ingen import från annan leverantör.

Detta skyddar development plan mot scope creep.

## 18. Öppna frågor

Öppna frågor ska klassificeras som:

- **blocking** – måste lösas innan relevant implementation,
- **non-blocking** – kan lösas senare.

System Builder ska inte fortsätta genom en blocking fråga som materiellt gör design eller verifiering osäker.

## 19. Kvalitetskriterier

En funktionell specifikation är tillräckligt bra när:

1. problem och mål är begripliga,
2. must-scope är tydlig,
3. aktörer och huvudflöden är identifierade,
4. centrala krav är observerbara/verifierbara,
5. implementation details är begränsade till verkliga krav,
6. affärsregler och behörighet är synliga när relevanta,
7. viktiga fel-/undantagsfall finns,
8. centrala acceptance criteria finns,
9. out-of-scope är explicit där relevant,
10. blockerande öppna frågor är synliga,
11. dokumentet beskriver current state och inte bara förändringshistorik.

## 20. Anti-patterns

System Builder ska undvika:

### Teknisk lösning förklädd till krav

> "Använd Kafka för events."

om det egentliga behovet är:

> "Händelser ska kunna levereras asynkront mellan delsystem."

### Vaga kvalitetsord

> snabbt, säkert, intuitivt, skalbart

utan konkret innebörd.

### Krav som inte går att avgöra

> Systemet ska vara användarvänligt.

### Fullständig UI-detaljering för tidigt

Beskriv beteende och informationsbehov först. Pixel- och komponentdesign hör bara hemma här om den är en del av själva kravet.

### Dubbletter

Samma krav ska inte finnas i flera avsnitt med olika formulering.

### Historik i current state

> "Tidigare gjorde systemet X men från version 2 gör det Y."

Detta hör i change history/decision record om historiken behöver bevaras. Current spec ska beskriva Y.

## 21. CREATE-regel

Vid CREATE:

1. börja från behov/discovery,
2. skapa en första sammanhängande spec,
3. markera blockerande frågor,
4. undvik att implementera innan must-scope och första planeringsunderlaget är tillräckligt stabilt,
5. revidera specen när legitima beslut tas.

## 22. CHANGE-regel

Vid CHANGE:

1. läs befintlig spec och faktisk kod,
2. identifiera vilka FR/NFR/use cases som påverkas,
3. dokumentera förändringsbehov och impact,
4. uppdatera current-state-specen när den avsedda funktionen ändras,
5. bevara större historik i change request vid behov,
6. uppdatera traceability för påverkade stabila ID:n.

Ändra inte ett befintligt krav-ID:s innebörd så drastiskt att spårbarheten blir missvisande. Skapa då nytt krav och markera det gamla som ersatt i historiken.

## 23. Small-project-regel

För small-projekt får strukturen komprimeras till exempelvis:

```text
# Functional Specification

## Purpose
## Scope
## Actors and main flows
## Functional requirements
## Acceptance criteria
## Out of scope
## Open questions
```

Kvalitetsreglerna gäller fortfarande.

Tomma sektioner ska inte skapas bara för mallens skull.

## 24. Traceability

När `.system-builder/traceability.yaml` används:

- full kravtext finns endast i Markdown,
- YAML refererar stabila krav-ID:n,
- `must`-krav ska kunna följas till development steps och verifiering,
- orphan requirements ska kunna identifieras.

## 25. Exit-kriterier för functional-specification-fasen

Fasen är klar när:

- must-funktionaliteten är tillräckligt definierad för arkitektur och planering,
- centrala acceptance criteria finns,
- blockerande frågor är lösta eller explicit blockerar nästa fas,
- specen är current-state och internkonsekvent,
- krav som kräver spårbarhet har stabila ID:n.
