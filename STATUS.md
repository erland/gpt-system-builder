# System Builder – Status

## Övergripande status
**PASS – runtime migration in progress**

## Senast slutförda steg
### SB-45 – Implementera OpenCode-runtime

OpenCode är nu en byggbar peer-runtime härledd från samma canonical System Builder-kontrakt.

Distributionen innehåller:

- root `AGENTS.md` genererad från canonical runtime-instruktion,
- `.opencode/runtime-contract.json` som adapter-snapshot,
- `.opencode/tool-mapping.json` som mappar canonical tool capabilities till OpenCode,
- `opencode.json` med approval-policy,
- relevant Knowledge,
- tydlig separation mellan runtime-workspace och målprojekt via `projectRoot`.

Inga custom script-tools genereras eftersom canonical tool-kontraktet inte deklarerar några konkreta script-tools. Detta undviker att hela `scripts/` implicit exponeras.

## Verifiering

- SB-44 CI: PASS
- OpenCode builder införd
- OpenCode validator införd
- ordinarie CI bygger och validerar OpenCode-ZIP
- `CLAUDE.md` förbjuds i OpenCode-distributionen
- muterande edit- och shell-operationer kräver approval
- tool mapping måste exakt motsvara deklarerad canonical tool-mängd
- projectRoot/workspace-separation valideras

## Blockerare
Inga.

## Nästa steg
**SB-46 – Modernisera build, lint och project hygiene.**
