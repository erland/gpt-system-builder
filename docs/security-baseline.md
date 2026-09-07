# System Builder – Säkerhetsbaslinje

## 1. Syfte

System Builder ska säkerställa att grundläggande säkerhetsfrågor beaktas i alla relevanta projekt utan att varje projekt automatiskt behandlas som en full säkerhetsrevision.

Baslinjen ska:

- fånga vanliga och kostsamma säkerhetsmissar tidigt,
- påverka krav, arkitektur, implementation, test och deployment,
- vara proportionerlig mot risk,
- kunna höja projektets kontrollnivå,
- identifiera när specialistgranskning krävs.

## 2. Grundprincip

> Secure by default där det är praktiskt, explicit riskbedömning där det inte är det.

System Builder ska inte anta att "säkerhet hanteras senare".

## 3. Omfattning

Baslinjen täcker minst när relevant:

- authentication,
- authorization,
- input validation,
- output handling,
- secrets,
- sensitive data,
- storage,
- transport security,
- dependency risk,
- logging,
- audit,
- file handling,
- external integrations,
- database access,
- deployment defaults,
- configuration,
- backups,
- error handling.

## 4. Riskproportionalitet

### Small / låg risk

Minst:
- inga hardcoded secrets,
- input validation,
- minsta nödvändiga behörighet,
- säker dependency-baseline,
- TLS via målplattform när publikt exponerad,
- loggar utan secrets,
- säkra defaultvärden.

### Medium

Utöver ovan:
- tydligare authz-modell,
- security-relevanta testfall,
- dependency scanning,
- trust boundaries i arkitekturen,
- explicit secrets/configuration model,
- deployment/security checks.

### Large / high risk

Kan kräva:
- threat modelling,
- specialist security review,
- SAST/DAST,
- penetration testing,
- formell secrets management,
- audit controls,
- regulatoriska krav,
- incident/restore-planer,
- hårdare release gates.

## 5. Authentication

När autentisering behövs ska System Builder definiera:

- vem som autentiseras,
- vilken identitetskälla som används,
- sessions-/tokenmodell på hög nivå,
- logout/expiry,
- hur credentials/secrets skyddas.

System Builder ska normalt föredra etablerad identitetsleverantör/protokoll framför egen lösenordshantering.

## 6. Authorization

Authorization ska uttryckas som verksamhets-/systemregel, inte bara UI-hide/show.

Kontroll ska ske server-side när skyddad data eller operation finns.

Princip:

> UI-begränsning är UX. Backend enforcement är säkerhet.

Beskriv när relevant:
- roles,
- ownership,
- tenant/domain boundary,
- privileged operations,
- default deny/allow-princip.

## 7. Least privilege

Komponenter, tokens och service accounts ska få minsta rimliga rättigheter.

Exempel:
- GitHub token med begränsad scope,
- DB-user utan adminbehörighet,
- container utan root där praktiskt,
- secrets bara till komponenter som behöver dem.

## 8. Input validation

All extern input ska behandlas som opålitlig.

Exempel:
- HTTP payload,
- query params,
- headers,
- filenames,
- ZIP entries,
- webhook payloads,
- external API responses när de påverkar säkerhetskritisk logik.

Validera:
- format,
- längd,
- typ,
- allowed values,
- size limits,
- path handling,
- encoding där relevant.

## 9. File handling

För uppladdade filer:

- begränsa storlek,
- validera format när möjligt,
- använd säkra temporära paths,
- förhindra path traversal,
- förhindra absoluta paths,
- undvik exekvering av användarinnehåll,
- cleanup temporära filer,
- separera persistent och ephemeral storage.

Arkivformat kräver särskild validering före extraktion.

## 10. Secrets

Secrets får inte:

- hårdkodas i repo,
- checkas in i `.env`,
- skrivas i logg,
- bäddas in i container image,
- exponeras i frontend bundle.

Secrets ska normalt tillföras via:
- environment variables,
- platform secret store,
- external secret manager.

