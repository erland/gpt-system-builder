# System Builder – Next-step state machine

## 1. Syfte

Detta dokument definierar den canonical state machine som styr System Builders beteende när användaren säger exempelvis:

- "Gör nästa steg"
- "Fortsätt"
- "Ta nästa"
- "Implementera nästa steg"

Målet är att nästa steg alltid väljs från projektets faktiska state, inte från konversationsminne eller en mekanisk `current + 1`.

## 2. Canonical state machine

```text
READ
  ↓
ASSESS
  ↓
SELECT
  ↓
LOCK
  ↓
IMPLEMENT
  ↓
VERIFY
  ↓
REVIEW
  ↓
UPDATE DOCS
  ↓
UPDATE STATUS
  ↓
PACKAGE / COMMIT
  ↓
STOP
```

Normal körning ska sluta efter exakt ett completed development step.

## 3. Prioritetsregel

Nästa åtgärd bestäms av faktisk projektstatus.

Prioritetsordning:

1. blocking issues
2. failed required verification
3. source drift / state inconsistency
4. repair required for active step
5. incomplete selected step
6. dependency prerequisites
7. first safe incomplete planned step
8. release/readiness work when implementation scope is complete

Planens numeriska ordning är en stark default, men blockerare och verkligt state går före.

## 4. READ

System Builder ska läsa tillräckligt underlag för att kunna välja säkert.

I target system repo:

1. användarens aktuella instruktion,
2. `AGENTS.md` om den finns,
3. `.system-builder/work-status.yaml`,
4. aktiv development plan,
5. relevanta current-state-dokument,
6. `.system-builder/project.yaml`,
7. traceability/deployment profile när relevant,
8. aktuell kod/test/build state.

I System Builder-projektets egen utveckling används dess `project-status.yaml` motsvarande som primärt utvecklingsstate.

### Regel

Chat history får hjälpa förstå kontext men får inte ersätta repository state.

## 5. ASSESS

Före val av steg ska System Builder kontrollera:

- finns blockerare?
- finns failed verification?
- finns selected/in-progress step?
- är previous step faktiskt completed?
- är dependencies uppfyllda?
- har source drift skett?
- motsäger plan och state varandra?
- har ny risk gjort planordningen osäker?
- finns ett repair-behov?

Resultatet av ASSESS ska leda till ett av:

- continue selected step,
- repair,
- unblock,
- select next planned step,
- update plan,
- release/readiness action.

## 6. Selected step

Om work status redan har ett `selected_step` eller `in_progress`-steg ska System Builder normalt fortsätta eller reparera detta steg innan ett nytt väljs.

Undantag:

- användaren avbryter explicit,
- steget har blivit irrelevant,
- blockerare gör fortsatt arbete osäkert,
- planen måste revideras.

## 7. SELECT

SELECT väljer exakt ett utvecklingssteg eller en explicit repair/unblock-action.

Valet ska baseras på:

- plan,
- dependencies,
- blockers,
- verification state,
- risk,
- current source.

System Builder ska inte välja ett steg bara för att dess ID är nästa nummer.

## 8. LOCK

Innan implementation ska valt steg låsas i work status.

Exempel:

```yaml
active_work:
  mode: CHANGE
  selected_step: DEV-014
  state: in_progress
```

LOCK gör att en avbruten körning kan återupptas utan att ett nytt steg väljs av misstag.

## 9. IMPLEMENT

System Builder implementerar:

- valt stegs scope,
- nödvändiga följdändringar,
- inga orelaterade features/refactors.

Om implementationen avslöjar större ny scope ska steget inte växa obegränsat. Använd plan-change-regler:

- split,
- insert,
- block,
- defer.

## 10. VERIFY

Kör required verification definierad i steget och den extra regression som faktisk ändring kräver.

Resultat:

### PASS
Steget kan gå vidare till REVIEW.

### WARNING
Får gå vidare endast om varningen är icke-blockerande och dokumenterad.

### FAIL
Steget får inte markeras completed.

### BLOCKED
Arbetet stannar i blockerad status.

## 11. REVIEW

Kontrollera före completion:

- done criteria,
- scope creep,
- regressions,
- security baseline,
- docs impact,
- traceability,
- repository hygiene,
- deployment impact.

REVIEW är inte en full specialistgranskning för varje steg, utan en systematisk completion check.

## 12. UPDATE DOCS

Uppdatera endast dokument som faktiskt påverkas.

Current-state docs ska spegla nytt current state efter completed change.

Historical docs ska bevara rationale när relevant.

System Builder ska undvika:
- dokumentändring bara för versionsbrus,
- duplicerad status,
- stale architecture/spec.

## 13. UPDATE STATUS

Efter verifiering ska state uppdateras från faktisk outcome.

PASS:
- selected step → completed
- completion evidence registreras
- next recommended räknas om

FAIL:
- selected step förblir in_progress/failed
- failure registreras
- next recommended blir repair/fix, inte nästa plansteg

BLOCKED:
- blocker registreras
- next recommended blir unblock action

## 14. PACKAGE / COMMIT

### ZIP mode

Efter completed step:
- bygg komplett projekt-ZIP,
- integritetskontroll,
- leverera artifact.

### GitHub mode

Efter completed step:
- commit relevanta changes,
- push till aktiv branch,
- uppdatera/återanvänd PR enligt GitHub-policy.

## 15. STOP

Efter ett normalt completed step ska System Builder stoppa.

Den ska:
- rapportera vad som slutförts,
- ange verifieringsresultat,
- länka artifact/PR där relevant,
- ange nästa rekommenderade steg.

Den ska inte automatiskt påbörja nästa steg.

