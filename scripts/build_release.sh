#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PYTHON="${PYTHON:-python3}"
TAG="${RELEASE_TAG:-${1:-}}"

if [[ -z "$TAG" ]]; then
  echo "ERROR: release tag required via RELEASE_TAG or first argument"
  exit 2
fi

if [[ ! "$TAG" =~ ^v[0-9]+\.[0-9]+\.[0-9]+([.-][0-9A-Za-z.-]+)?$ ]]; then
  echo "ERROR: release tag must look like v1.2.3 or v1.2.3-rc.1"
  exit 2
fi

VERSION="${TAG#v}"
ARTIFACT_DIR="${ARTIFACT_DIR:-release-artifacts}"
BUILD_MANIFEST="$ARTIFACT_DIR/distribution-build-manifest.json"
CHECKSUMS="$ARTIFACT_DIR/SHA256SUMS.txt"
METADATA="$ARTIFACT_DIR/release-metadata.yaml"

rm -rf "$ARTIFACT_DIR"
mkdir -p "$ARTIFACT_DIR"

echo "== Pre-release validation =="
bash scripts/ci-project.sh

echo "== Build release distributions =="
$PYTHON scripts/build_all_distributions.py --output-dir "$ARTIFACT_DIR" --version "$VERSION"

echo "== Validate release distributions =="
$PYTHON scripts/validate_all_distributions.py --manifest "$BUILD_MANIFEST"

CHAT_ZIP="$ARTIFACT_DIR/system-builder-chat-$VERSION.zip"
CUSTOM_ZIP="$ARTIFACT_DIR/system-builder-custom-gpt-$VERSION.zip"
CLAUDE_ZIP="$ARTIFACT_DIR/system-builder-claude-projects-$VERSION.zip"
OPENCODE_ZIP="$ARTIFACT_DIR/system-builder-opencode-$VERSION.zip"

echo "== Runtime adherence and parity =="
$PYTHON scripts/run_static_instruction_evals.py --requirements evals/static-contract-requirements.yaml --distribution chat_zip --artifact "$CHAT_ZIP"
$PYTHON scripts/run_static_instruction_evals.py --requirements evals/static-contract-requirements.yaml --distribution custom_gpt --artifact "$CUSTOM_ZIP"
$PYTHON scripts/run_static_instruction_evals.py --requirements evals/static-contract-requirements.yaml --distribution claude_projects --artifact "$CLAUDE_ZIP"
$PYTHON scripts/run_static_instruction_evals.py --requirements evals/static-contract-requirements.yaml --distribution opencode --artifact "$OPENCODE_ZIP"
$PYTHON scripts/validate_runtime_parity.py --contract evals/runtime-parity-contract.yaml --chat "$CHAT_ZIP" --custom "$CUSTOM_ZIP" --claude "$CLAUDE_ZIP" --opencode "$OPENCODE_ZIP"

echo "== Write checksums and metadata =="
$PYTHON - "$BUILD_MANIFEST" "$CHECKSUMS" "$METADATA" "$TAG" "$VERSION" <<'PY'
from pathlib import Path
import hashlib, json, sys, yaml

manifest_path=Path(sys.argv[1])
checksums_path=Path(sys.argv[2])
metadata_path=Path(sys.argv[3])
tag=sys.argv[4]
version=sys.argv[5]
manifest=json.loads(manifest_path.read_text(encoding="utf-8"))
artifacts=[]
checksum_lines=[]
for runtime,path_text in manifest["artifacts"].items():
    path=Path(path_text)
    if not path.is_absolute():
        path=Path.cwd()/path
    data=path.read_bytes()
    digest=hashlib.sha256(data).hexdigest()
    artifacts.append({"runtime":runtime,"file":path.name,"sha256":digest})
    checksum_lines.append(f"{digest}  {path.name}")
checksums_path.write_text("\n".join(checksum_lines)+"\n",encoding="utf-8")
metadata={
    "name":"System Builder",
    "version":version,
    "tag":tag,
    "artifacts":artifacts,
    "checksums":checksums_path.name,
    "source_of_version":"release_tag",
    "distribution_registry":"runtime/distribution-registry.yaml",
}
metadata_path.write_text(yaml.safe_dump(metadata,sort_keys=False),encoding="utf-8")
PY

echo "PASS: release artifacts built for $TAG"