`.env.example` får innehålla nyckelnamn men inte verkliga värden.

## 11. Sensitive data

System Builder ska identifiera känslig data när projektunderlag visar att sådan finns.

Bedöm:
- collection minimization,
- storage,
- retention,
- access,
- logging,
- backups,
- deletion,
- export.

System Builder ska inte fabricera juridiska klassificeringar.

## 12. Encryption / transport

Publik eller känslig trafik ska normalt använda TLS.

På plattformar som Coolify ska TLS normalt hanteras av plattformen.

System Builder ska undvika dubbel TLS-terminering utan anledning.

Encryption at rest ska bedömas utifrån risk och plattform; den ska inte påstås vara uppfylld utan faktisk plattforms-/lagringsgrund.

## 13. Database security

När databas används:

- credentials via secrets/configuration,
- minsta privileges,
- parametriserade queries/ORM,
- migrations kontrolleras,
- inga default/admin credentials,
- backup/restore-responsibility tydlig,
- network exposure begränsas.

Extern PostgreSQL ska inte exponeras publikt om det inte finns ett motiverat behov.

## 14. External integrations

Bedöm:
- auth scopes,
- webhook validation,
- timeout,
- retries,
- idempotency,
- rate limits,
- untrusted responses,
- secret storage,
- error leakage.

## 15. Dependency security

System Builder ska:

- använda aktivt underhållna dependencies där möjligt,
- undvika onödiga dependencies,
- låsa versioner enligt stackens normala modell,
- använda dependency scanning när projektet/CI motiverar det,
- inte uppgradera stora dependency-set opportunistiskt i orelaterade steg.

Kända kritiska vulnerabilities kan blockera release.

## 16. Logging

Loggar ska vara användbara utan att läcka:

- passwords,
- tokens,
- API keys,
- session secrets,
- känsliga payloads,
- persondata i onödan.

Bra loggar inkluderar:
- operation/correlation ID,
- outcome,
- relevant system context.

## 17. Error handling

Fel till användare/API ska inte avslöja:

- stack traces,
- secrets,
- interna credentials,
- onödiga implementation details.

Interna loggar kan ha mer diagnostik men ska fortfarande skydda secrets.

## 18. Audit

Audit trail behövs när projektets risk/krav motiverar det.

Exempel:
- privilegierade admin-operationer,
- ändring av behörighet,
- kritisk dataexport,
- security-relevant configuration.

Audit är inte samma sak som debug logging.

## 19. Secure defaults

Exempel:
- private-by-default när användarens data/repository inte uttryckligen ska vara publikt,
- explicit CORS,
- CSRF-skydd när relevant,
- secure cookies,
- debug mode off i production,
- no default passwords,
- no wildcard privileges,
- health endpoint utan secrets.

## 20. Web security baseline

För webbappar när relevant:

- server-side authz,
- XSS-säker rendering,
- CSRF där cookie-auth kräver det,
- CORS least privilege,
- secure/session cookie-flags,
- security headers där plattformen stödjer det,
- rate limiting för känsliga endpoints när risk motiverar det.

## 21. API security baseline

- authentication där endpoint inte är publik,
- authorization per operation/resource,
- schema/input validation,
- size limits,
- rate/abuse considerations,
- idempotency där dubbel exekvering är farlig,
- safe error responses.

## 22. Container baseline

För containeriserade tjänster:

- minimal base image där praktiskt,
- non-root runtime där möjligt,
- inga secrets i image/layers,
- `.dockerignore`,
- endast nödvändiga ports,
- health checks,
- reproducible build,
- dependency/package scanning när relevant.

## 23. Coolify baseline

Vid Coolify:

- app image innehåller inte PostgreSQL,
- PostgreSQL körs externt/separat,
- TLS och reverse proxy hanteras av plattformen,
- secrets sätts i plattformens environment/secret configuration,
- publicera bara appens nödvändiga endpoint,
- health endpoint konfigureras,
- persistent volume endast om appen verkligen behöver filstorage.

## 24. CI/CD security

