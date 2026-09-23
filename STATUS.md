# System Builder – Status

## Övergripande status
**SB-50 IN PROGRESS – completion transition awaiting full CI**

## Aktuellt steg
### SB-50 – Separera verifierad implementation från completion transition

Implementationen är gjord på work branch. Steget är avsiktligt inte markerat completed ännu: full required CI måste först PASS för implementation revisionen.

Förändringen inför:

- verifierad source revision som optional completion evidence,
- GitHub-flödet implementation commit → full CI → completion-only state commit → lightweight completion check,
- ZIP-flödet full verifiering → completion transition → lightweight state validation → package,
- resumable checkpoint när ZIP-läge saknar en extern required gate,
- fallback till full verifiering om revision/evidence inte kan härledas säkert,
- bakåtkompatibilitet med projekt skapade av äldre System Builder-versioner utan obligatorisk förhandsmigrering.

## Release candidate

Nuvarande version är fortsatt `1.0.0-rc.2`. SB-50 är en efterföljande förändring och releasebeslut tas först efter grön full CI.

## Nästa åtgärd

Kör full projekt-CI för implementation revisionen. Vid PASS får SB-50 klarmarkeras genom en ren completion/status-ändring.
