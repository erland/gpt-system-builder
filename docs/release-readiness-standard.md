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
