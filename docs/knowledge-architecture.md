# System Builder – Knowledge-arkitektur

## 1. Syfte

System Builder ska använda Knowledge som referensmaterial, inte som gömd runtime-logik.

Kritiska beteenderegler ska ligga i canonical instruktioner och policykontrakt. Knowledge ska stödja modellen med fördjupning, exempel, referenser och domänmaterial.

## 2. Grundprincip

> Om en regel måste följas för att System Builder ska bete sig korrekt får den inte endast finnas i Knowledge.

## 3. Tre lager

### Lager A – Canonical runtime contract

Innehåller regler som måste styra beteendet direkt:

- identitet och scope,
- CREATE / CHANGE / IMPROVE,
- next-step state machine,
- ZIP/GitHub mode,
- release readiness,
- source-of-truth-regler,
- blocker/failure-policy,
- one-step-per-run.

Dessa ska vara nåbara direkt från huvudinstruktionen, normalt utan mer än ett filhopp.

### Lager B – Canonical standards

Detaljerade styrande standarder:

- functional specification,
- architecture,
- development plan,
- risk/feasibility,
- security,
- test strategy,
- deployment,
- Docker,
- Coolify,
- operational docs.

De är fortfarande styrande, men behöver inte bäddas i huvudprompten.

### Lager C – Knowledge/reference

Referensmaterial som hjälper modellen men inte ensamt styr kritiskt beteende:

- exempel,
- glossary,
- technology notes,
- platform references,
- checklists,
- style guides,
- reusable patterns.

## 4. Knowledge får innehålla

Knowledge passar för:

- förklaringar,
- exempel,
- referensmönster,
- tekniska jämförelser,
- API-/plattformssammanfattningar,
- domänspecifik terminologi,
- vanliga fallgropar,
- exempelprojekt.

## 5. Knowledge får inte vara enda plats för

Följande får inte endast ligga i Knowledge:

- "ett steg per körning",
- blockerare före nästa steg,
- hur work status väljs,
- source-of-truth-prioritet,
- ZIP-outputkrav,
- PR-reuse,
- release decision-regler,
- säkerhetskritiska no-go-regler.

## 6. Runtime reachability

Core flow ska normalt vara:

```text
main instruction
→ canonical policy/standard
```

Undvik:

```text
main instruction
→ index
→ topic file
→ subtopic
→ actual rule
```

för regler som måste följas konsekvent.

## 7. Knowledge index

Knowledge ska ha ett index som beskriver:

- fil,
- syfte,
- när den ska användas,
- om den är normative eller reference.

Exempel:

| File | Purpose | Use when | Class |
|---|---|---|---|
| `knowledge/technology-patterns.md` | Technology reference | Choosing implementation approach | reference |
| `docs/docker-baseline.md` | Docker behavior contract | Docker target selected | normative |

## 8. Normative vs reference

Använd explicit klassificering:

- `normative` – styr beteende,
- `reference` – stödjer resonemang,
- `example` – visar tillämpning.

Knowledge-katalogen ska primärt innehålla `reference` och `example`.

## 9. Duplication

Undvik att kopiera samma regel till flera Knowledge-filer.

Om samma regel behöver synas på flera ställen:
- canonical källa äger formuleringen,
- övriga filer länkar/refererar.

## 10. Knowledge och Custom GPT

Custom GPT Knowledge har praktiska begränsningar i antal och storlek.

System Builder ska därför:

- prioritera få, högvärdiga filer,
- slå samman närliggande referensmaterial,
- inte lägga critical runtime rules där,
- hålla huvudinstruktionen självständig nog för kärnflödet.

## 11. Knowledge och Chat ZIP

Chat ZIP kan innehålla fler filer än Custom GPT Knowledge.

Skillnaden i distributionsformat får inte skapa olika beteendekontrakt.

Chat ZIP kan bära:
- alla canonical docs,
- examples,
- schemas,
- scripts,
- reference knowledge.

Custom GPT behöver kompilerad/kuraterad delmängd.

## 12. Runtime parity

Chat ZIP och Custom GPT ska dela:

- samma identitet,
- samma modes,
- samma step-policy,
- samma source-of-truth,
- samma blocker/failure behavior,
- samma release semantics.

Skillnader får finnas i hur mycket referensmaterial som är direkt tillgängligt, inte i core behavior.

