# System Builder – ZIP-läge

## 1. Syfte

ZIP-läge används när användaren levererar ett helt eller delvis utvecklat system som ZIP och vill att System Builder ska analysera, planera, ändra eller fortsätta arbetet stegvis.

ZIP ska behandlas som ett first-class source mode, inte som ett tillfälligt filformat.

Målet är att varje levererad ZIP ska vara tillräckligt komplett för att arbetet ska kunna återupptas utan konversationsminne.

## 2. Grundprincip

> ZIP in → analysera faktisk source → genomför exakt ett säkert steg → verifiera → bygg komplett ny ZIP → stoppa.

System Builder ska inte arbeta från gamla extraherade filer om användaren har laddat upp en nyare ZIP.

## 3. ZIP som source of truth

När en aktuell ZIP är användarens källa gäller:

1. användarens aktuella instruktion,
2. innehållet i den aktuella ZIP:en,
3. `AGENTS.md`,
4. `.system-builder/work-status.yaml`,
5. aktiv plan/current-state-dokument,
6. kod/test,
7. generell System Builder Knowledge.

Chat history är sekundär.

## 4. Import

Vid import ska System Builder:

1. identifiera ZIP-filen,
2. verifiera att den går att läsa,
3. inspektera root shape,
4. extrahera säkert,
5. identifiera projektrot,
6. läsa canonical state om det finns,
7. bedöma om ZIP:en representerar CREATE, CHANGE, IMPROVE eller annan fas.

## 5. Säker extraktion

ZIP-extraktion ska skydda mot:

- `../` path traversal,
- absoluta paths,
- paths som lämnar projektroten,
- symlink-problem när runtime kan representera dem,
- orimligt stora eller uppenbart skadliga archives när relevant.

System Builder ska inte skriva filer utanför vald workspace-root.

## 6. Root-shape detection

ZIP kan exempelvis innehålla:

### Direkt projektrot

```text
README.md
src/
docs/
```

### Wrapper directory

```text
my-project/
  README.md
  src/
  docs/
```

System Builder ska identifiera projektroten utan att skapa dubbla wrappers i output.

Output-ZIP ska normalt representera projektets root direkt om projektets build/packaging-regler inte säger annat.

## 7. Repository state discovery

Efter extraktion ska System Builder söka efter:

- `AGENTS.md`
- `.system-builder/project.yaml`
- `.system-builder/work-status.yaml`
- `.system-builder/traceability.yaml`
- `.system-builder/deployment-profile.yaml`
- `docs/development-plan.md`
- `docs/functional-specification.md`
- `docs/architecture.md`
- build/test files
- `.gitignore`
- `.dockerignore`
- CI workflows.

Saknade state-filer är inte automatiskt fel; behovet styrs av projektets mognad och komplexitet.

## 8. Existing System Builder state

Om ZIP:en redan har `.system-builder/` ska den användas som machine state efter validering.

System Builder ska kontrollera:

- schema validity,
- selected step,
- blockers,
- verification,
- source drift,
- plan/state consistency.

Felaktigt state repareras från faktisk source och evidens.

## 9. ZIP utan System Builder state

Om ett befintligt system saknar state ska System Builder:

1. analysera faktisk source,
2. identifiera mode,
3. skapa minsta nödvändiga `.system-builder/` state,
4. inte fabricera completed history,
5. dokumentera vad som härletts.

För ett nytt projekt kan CREATE-state initieras.

## 10. Source drift mellan ZIP-versioner

Om användaren laddar upp en ny ZIP mellan körningar ska System Builder inte anta att den är identisk med föregående output.

Kontrollera när praktiskt:

- version,
- checksum,
- filskillnader,
- work status,
- selected step.

Om source har ändrats externt ska ASSESS avgöra om state/plan behöver repareras innan nästa steg.

## 11. Checksum

System Builder bör beräkna SHA-256 för levererad output-ZIP.

Checksum används som:

- artifact identity,
- felsökningshjälp,
- enkel driftindikator.

Checksum ersätter inte Git-history.

## 12. ZIP development loop

Normal ZIP-körning:

```text
RECEIVE ZIP
→ SAFE EXTRACT
→ READ STATE
→ ASSESS
→ SELECT ONE STEP
→ LOCK
→ IMPLEMENT
→ VERIFY
→ REVIEW
→ UPDATE DOCS/STATE
→ HYGIENE
→ BUILD COMPLETE ZIP
→ VERIFY ZIP
→ DELIVER
→ STOP
```

## 13. Ett steg per ZIP

Normalregel:

- en input-ZIP,
- ett completed development step,
- en output-ZIP.

Användaren kan uttryckligen be om flera steg, men System Builder ska då fortfarande hålla state och verifiering per steg.

## 14. Output completeness

Output-ZIP ska vara komplett för projektet.

Den får inte bara innehålla ändrade filer.

Den ska normalt innehålla:

- hela source tree,
- current-state docs,
- machine state,
- tests,
- scripts,
- configuration,
- build files,
- relevanta CI/deployment files.

## 15. Generated artifacts

Projektets egna genererade artefakter ska bara ligga i ZIP om projektets packaging-regler kräver det.

Typiskt ska följande exkluderas från source ZIP:

- `node_modules/`
- build cache,
- `.venv/`
- `target/`
- `dist/` när det endast är transient build output,
- OS/editor files,
- temporära testartefakter.

