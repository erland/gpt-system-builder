# System Builder – Status

## Övergripande status
**CHANGE IN PROGRESS – SB-62 complete, SB-63 next**

## Senast slutförda steg
### SB-62 – Release-tag som canonical versionskälla

SB-62 är verifierad med full required CI för revision `9133dba6e8fa5e5bedb1c07507f25ec3ea9ffa00` och är completed.

System Builder har nu en generell releaseversioneringsregel:

- när releaseartefakter byggs från en Git-tag är taggen normalt canonical versionskälla,
- artifactnamn, image tags och release metadata härleds från samma releaseversion,
- hårdkodade parallella releaseversioner ska undvikas,
- om `package.json`, `pom.xml`, Gradle metadata eller annan ecosystemfil också innehåller version ska versionsägarskap vara explicit,
- antingen äger taggen versionen och ecosystemfilen synkas/valideras, eller så äger ecosystemfilen versionen och taggen valideras mot den,
- mismatch mellan tagg, artifacts, release metadata och ecosystemversion är release-blocking.

Custom GPT-instruktionen är fortsatt inom 8 000-teckensgränsen.

## Aktiv förändringsserie

Återstående:

- **SB-63** – regression coverage för README och releaseversionering.

## Nästa åtgärd

Implementera SB-63 på samma PR.
