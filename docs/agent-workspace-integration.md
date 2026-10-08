# Agent Workspace integration

## Syfte

Agent Workspace är en **optional execution backend** för System Builder. Den ska användas när den tillför en capability som aktuell host eller repository-CI inte redan erbjuder tillräckligt bra.

Den är aldrig standardval bara för att pluginen finns installerad.

## Kostnads- och routingprincip

I GitHub source mode gäller:

1. Om befintlig eller säkert genererbar GitHub Actions kan utföra required build/test/lint/typecheck/browser-verifiering ska `github_first` användas.
2. Agent Workspace ska inte användas parallellt för samma verifiering enbart för redundans.
3. `hybrid_github_external_execution` väljs endast när GitHub Actions inte kan ge required capability/evidens, eller när ett explicit workflowbehov motiverar den extra execution-kostnaden.
4. GitHub repository/branch/PR/CI förblir source och state authority även när Agent Workspace används.
5. Agent Workspace-resultat är execution evidence, inte repository state.

Exempel på legitima skäl att använda Agent Workspace i GitHub mode:

- required verifiering kan inte köras i repository-CI,
- en isolerad interaktiv execution behövs innan commit/PR,
- en build artifact måste produceras omedelbart för vidare handoff i samma workflow,
- CI-konfiguration saknas och det vore oproportionerligt att skapa/ändra workflow endast för en tillfällig verifiering.

## ZIP/workspace mode

I ZIP eller fristående workspace kan `agent_workspace` väljas när:

- lokal code execution saknas eller är otillräcklig,
- projektet är kompatibelt med Agent Workspace,
- required verifiering kan köras där,
- kostnaden är motiverad jämfört med ett billigare lokalt alternativ.

## Lifecycle

När Agent Workspace används ska System Builder följa denna lifecycle:

1. **create** – skapa kortlivad workspace med minsta praktiska lifetime,
2. **upload** – överför relevant project source som ZIP eller via stödd URL-handoff,
3. **verify/build** – kör endast den verifiering/build som behövs för aktuellt steg,
4. **collect** – hämta metadata/artifact-länk endast när ett senare steg faktiskt behöver artifacten,
5. **destroy** – destruera workspace i samma körning även efter fel när destroy är möjligt.

Workspace får inte lämnas aktiv utan skäl.

## Supported execution semantics

System Builder får mappa Agent Workspace till:

- workspace creation,
- project ZIP upload,
- project verification,
- project build,
- artifact metadata/download-link handoff,
- workspace destruction.

Exakta host tool-namn är runtime-specifika. Canonical System Builder ska beskriva capability semantics, inte hårdkoda MCP-implementationen som enda möjliga backend.

## Verification evidence

Ett Agent Workspace-resultat får registreras som verifieringsevidens endast när operationen faktiskt kördes.

Registrera minst:

- execution backend: `agent_workspace`,
- source revision/checksum som verifierades,
- verifieringstyp,
- resultat,
- eventuella artifact identifiers,
- workspace cleanup-resultat.

Ett pluginfel, timeout eller otillgänglig backend är **inte** project failure om projektet inte faktiskt kördes och misslyckades. Klassificera det som environment/backend-limited och använd annan säker verifieringsväg när sådan finns.

## Build artifacts

Använd build-artifact endast när nästa workflowsteg behöver den.

Exempel:

- direkt handoff till PWA Preview,
- nedladdningsbar release/test artifact,
- verifiering av exakt byggd output.

Bygg inte artifact om vanlig `project_verify` räcker.

## Cleanup

Destroy är obligatoriskt best effort:

- kör efter lyckad verifiering,
- kör efter misslyckad verifiering,
- kör efter build/artifact-handoff,
- rapportera cleanup failure separat från projektets build/test-resultat.

Cleanup failure gör inte automatiskt projektverifieringen ogiltig, men ska registreras som operational warning.

## Fallback

Om Agent Workspace saknas eller inte svarar:

- GitHub mode → använd GitHub Actions/repository CI när det kan uppfylla required checks,
- ZIP/workspace → använd lokal execution när tillgänglig,
- annars använd befintlig deferred/environment-limited policy,
- rapportera aldrig en ej körd Agent Workspace-kontroll som PASS.
