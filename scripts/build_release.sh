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
CHAT_ZIP="$ARTIFACT_DIR/system-builder-chat-$VERSION.zip"
CUSTOM_ZIP="$ARTIFACT_DIR/system-builder-custom-gpt-$VERSION.zip"
CHECKSUMS="$ARTIFACT_DIR/SHA256SUMS.txt"

rm -rf "$ARTIFACT_DIR"
mkdir -p "$ARTIFACT_DIR"

echo "== Pre-release validation =="
bash scripts/ci-project.sh

echo "== Build release distributions =="
$PYTHON scripts/build_chat_runtime_zip.py --project-root . --output "$CHAT_ZIP"
$PYTHON scripts/build_custom_gpt_distribution.py --source-dir runtime/custom-gpt-source --output "$CUSTOM_ZIP"

echo "== Validate release distributions =="
$PYTHON scripts/validate_chat_runtime_zip.py "$CHAT_ZIP"
$PYTHON scripts/validate_custom_gpt_distribution.py "$CUSTOM_ZIP"
$PYTHON scripts/run_static_instruction_evals.py --requirements evals/static-contract-requirements.yaml --distribution chat_zip --artifact "$CHAT_ZIP"
$PYTHON scripts/run_static_instruction_evals.py --requirements evals/static-contract-requirements.yaml --distribution custom_gpt --artifact "$CUSTOM_ZIP"
$PYTHON scripts/validate_runtime_parity.py --contract evals/runtime-parity-contract.yaml --chat "$CHAT_ZIP" --custom "$CUSTOM_ZIP"

echo "== Write checksums =="
(
  cd "$ARTIFACT_DIR"
  sha256sum "$(basename "$CHAT_ZIP")" "$(basename "$CUSTOM_ZIP")" > "$(basename "$CHECKSUMS")"
)

cat > "$ARTIFACT_DIR/release-metadata.yaml" <<EOF
name: System Builder
version: "$VERSION"
tag: "$TAG"
artifacts:
  - "$(basename "$CHAT_ZIP")"
  - "$(basename "$CUSTOM_ZIP")"
checksums: "$(basename "$CHECKSUMS")"
source_of_version: release_tag
EOF

echo "PASS: release artifacts built for $TAG"
