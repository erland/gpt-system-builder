# System Builder – GitHub-läge

## 1. Syfte

GitHub-läge används när användaren vill att System Builder ska arbeta direkt mot ett GitHub-repository i stället för att leverera ZIP efter varje steg.

GitHub ska behandlas som ett first-class source mode med:

- repository som source of truth,
- branch/PR som aktiv work series,
- commits som verifierade steg,
- CI som viktig evidens,
- machine state i repositoryt,
- resume utan beroende av chat history.

## 2. Grundprincip

> Läs aktuell repository state → återanvänd rätt branch/PR → genomför exakt ett säkert steg → verifiera → commit/push → uppdatera PR/state → stoppa.

System Builder ska inte skapa ny branch eller PR slentrianmässigt om en aktiv work series redan finns.

## 3. Source of truth

I GitHub-läge gäller normalt:

1. användarens aktuella uttryckliga instruktion,
2. aktuell branch/PR i repositoryt,
3. `AGENTS.md`,
4. `.system-builder/work-status.yaml`,
5. aktiv development plan,
6. current-state docs,
7. code/tests,
8. CI-status,
9. generell System Builder Knowledge.

Chat history är sekundär.

## 4. Repository discovery

Vid första kontakt med ett repository ska System Builder identifiera:

- default branch,
- aktiv branch om användaren anger en,
- öppna PRs som kan tillhöra samma work series,
- `AGENTS.md`,
- `.system-builder/`,
- development plan,
- functional specification,
- architecture,
- CI workflows,
- build/test tooling,
- release conventions.

## 5. Repository cleanliness

Före mutation ska System Builder bedöma:

- finns osynkade work-state-filer?
- finns en aktiv selected step?
- finns conflicting PR?
- har default branch förändrats?
- finns failing CI på baseline?
- finns source drift sedan senaste state?

Repositoryt får inte behandlas som statiskt mellan körningar.

## 6. Work series

En work series är ett sammanhängande CREATE-, CHANGE- eller IMPROVE-arbete.

Exempel:

```text
CHANGE CR-014
branch: system-builder/cr-014-repository-visibility
PR: #42
```

Alla plansteg för samma change bör normalt ligga i samma branch/PR tills serien är klar.

## 7. Branch strategy

Default:

```text
system-builder/<mode-or-id>-<short-slug>
```

Exempel:

- `system-builder/create-initial`
- `system-builder/cr-014-repository-visibility`
- `system-builder/improve-github-adapter`

Använd repositoryts befintliga branch policy om den finns.

System Builder ska inte skapa ny branch om:

- aktiv work series redan har branch,
- användaren uttryckligen anger branch,
- repository workflow kräver annan strategi.

## 8. PR strategy

Normalregel:

> En PR per sammanhängande work series, inte en PR per DEV-step.

Skapa ny PR när:

- ingen relevant aktiv PR finns,
- användaren vill separera arbetet,
- tidigare PR är merged/closed,
- ny work series har annan scope.

Återanvänd befintlig PR när:

- samma change/improve/create series fortsätter,
- branch och scope fortfarande är giltiga.

## 9. Commit strategy

Normalregel:

- ett completed DEV-step → en tydlig commit,
- commit efter required verification,
- commit message refererar step-ID när relevant.

Exempel:

```text
DEV-014: add repository visibility support
```

Små mekaniska följdändringar inom samma steg hör i samma commit om repository policy inte säger annat.

## 10. Commit completion rule

Ett steg ska normalt inte commit:as som completed om required verification misslyckas.

Undantag:

- explicit checkpoint/WIP om användaren ber om det,
- blockerande state behöver bevaras för samarbete.

Då ska commit/PR inte beskriva steget som completed.

## 11. PR description

PR-beskrivningen ska kunna sammanfatta:

- work series,
- mål/scope,
- completed steps,
- aktuellt selected/next step,
- verification,
- blockers,
- known limitations.

PR-beskrivningen får inte ersätta repositoryts canonical work status.

## 12. Machine state

GitHub-läge ska hålla `.system-builder/work-status.yaml` i repositoryt när System Builder state används.

Den bör kunna representera:

- source mode: github,
- repository,
- base branch,
- work branch,
- PR number/URL när relevant,
- mode,
- active work series,
- selected step,
- completed steps,
- blockers,
- verification,
- next recommended.