- secrets i CI secret store,
- minimala workflow permissions,
- pinning/versionering av actions enligt projektpolicy,
- inga secrets i PR-output/loggar,
- artifacts hanteras med avsedd retention,
- release workflow ska bygga från verifierad commit/tag.

## 25. GitHub baseline

När repository finns på GitHub bör System Builder vid behov stödja:

- `.gitignore`,
- secret scanning/dependency tooling när tillgängligt,
- branch/PR workflow,
- begränsade GitHub token permissions,
- no credentials committed.

## 26. Security verification

Security-relevant krav ska ha explicit verifiering.

Exempel:
- unauthorized user gets denied,
- path traversal ZIP rejected,
- secrets absent from logs,
- container runs non-root,
- protected endpoint requires auth,
- invalid webhook signature rejected.

## 27. Security blocker

Säkerhetsfråga ska blockera relevant implementation/release när:

- authz för känslig operation är oklar,
- credentials måste hårdkodas,
- användarinput kan leda till code/path execution,
- kritisk vulnerability saknar mitigation,
- data riskerar okontrollerad förlust/exponering,
- deployment kräver osäker publik databas,
- central trust boundary är odefinierad.

## 28. Specialistgranskning

System Builder ska rekommendera specialistgranskning när exempelvis:

- systemet hanterar mycket känslig data,
- Internet-exponerad attackyta är stor,
- komplex auth/identity,
- payment/financial controls,
- high-impact admin operations,
- avancerad cryptography,
- regulatorisk säkerhetsnivå,
- kritisk infrastruktur.

System Builder är process owner och baseline-granskare, inte automatiskt ersättare för security specialist.

## 29. Threat model

Threat model behövs när risk motiverar det.

En lätt modell kan täcka:
- assets,
- actors,
- trust boundaries,
- entry points,
- abuse cases,
- mitigations.

Full STRIDE eller motsvarande är inte obligatoriskt för varje system.

## 30. Säkerhetsdokumentation

Security ska primärt integreras i:
- functional spec (security requirements),
- architecture (security model),
- risk/feasibility,
- test strategy,
- configuration,
- operations.

Separat `docs/security.md` skapas bara när komplexiteten motiverar det.

## 31. CHANGE-regel

Vid CHANGE ska System Builder fråga/analysera:

- förändras attackytan?
- tillkommer ny input/integration?
- ändras auth/authz?
- ändras dataägarskap?
- tillkommer secrets?
- ändras deployment/network exposure?
- krävs nya regression/security tests?

## 32. IMPROVE-regel

Teknisk förbättring får inte försämra säkerhetskontroller även om funktionellt beteende är oförändrat.

Security-sensitive refactoring bör ha characterization/regression tests.

## 33. Anti-patterns

Undvik:
- "vi använder HTTPS, alltså är systemet säkert",
- auth endast i frontend,
- secrets i `.env` committed,
- admin DB-user för app,
- wildcard CORS utan behov,
- logging av fulla tokens,
- root container som default utan anledning,
- security review först efter release,
- generisk checklist utan koppling till faktisk systemrisk.

## 34. Security review checklist

Minst när relevant:

- [ ] Authentication defined
- [ ] Authorization enforced server-side
- [ ] Least privilege
- [ ] Input validation
- [ ] File handling safe
- [ ] Secrets externalized
- [ ] Sensitive data identified
- [ ] TLS ownership defined
- [ ] DB access constrained
- [ ] External integrations reviewed
- [ ] Dependencies checked
- [ ] Logs avoid secrets
- [ ] Error responses safe
- [ ] Container defaults safe
- [ ] Deployment exposure reviewed
- [ ] Security tests exist for critical controls

## 35. Exit-kriterier för säkerhetsbaslinjen

Fasen är tillräcklig när:

- security-relevant requirements är synliga,
- trust/auth/authz/input/secrets/deployment är bedömda,
- kritiska security risks är blockerare eller mitigerade,
- verifieringsplan finns,
- specialist review är identifierad när baseline inte räcker.
