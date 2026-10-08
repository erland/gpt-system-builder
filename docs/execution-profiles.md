# Capability-aware execution profiles

## Syfte

Execution profiles översätter ett validerat capability-discovery snapshot till ett deterministiskt val av exekveringsväg.

Discovery svarar på **vad som finns**. Routing svarar på **vilken exekveringsväg som ska användas**. Profilerna får inte själva duplicera specialistfunktionalitet från Agent Workspace, PWA Preview eller Browser Screenshot.

## Profiler

### `github_first`

Använd när GitHub är canonical source mode och repository read/write samt nödvändiga verifieringsmöjligheter redan kan uppfyllas utan extern execution backend.

Ansvar:

- repositoryt är source of truth,
- branch/commit/PR/CI används som execution state,
- lokal eller repository-baserad verifiering används enligt projektets kontrakt,
- befintlig eller säkert genererbar GitHub Actions ska föredras framför Agent Workspace när den kan utföra required verifiering,
- Agent Workspace får inte köras parallellt enbart för redundant verifiering.

### `hybrid_github_external_execution`

Använd när GitHub är source of truth men code execution behöver en separat tillgänglig execution backend.

Typiskt:

- GitHub read/write finns,
- GitHub Actions/repository CI kan inte uppfylla required verifiering eller ett explicit workflowbehov motiverar extern execution,
- lokal code execution saknas eller är otillräcklig,
- `companion.agent_workspace` finns.

Att Agent Workspace är installerad är inte tillräckligt skäl. När GitHub Actions kan göra jobbet ska `github_first` behållas för att undvika onödiga Agent Workspace-minuter.

GitHub äger source/commit/PR-state. Execution backend får verifiera/builda men får inte bli ny repository authority.

### `agent_workspace`

Använd för ZIP/workspace-baserat arbete när Agent Workspace finns och är den lämpligaste execution backenden.

Profilen betyder bara att execution ska delegeras dit. Detaljer om workspace lifecycle, upload, build/verify och destroy definieras i SB-72.

### `zip_local`

Använd när ZIP/workspace-läge har tillräckliga lokala capabilities:

- filesystem read/write,
- code execution,
- persistent state,
- project packaging när ZIP ska levereras.

### `degraded_manual`

Använd endast när automatiserad preferred path saknas men ett explicit säkert fallback finns. Profilen får aldrig förvandla saknad required capability till PASS.

Exempel:

- GitHub write saknas men patch/ZIP kan levereras,
- lokal execution saknas men verifiering kan lämnas explicit pending/deferred enligt befintliga riskregler.

## Routingprioritet

Routing är deterministisk och sker efter capability discovery.

1. Om en required capability är `blocked` utan explicit safe fallback → routing status `blocked`, ingen execution profile.
2. GitHub source mode + repository read/write + direkt tillräcklig execution/verification → `github_first`.
3. GitHub source mode + repository read/write + Agent Workspace tillgängligt när extern execution behövs → `hybrid_github_external_execution`.
4. ZIP/workspace + Agent Workspace tillgängligt när lokal execution saknas/är otillräcklig → `agent_workspace`.
5. ZIP/workspace + lokala required capabilities → `zip_local`.
6. Om preferred path inte finns men ett uttryckligt fallback kan fullfölja aktuell operation ärligt → `degraded_manual`.
7. Annars → `blocked`.

Vid flera möjliga profiler ska den enklaste profil som uppfyller operationens required capabilities väljas. Companion-plugin får inte väljas bara för att den finns.

## Companion capabilities

- Agent Workspace påverkar execution-routing.
- PWA Preview och Browser Screenshot påverkar normalt senare preview/visual-verification actions, inte kärnprofilen för source mutation.
- Saknad PWA Preview eller Browser Screenshot får därför inte ändra en i övrigt fungerande `github_first` eller `zip_local` profil till blocked.

## Maskinläsbart beslut

Schema: `schemas/execution-profile.schema.json`.

Exempel: `examples/execution-profile.example.yaml`.

Beslutet ska innehålla:

- discovery source/context,
- vald profil eller null,
- status `selected`, `degraded` eller `blocked`,
- deterministiska skäl,
- vilka capabilities som motiverade valet,
- fallback om relevant.

## Authority

Execution profile är runtime-beslut. Den ändrar inte source-of-truth-regler:

- GitHub source mode → repositoryt förblir authority.
- ZIP/workspace → aktuellt workspace/project package förblir authority.
- Companion execution backend är aldrig project-state authority om inte canonical source mode uttryckligen säger det.