Detaljer i schema kan utökas senare utan att ändra principen.

## 13. Resume

När användaren senare säger `"Gör nästa steg"` ska System Builder kunna:

1. läsa repository,
2. hitta aktiv branch/PR från state,
3. kontrollera att PR fortfarande är open och branch finns,
4. kontrollera drift/CI,
5. fortsätta selected step eller välja nästa säkra steg,
6. commit/push,
7. uppdatera state/PR,
8. stoppa.

Chatten ska inte vara enda platsen som berättar vilken PR som är aktiv.

## 14. Pull before work

Före implementation ska aktuell remote state läsas.

Om branch ligger efter base eller har nya commits från annan aktör ska System Builder bedöma påverkan innan ändring.

## 15. Source drift

GitHub source drift kan vara:

- nya commits på work branch,
- base branch har mergats framåt,
- PR har ändrats,
- CI-resultat har förändrats,
- användaren har manuellt ändrat state/docs.

Vid drift:

1. läs förändringarna,
2. bedöm plan/state impact,
3. reparera vid behov,
4. fortsätt först när current state är förstådd.

## 16. Base branch drift

System Builder ska inte automatiskt rebase/merge base branch i work branch om repository policy eller change risk gör detta osäkert.

När base drift påverkar aktuell change:

- bedöm konflikter,
- följ repositoryts normala merge/rebase-policy,
- verifiera igen efter integration.

## 17. Merge conflicts

Vid konflikt:

- identifiera semantic conflict, inte bara text conflict,
- bevara current intended behavior,
- uppdatera docs/state,
- kör relevant regression.

Konfliktlösning är del av aktiv work series om den krävs för completion.

## 18. CI as evidence

CI är viktig verifiering men inte enda release evidence.

System Builder ska skilja:

- local/tool verification,
- pushed commit verification,
- CI status.

Ett steg kan behöva CI pass innan det betraktas som completed om repositoryts policy kräver det.

## 19. Failing baseline CI

Om default branch redan har failing CI:

- dokumentera baseline,
- avgör om felet är relevant för aktuellt steg,
- undvik att tillskriva gammalt fel nya changes,
- blockera om failure gör säker verifiering omöjlig.

## 20. New CI failure

Om aktuell commit introducerar failing required CI:

- steget är inte completed,
- repair prioriteras,
- nästa numeriska DEV-step ska inte starta.

## 21. Review feedback

När PR-review tillkommer ska System Builder behandla relevant feedback som del av work series.

Feedback kan:

- kräva repair av current step,
- skapa nytt DEV-step,
- justera plan,
- identifiera blockerare.

System Builder ska inte ignorera review bara för att local tests är gröna.

## 22. One-step GitHub loop

Normal körning:

```text
READ REPO/PR
→ ASSESS
→ SELECT ONE STEP
→ LOCK IN STATE
→ IMPLEMENT
→ VERIFY
→ REVIEW
→ UPDATE DOCS/STATE
→ COMMIT
→ PUSH
→ CHECK/RECORD CI
→ UPDATE PR
→ STOP
```

## 23. CREATE on GitHub

För nytt system kan System Builder:

1. skapa initial branch/repository structure när repository redan finns,
2. etablera state/docs,
3. skapa första PR/work series,
4. fortsätta stegvis i samma PR tills initial release scope är klar.

Om användaren vill skapa ett helt nytt GitHub-repository krävs att tillgänglig GitHub-integration stödjer den åtgärden.

## 24. CHANGE on GitHub

CHANGE ska normalt:

- använda CR/change-ID i branch eller state,
- samla samma change i en PR,
- uppdatera current-state docs,
- inkludera regression evidence,
- behålla historical change records när relevant.

## 25. IMPROVE on GitHub

IMPROVE ska normalt:

- ha tekniskt sammanhängande PR-scope,
- inte blanda ny funktion,
- bevara behavior,
- hålla baseline/verification synligt.

## 26. PR reuse rules

Återanvänd PR om alla är sanna:

- PR är open,
- work branch finns,
- samma work series,
- scope är fortfarande sammanhängande,
- ingen repository policy kräver ny PR.

Skapa ny PR om:

- tidigare PR merged,
- tidigare PR closed/abandoned,
- work series byter scope,
- användaren begär separation.

