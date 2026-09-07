# System Builder – GitHub Release build

Git-taggen är source of truth för releaseversionen.

För `v1.0.0` byggs:
- `system-builder-chat-1.0.0.zip`
- `system-builder-custom-gpt-1.0.0.zip`
- `SHA256SUMS.txt`
- `release-metadata.yaml`

Release-builden kör först hela projekt-CI:n, bygger sedan båda distributionerna färskt, validerar dem, kör instruction-adherence och runtime parity och publicerar först därefter.

`.github/workflows/release.yml` triggas av tagg `v*` eller manuell workflow_dispatch med explicit tagg.

Vanlig PR-CI har `contents: read`. Endast release-workflowen har `contents: write`.

Om GitHub Release redan finns används `gh release upload --clobber`; annars skapas releasen med genererade release notes.

En saknad eller ogiltig tagg blockerar release. Versionsnumret får inte tas från ett hårdkodat dev-värde.