## 13. Knowledge selection

När Custom GPT byggs ska Knowledge väljas efter:

1. hög återanvändningsgrad,
2. hög beslutspåverkan,
3. låg duplicering,
4. stabilitet över tid,
5. rimlig filstorlek.

## 14. Knowledge anti-patterns

Undvik:

- en fil per liten regel,
- duplicerad policytext,
- stora dumpade dokument utan index,
- gamla versionskopior,
- critical rules enbart i Knowledge,
- exempel som ser ut som canonical policy,
- runtime som kräver flera filhopp.

## 15. Aktualitet

Reference Knowledge som kan bli gammal ska:

- vara tydligt märkt,
- helst länka till aktuell extern källa i stället för att låtsas vara permanent,
- uppdateras separat från canonical beteendekontrakt.

## 16. Web och Knowledge

För tidskänsliga tekniska fakta ska System Builder kunna använda webben när den finns tillgänglig.

Knowledge ska inte användas som ursäkt för att behandla gammal produkt-/plattformskunskap som aktuell fakta.

## 17. Exempelstruktur

```text
knowledge/
  README.md
  technology-patterns.md
  platform-reference.md
  terminology.md
```

Canonical styrning ligger fortsatt under `docs/`.

## 18. Knowledge README

`knowledge/README.md` ska ange:

- syftet med Knowledge,
- klassificeringsregler,
- filindex,
- att canonical behavior finns i docs/instructions,
- hur filer väljs till Custom GPT.

## 19. File size

Filer ska vara tillräckligt fokuserade för retrieval.

För stora omnibusfiler kan delas, men splittring får inte skapa onödiga filhopp.

## 20. Naming

Använd stabila beskrivande namn.

Bra:
- `technology-patterns.md`
- `platform-reference.md`

Undvik:
- `misc.md`
- `notes2.md`
- `final-knowledge.md`

## 21. Knowledge lifecycle

När systemet utvecklas:

1. uppdatera canonical docs först,
2. bedöm om reference material påverkas,
3. uppdatera Knowledge,
4. bygg distributionsspecifik Knowledge senare.

## 22. Knowledge validation

Validering ska kunna kontrollera:

- index finns,
- varje Knowledge-fil är klassificerad,
- inga duplicate filenames,
- inga förbjudna critical-rule-only markers,
- refererade filer finns.

## 23. System Builder initial Knowledge

Initialt bör Knowledge hållas litet.

För SB-29 etableras:

- `knowledge/README.md`
- `knowledge/technology-patterns.md`
- `knowledge/platform-reference.md`
- `knowledge/terminology.md`

Dessa är reference-material och ska inte vara runtime-kritiska.

## 24. Technology patterns

Kan sammanfatta generella val, exempelvis:

- modular monolith som default för mindre system,
- external PostgreSQL för relationsdata,
- stateless services,
- Docker som vanlig packagingform,
- risk-first spikes.

Det får inte duplicera full canonical architecture/deployment policy.

## 25. Platform reference

Kan innehålla kort referens till:

- GitHub,
- Docker,
- Coolify,
- PostgreSQL,
- generic container platforms.

Tidskänsliga detaljer ska verifieras när de används.

## 26. Terminology

Terminologi hjälper modellen hålla stabil betydelse för:

- current-state docs,
- work series,
- selected step,
- blocker,
- acceptance,
- release readiness,
- packaging,
- deployment.

## 27. Custom GPT compilation

I senare steg ska en compiler välja:
- huvudinstruktion,
- ett begränsat Knowledge-set,
- schemas/examples endast när de ger runtimevärde.

## 28. Chat ZIP runtime

I Chat ZIP kan modellen läsa hela projektet, men runtime-instruktionen ska fortfarande prioritera canonical filer och inte göra "sök allt" till normalflöde.

## 29. Specialistgräns

Knowledge får beskriva när specialist-GPT är lämplig, men System Builder ska inte bli beroende av specialist för sitt core lifecycle.

## 30. Exit-kriterier för SB-29

SB-29 är klart när:

- normative/reference/example är definierade,
- core runtime reachability är definierad,
- Knowledge-index finns,
- initial Knowledge-struktur finns,
- Chat ZIP/Custom GPT parity-regel finns,
- validation finns,
- inga critical behavior rules ligger enbart i Knowledge.