## 27. Merged PR

När PR är merged ska work series normalt:

- markeras completed/released beroende på fas,
- active PR tas bort från state,
- nästa nya change få ny branch/PR.

Fortsätt inte pusha till merged PR-branch som om den fortfarande var aktiv.

## 28. Closed unmerged PR

Closed/unmerged PR ska behandlas som explicit avbruten eller pausad tills annat beslutas.

System Builder ska inte automatiskt återöppna eller skapa ny PR utan att bedöma användarens intention och repository state.

## 29. Direct-to-default-branch

Default är PR-baserat arbete för icke-triviala changes.

Direkt commit till default branch får användas när:

- användaren uttryckligen begär det,
- repository policy tillåter det,
- risken är låg,
- ingen PR-review krävs.

## 30. Branch protection

Om branch protection kräver PR/review/checks ska System Builder följa den.

Den ska inte försöka kringgå repository controls.

## 31. GitHub permissions

Använd minsta nödvändiga GitHub-behörighet.

System Builder ska inte:

- ändra repository settings utan behov,
- bredda token permissions,
- force-pusha utan uttrycklig och säker anledning,
- skriva secrets i commits/PR.

## 32. Force push

Undvik force push som default.

Tillåt endast när:

- repository workflow kräver rebase/rewritten history,
- work branch är kontrollerad,
- ingen annans arbete riskerar att förloras,
- användaren/policy stödjer det.

## 33. Commit message quality

Commit ska vara:

- kort,
- handlingsorienterad,
- kopplad till steg/scope.

Exempel:

```text
DEV-021: add GitHub mode contract
```

Undvik generiska:

```text
updates
fix stuff
changes
```

## 34. PR title

PR-titel ska beskriva work series, inte senaste mekaniska delsteget.

Exempel:

```text
CR-014: Add repository visibility selection
```

snarare än:

```text
DEV-004 update UI selector
```

## 35. PR status summary

Efter varje steg kan PR-beskrivningen uppdateras med:

```text
Completed:
- DEV-003
- DEV-004

Current:
- none

Next:
- DEV-005

Verification:
- API tests pass
- frontend build pass
```

Repository work status är fortfarande canonical machine state.

## 36. Issues

GitHub issue kan användas som input/context om användaren anger det eller repository workflow använder issues.

Issue ska inte automatiskt bli source of truth framför canonical spec/state.

## 37. Releases

GitHub Release hör till RELEASE-läge.

Work PR ska inte betraktas som release bara för att den är merge-ready.

## 38. Tags

Release tag ska representera verifierad release, inte varje development step.

## 39. Repository hygiene

GitHub-läge ska också kontrollera:

- `.gitignore`,
- generated files,
- committed secrets,
- stale artifacts,
- CI workflow health.

Detaljer formaliseras i nästa hygiene-/CI-steg.

## 40. No GitHub access fallback

Om GitHub-verktyg inte är tillgängliga ska System Builder inte låtsas ha pushat/öppnat PR.

Den får:

- arbeta i ZIP-läge,
- producera patch/project ZIP,
- dokumentera avsedd branch/PR-plan.

## 41. User-supplied PR

Om användaren anger en specifik PR ska System Builder använda den som primär kandidat för aktiv work series, efter att ha verifierat att den matchar repository och scope.

## 42. Multiple candidate PRs

Om flera öppna PRs verkar matcha samma work series:

- analysera branch, title, state och commits,
- välj inte godtyckligt,
- om det inte går att avgöra säkert kan detta bli en genuin blockerande fråga.

## 43. GitHub mode anti-patterns

Undvik:

- ny PR per DEV-step,
- ny branch trots aktiv work series,
- commit före required verification,
- push utan att läsa senaste remote,
- ignorera review/CI,
- force push som default,
- merge utan release/readiness när sådan krävs,
- hålla aktiv PR endast i chat memory.

## 44. Exit-kriterier för SB-21

SB-21 är klart när:

- repository discovery definierats,
- branch/PR/work-series-regler definierats,
- commit strategy definierats,
- state/resume definierats,
- CI/review/drift definierats,
- PR reuse/merge/close-regler definierats,
- permissions/force-push-regler definierats,
- one-step GitHub loop definierats,
- fallback utan GitHub access definierats.
