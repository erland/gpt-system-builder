#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
PYTHON="${PYTHON:-python3}"
VERSION="${1:-1.4.1}"
echo '== Canonical migration registry =='
"$PYTHON" scripts/validate_distribution_registry.py
"$PYTHON" scripts/validate_runtime_contract.py
"$PYTHON" scripts/validate_runtime_instruction.py .
"$PYTHON" scripts/validate_capability_discovery.py
"$PYTHON" scripts/validate_state_contracts.py
"$PYTHON" scripts/validate_improve_intake.py examples/improve-intake.example.md
"$PYTHON" scripts/run_e2e_small_create_eval.py --scenario-root evals/e2e/small-create
"$PYTHON" scripts/run_e2e_existing_change_eval.py --scenario-root evals/e2e/existing-system-change
if [[ "${RUN_DOCKER_SCENARIO:-0}" == "1" ]]; then
  "$PYTHON" scripts/run_e2e_docker_coolify_eval.py --scenario-root evals/e2e/docker-coolify
fi
"$PYTHON" scripts/build_distributions.py --version "$VERSION"
"$PYTHON" scripts/validate_distributions.py

"$PYTHON" scripts/validate_distribution_registry.py
printf 'PASS: migrated CI pipeline\n'