Repositoryts `.gitignore` och hygiene-policy ska styra.

## 16. ZIP filename

Output bör ha begripligt namn.

Exempel:

```text
my-system-project-v0.3.0-dev.zip
my-system-project-sb17.zip
```

System Builder ska inte förlita sig på filnamnet som enda versionskälla.

## 17. Version

Om projektet har canonical versionfil ska den respekteras.

Utvecklingssteg behöver inte automatiskt bumpa releaseversion.

För non-release artifacts får:

- dev,
- rc,
- step suffix

användas för tydlighet.

Releaseversion ska styras av projektets releasepolicy.

## 18. ZIP integrity verification

Innan leverans ska System Builder minst:

- öppna ZIP:en,
- testa CRC/integritet,
- kontrollera required files,
- säkerställa att projektroten är korrekt,
- kontrollera att output inte råkat packa sig själv.

## 19. Self-inclusion

Buildscript får inte inkludera output-ZIP inuti output-ZIP.

Exkludera:

- output path,
- generated distribution directory,
- temporära workspacefiler.

## 20. Project hygiene

Före ZIP-build:

- identifiera generated/temp files,
- ta bort endast hög-säkerhetsklassade skräpfiler,
- respektera canonical/history files,
- använd Git som historik när Git finns,
- dokumentera tveksamma findings hellre än att radera osäkert.

## 21. Required resume content

En System Builder-styrd ZIP ska normalt kunna återupptas med:

- project metadata,
- work status,
- development plan,
- relevant current-state docs,
- source,
- tests,
- build/validation scripts.

För small projects kan vissa artefakter saknas om de inte behövs.

## 22. Resume

När användaren återkommer med en output-ZIP och säger `"Gör nästa steg"`:

1. läs ZIP:ens state,
2. validera selected/completed/next,
3. kontrollera blockerare/drift,
4. följ next-step state machine,
5. genomför ett steg,
6. leverera ny ZIP.

System Builder ska inte kräva att användaren återberättar tidigare steg om ZIP-state är komplett.

## 23. ZIP + CHANGE

Vid CHANGE:

- läs current source,
- skapa/uppdatera CR/impact vid behov,
- uppdatera current-state docs,
- implementera ett change step,
- kör regression,
- leverera komplett ZIP.

## 24. ZIP + IMPROVE

Vid IMPROVE:

- etablera baseline,
- bevara behavior,
- implementera ett tekniskt step,
- regression,
- komplett ZIP.

## 25. ZIP + CREATE

Vid CREATE kan första implementationsteget skapa hela projektstrukturen från canonical plan.

Efter första implementationsteget ska projektet levereras som komplett ZIP och därefter fortsätta som normalt ZIP-resume.

## 26. Validation scripts

När projektet innehåller scripts för:

- schema validation,
- build,
- lint,
- tests,
- packaging,

ska System Builder använda dem före egna ad-hoc-alternativ när de är relevanta och säkra.

## 27. Unknown tooling

Om ZIP innehåller okänd stack:

- läs README/build files,
- identifiera package manager/build system,
- använd projektets egna kommandon,
- undvik att introducera ny tooling utan behov.

## 28. Binary files

System Builder ska bevara binära projektfiler som inte behöver ändras.

Den ska inte konvertera eller regenerera binärer utan skäl.

## 29. Secrets

ZIP-output får inte inkludera:

- credentials,
- riktiga `.env` secrets,
- private keys,
- tokens,

om de inte redan är explicit avsedda som test fixtures och säkert identifierade.

Om secrets upptäcks ska de behandlas som security issue.

## 30. Large archives

För stora projekt ska System Builder:

- analysera selektivt,
- undvika att läsa alla filer om det inte behövs,
- fokusera på state, plan, relevanta källfiler och tests,
- fortfarande leverera komplett ZIP.

## 31. ZIP diff summary

Efter completed step bör leveransen sammanfatta:

- completed step,
- huvudsakliga ändringar,
- verification,
- artifact checksum,
- next recommended step.

Full diff behöver inte återges i chatten.

## 32. Failure outcome

Om steget inte kan completed:

- state ska visa failure/blocker,
- ZIP får ändå levereras om den behövs för resume,
- den får inte beskrivas som completed artifact,
- nästa recommended ska vara repair/unblock.

## 33. Partial output

System Builder ska inte leverera en partial source ZIP som ser ut som fullständig projektleverans.

Om endast patch/diff efterfrågas explicit kan det göras, men default är komplett project ZIP.

## 34. Artifact naming vs project naming

Outputfilens namn får förändras utan att projektets interna namn ändras.

Interna canonical identifiers ska inte automatiskt härledas från artifact filename.

## 35. ZIP mode anti-patterns

Undvik:

- endast skicka ändrade filer,
- förlita sig på chat history,
- packa `node_modules`,
- packa tidigare ZIP i ny ZIP,
- glömma work status,
- skriva utanför workspace,
- markera step completed utan verification,
- börja nästa steg före leverans.

## 36. Exit-kriterier för SB-20

SB-20 är klart när:

- ZIP import/safe extraction definierats,
- root detection definierats,
- state discovery/resume definierats,
- source drift mellan ZIP-versioner definierats,
- one-step loop definierats,
- complete output ZIP definierats,
- hygiene/exclusions definierats,
- integrity/checksum definierats,
- failure/repair artifact-regler definierats.
