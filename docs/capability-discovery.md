# Capability discovery

## Syfte

System Builder ska upptäcka vilka execution capabilities som faktiskt finns i den aktuella host/runtime-körningen innan en exekveringsväg väljs.

Discovery beskriver **vad som finns nu**. Den väljer inte execution profile; det sker i SB-71.

## Principer

1. Utgå från faktisk host/tool availability, inte från antaganden om installerade plugins.
2. Föredra host-advertised capabilities och redan tillgängliga verktyg framför probes.
3. Använd endast lätta, icke-destruktiva probes när availability inte annars kan fastställas.
4. Markera capability som `unknown` när den inte säkert kan avgöras.
5. Rapportera aldrig en capability som `available` utan faktisk evidens.
6. Saknad optional capability blockerar inte arbetet.
7. Saknad required capability blockerar operationen, eller degraderar endast när ett uttryckligt säkert fallback finns.
8. Discovery-resultatet är runtime-evidens, inte långlivad project source of truth. Det ska uppdateras per körning eller när host/tool availability ändras.

## Canonical capability IDs

Basförmågor:

- `repository.read`
- `repository.write`
- `filesystem.read`
- `filesystem.write`
- `code_execution`
- `persistent_state`
- `project_packaging`

Optional companion capabilities:

- `companion.agent_workspace`
- `companion.pwa_preview`
- `companion.browser_screenshot`

Companion capabilities ska vara optional i discovery-modellen. Ett senare konkret steg kan göra en capability required för just den operationen, men frånvaro av en companion plugin får inte göra System Builder oanvändbar när ett canonical fallback-flöde finns.

## Availability states

Varje capability får exakt ett availability-värde:

- `available` – faktisk host/tool-evidens finns.
- `unavailable` – hosten visar eller en säker probe visar att capability saknas.
- `unknown` – kan inte avgöras säkert.
- `not_applicable` – capability behövs inte i aktuell source/operation context.

## Requirement per operation

Discovery snapshot skiljer availability från requirement:

- `required`
- `recommended`
- `optional`
- `not_required`

Det gör att samma host capability kan vara optional i ett steg men required i ett annat.

## Outcome

Efter discovery klassificeras varje capability som:

- `satisfied` – requirement kan uppfyllas,
- `degraded` – capability saknas men ett explicit fallback finns,
- `blocked` – required capability saknas/är unknown utan säkert fallback,
- `ignored` – not required/not applicable.

Discovery får inte välja GitHub-first, Agent Workspace, ZIP/local eller annan execution profile. Den producerar bara evidensen som SB-71 senare använder för routing.

## Maskinläsbart kontrakt

Schema: `schemas/capability-discovery.schema.json`.

Exempel: `examples/capability-discovery.example.yaml`.

Snapshot kan hållas i hostens runtime-state eller som tillfällig strukturerad evidens. Om den serialiseras i projektet ska den betraktas som runtime snapshot och uppdateras före routing; den får inte övertrumfa faktisk tool availability.

## Detektionsordning

För varje relevant capability:

1. läs hostens deklarerade tools/capabilities,
2. återanvänd redan bekräftad capability från den aktuella körningen,
3. gör en säker, icke-muterande probe om det behövs,
4. annars `unknown`.

Exempel:

- en tillgänglig GitHub connector med read/write actions kan ge `repository.read/write = available`,
- en exekveringsruntime kan ge `code_execution = available`,
- installerat Agent Workspace med callable tools kan ge `companion.agent_workspace = available`,
- frånvaro av PWA Preview ska ge `unavailable` eller `unknown`, inte ett blockerande fel om preview inte är required.

## Frågor till användaren

Fråga inte användaren om teknisk tool availability som hosten kan avgöra själv. Fråga endast när en verklig produkt-/säkerhets-/affärsfråga påverkar vilken capability som bör krävas.