## 16. Failure handling

Om required verification misslyckas:

```text
VERIFY FAIL
→ UPDATE STATUS as failed/in_progress
→ RECOMMEND REPAIR
→ PACKAGE only if useful and safe
→ STOP
```

Nästa användarkommando `"Gör nästa steg"` ska då reparera felet före nytt plansteg.

## 17. Blocker handling

Om blockerare upptäcks:

```text
ASSESS
→ BLOCKER FOUND
→ select unblock/analysis action
→ do not start dependent step
```

Blockerare kan vara:

- saknad access,
- unresolved architecture decision,
- unsafe migration,
- failing baseline,
- missing critical dependency,
- source/state conflict.

## 18. Source drift

Source drift betyder att repository/source har förändrats så att work status eller plan kan vara stale.

Exempel:
- användaren har ändrat kod manuellt,
- annan branch har mergats,
- ZIP har annan version än status antar,
- active PR har nya commits.

Vid drift:

1. läs diff/current source,
2. bedöm påverkan,
3. reparera state/plan,
4. fortsätt först när current state är förstått.

## 19. State inconsistency

Exempel:

- work status säger DEV-006 completed men required file saknas,
- plan säger steg ej gjort men traceability säger implemented,
- selected step saknas i planen,
- completed dependency är faktiskt failing.

System Builder ska prioritera faktisk evidens.

Maskinstate ska repareras från source + verifiering, inte tvärtom.

## 20. Repair mode

Repair används när ett tidigare steg inte är komplett trots att användaren vill fortsätta.

Repair kan:

- fixa failing tests,
- återställa missing artifact,
- synka state,
- korrigera docs,
- slutföra incomplete step.

Repair är normalt del av samma selected step, inte ett nytt plan-ID, om scope fortfarande är samma completionarbete.

## 21. När nytt repair-step behövs

Skapa nytt DEV-step om repair:

- är stort,
- har egen risk,
- påverkar flera områden,
- inte rimligen ryms inom ursprungligt steg,
- behöver egen verifiering/history.

## 22. Plan drift

Om verkligheten visar att planen bör ändras:

- dokumentera varför,
- uppdatera framtida steg,
- återanvänd inte gamla ID:n för ny betydelse,
- synka traceability/status.

System Builder får inte följa en uppenbart felaktig plan bara för att den är dokumenterad.

## 23. Next recommended

`next_step.recommended` ska representera **nästa säkra åtgärd**, inte bara nästa plan-ID.

Exempel:

```yaml
next_step:
  recommended: DEV-014
  title: Add GitHub adapter
  reason: Dependencies complete and no blockers.
```

eller:

```yaml
next_step:
  recommended: repair
  title: Repair failing migration test
  reason: DEV-013 cannot be completed while required migration verification fails.
```

## 24. No hidden continuation

System Builder ska inte:

- markera flera steg completed i samma normala körning,
- implementera nästa steg "när den ändå är igång",
- gå vidare efter failed verification,
- låta chat memory bli enda bevis på completion.

## 25. User override

Användaren får explicit:

- välja annat framtida steg,
- be om flera steg,
- ändra plan,
- avbryta current step.

System Builder ska då bedöma dependencies/risk och varna/blockera om valet är osäkert.

Explicit användarinstruktion ersätter inte säkerhets- eller faktisk blockerare.

## 26. State transition model

Tillåtna huvudtransitioner:

```text
planned
→ selected
→ in_progress
→ completed
```

Alternativa:

```text
in_progress → failed
in_progress → blocked
failed → in_progress
blocked → in_progress
planned → cancelled
planned → deferred
```

`completed` ska normalt inte återgå till `in_progress` utan source drift eller explicit re-open.

## 27. Completion evidence

Completed step ska ha evidens som passar steget.

Exempel:
- build pass,
- tests pass,
- schema validation,
- artifact checksum,
- container health,
- manual acceptance outcome.

Evidens kan sammanfattas i work status utan att duplicera hela loggen.

## 28. Small-project state machine

Samma state machine gäller även small projects.

Skillnaden är färre artefakter och kortare ASSESS/REVIEW, inte att state discipline försvinner.

## 29. ZIP-specific resume

En ZIP ska vara self-contained nog för resume.

Minst när System Builder state används:
- plan,
- work status,
- project metadata,
- relevanta canonical docs,
- source,
- tests.

## 30. GitHub-specific resume

GitHub resume ska kunna härledas från:
- repository branch/PR,
- work status,
- plan,
- source,
- CI.

Chatten får inte vara enda platsen som berättar vilken PR/branch som är aktiv.

## 31. Acceptance of warnings

En warning får inte tyst behandlas som pass.

System Builder ska:
- dokumentera warning,
- ange varför den inte blockerar,
- säkerställa att release readiness senare omprövar den.

## 32. Release transition

När inga development steps återstår ska next recommended inte bli "inget".

Den ska övergå till relevant:
- release readiness,
- packaging,
- acceptance,
- documentation,
- release.

## 33. Anti-patterns

Undvik:

- `next = current + 1`,
- flera steg per körning,
- completion utan verification,
- stale selected_step,
- blockerare i prose men inte state,
- plan som körs trots source drift,
- ny PR för varje delsteg,
- "allt klart" utan release readiness.

## 34. Exit-kriterier för SB-19

SB-19 är klart när:

- hela state machine är definierad,
- selection priority är explicit,
- lock/resume-regler finns,
- failure/blocker/source-drift hantering finns,
- repair-regler finns,
- completion evidence definieras,
- ZIP/GitHub resume täcks,
- STOP efter ett steg är explicit.
