# System Builder – Status

## Övergripande status
**PASS – runtime migration in progress**

## Senast slutförda steg
### SB-48 – Uppdatera CI, release och dokumentation

Releaseflödet är nu uppdaterat för hela GPT Byggaren 1.4-runtime-målbilden.

GitHub Release bygger och publicerar:

- Chat ZIP
- Custom GPT
- Claude Projects
- OpenCode
- SHA256 checksums
- release metadata
- distribution build manifest

Releasebygget använder samma distributionsregister som ordinarie CI och kör static instruction adherence samt runtime parity för alla fyra runtimes.

README beskriver nu runtime-målbild, lokal build/validation och samtliga release-assets.

## Verifiering

- SB-47 repair CI: PASS
- release bygger alla fyra runtime-distributioner via gemensamt registry
- alla fyra distributioner valideras före publicering
- instruction adherence körs för alla fyra
- runtime parity körs med Chat, Custom GPT, Claude Projects och OpenCode
- checksummor och release metadata härleds från build manifest
- release-validatorn kräver samtliga fyra runtime-assets

## Blockerare
Inga.

## Nästa steg
**SB-49 – Full regression och ny release candidate.**
