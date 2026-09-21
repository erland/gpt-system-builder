# Migrering mot GPT Byggaren 1.4.0

## Syfte

Detta dokument fastställer System Builders fortsatta runtime-mål efter den tidigare planen SB-01–SB-41.

Migreringen ska bevara System Builders canonical domänbeteende: CREATE, CHANGE, IMPROVE, PLAN, REPAIR och RELEASE, inklusive ZIP-/GitHub-läge, persistent projektstate, verifiering, dokumentation och release readiness.

## Gap mot GPT Byggaren 1.4.0

Nuvarande projekt har två runtime-adaptrar:

- Chat ZIP
- Custom GPT

GPT Byggaren 1.4.0 kräver att registrerade peer runtimes bedöms explicit och att aktiverade runtimes härleds från plattformsneutrala behavior-, capability-, artifact-, workspace/state- och tool-kontrakt.

System Builder saknar idag:

- generiskt runtime compatibility-kontrakt,
- explicit capability-/artifact-/workspace-state-/tool-kontrakt,
- Claude Projects-adapter,
- OpenCode-adapter,
- generic runtime parity över fler än Chat ZIP och Custom GPT,
- CI/release-build för fler än två runtimes.

## Runtimebedömning

| Runtime | Bedömning | Aktivera | Motivering |
| --- | --- | --- | --- |
| ChatGPT Chat / Chat ZIP | equivalent | Ja | Befintlig och validerad runtime. |
| ChatGPT Custom | equivalent inom befintligt kontrakt | Ja | Befintlig och validerad runtime; plattformsbegränsningar hanteras redan av kompileringen. |
| Claude Projects | reduced | Ja | Kärnflöden för analys, planering, dokumentation och filbaserat arbete är användbara, men lokal script-/tool-exekvering och GitHub-mutation kan inte antas. Reducerad parity ska vara explicit. |
| OpenCode | equivalent för repo/workspace-arbete | Ja | Passar System Builders Git-, repository-, workspace/state- och lokala tool-flöden. `AGENTS.md` ska vara genererad runtime-entrypoint. |
| OpenAI Plugin v1 | reduced / not recommended | Nej | System Builder är starkt beroende av långlivat workspace/state samt verktygs-/repository-exekvering. Skills-first Plugin v1 täcker inte detta tillräckligt för en full System Builder-runtime. |

## Beslutad målbild

Aktiverade distributionsmål efter migreringen:

1. Chat ZIP
2. Custom GPT
3. Claude Projects
4. OpenCode

OpenAI Plugin ska fortsatt finnas med i compatibility-bedömningen men inte byggas eller publiceras förrän dess runtime kan täcka System Builders kritiska workspace/state- och tool-krav utan dold funktionsförlust.

## Migreringsprinciper

- Canonical instruktion och domänbeteende förblir gemensamma.
- Runtime-specifika filer är genererade adaptrar, inte nya sanningskällor.
- Reducerad parity dokumenteras i stället för att döljas med specialregler.
- CI och release readiness ska omfatta samtliga aktiverade runtimes.
- Releasebygget ska producera alla aktiverade distributioner från samma tagg.
- Den tidigare releasekandidaten 1.0.0-rc.1 bevaras som historiskt resultat men är inte längre slutlig release-målbild efter att migrationsserien startats.

## Nästa tekniska beroende

Innan Claude/OpenCode-adaptrarna implementeras behöver projektet ett plattformsneutralt runtime-kontrakt som explicit beskriver:

- behavior,
- capabilities,
- artifacts,
- workspace/state,
- tools,
- runtime compatibility/parity.

Detta är SB-43.
