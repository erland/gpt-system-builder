#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PYTHON="${PYTHON:-python3}"
DIST_DIR="${DIST_DIR:-dist-ci}"
CHAT_ZIP="$DIST_DIR/system-builder-chat-ci.zip"
CUSTOM_ZIP="$DIST_DIR/system-builder-custom-gpt-ci.zip"

rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"

echo "== State/schema validators =="
$PYTHON scripts/validate_state_contracts.py
$PYTHON scripts/validate_traceability.py --file .system-builder/traceability.yaml --schema schemas/traceability.schema.json
$PYTHON scripts/validate_deployment_profile.py --file .system-builder/deployment-profile.yaml --schema schemas/deployment-profile.schema.json

echo "== Canonical validators =="
$PYTHON scripts/validate_functional_spec.py examples/functional-specification.example.md
$PYTHON scripts/validate_architecture_doc.py examples/architecture.example.md
$PYTHON scripts/validate_decision_records.py adr examples/ADR-001-modular-monolith.example.md
$PYTHON scripts/validate_decision_records.py product examples/product-decisions.example.md
$PYTHON scripts/validate_development_plan.py examples/development-plan.example.md
$PYTHON scripts/validate_risk_feasibility.py examples/risk-feasibility.example.md
$PYTHON scripts/validate_test_strategy.py examples/test-strategy.example.md
$PYTHON scripts/validate_security_review.py examples/security-review.example.md
$PYTHON scripts/validate_create_intake.py examples/create-intake.example.md
$PYTHON scripts/validate_change_artifacts.py request examples/CR-001-request.example.md
$PYTHON scripts/validate_change_artifacts.py impact examples/CR-001-impact-analysis.example.md
$PYTHON scripts/validate_improve_intake.py examples/improve-intake.example.md
$PYTHON scripts/validate_next_step_assessment.py examples/next-step-assessment.example.md
$PYTHON scripts/validate_github_run_assessment.py examples/github-run-assessment.example.md
$PYTHON scripts/validate_deployment_packaging_plan.py examples/deployment-packaging-plan.example.md
$PYTHON scripts/validate_docker_baseline.py examples/Dockerfile.example --dockerignore examples/dockerignore.example
$PYTHON scripts/validate_coolify_profile.py examples/coolify-deployment-profile.example.md
$PYTHON scripts/validate_operational_docs.py configuration examples/configuration.example.md
$PYTHON scripts/validate_operational_docs.py installation examples/installation.example.md
$PYTHON scripts/validate_operational_docs.py operations examples/operations.example.md
$PYTHON scripts/validate_release_readiness.py examples/release-readiness.example.md
$PYTHON scripts/validate_knowledge_architecture.py .
$PYTHON scripts/validate_runtime_instruction.py .
$PYTHON scripts/validate_instruction_evals.py evals/instruction-adherence.yaml

echo "== Fresh distribution build =="
$PYTHON scripts/build_chat_runtime_zip.py --project-root . --output "$CHAT_ZIP"
$PYTHON scripts/build_custom_gpt_distribution.py --source-dir runtime/custom-gpt-source --output "$CUSTOM_ZIP"

echo "== Distribution validation =="
$PYTHON scripts/validate_chat_runtime_zip.py "$CHAT_ZIP"
$PYTHON scripts/validate_custom_gpt_distribution.py "$CUSTOM_ZIP"

echo "== Instruction adherence and parity =="
$PYTHON scripts/run_static_instruction_evals.py --requirements evals/static-contract-requirements.yaml --distribution chat_zip --artifact "$CHAT_ZIP"
$PYTHON scripts/run_static_instruction_evals.py --requirements evals/static-contract-requirements.yaml --distribution custom_gpt --artifact "$CUSTOM_ZIP"
$PYTHON scripts/validate_runtime_parity.py --contract evals/runtime-parity-contract.yaml --chat "$CHAT_ZIP" --custom "$CUSTOM_ZIP"

echo "== E2E regression =="
$PYTHON scripts/run_e2e_small_create_eval.py --scenario-root evals/e2e/small-create
$PYTHON scripts/run_e2e_existing_change_eval.py --scenario-root evals/e2e/existing-system-change
$PYTHON scripts/run_e2e_docker_coolify_eval.py --scenario-root evals/e2e/docker-coolify

echo "== Clean generated CI artifacts before hygiene =="
rm -rf "$DIST_DIR"
find evals -type d -name __pycache__ -prune -exec rm -rf {} +
find evals -type f -name '*.pyc' -delete

echo "== Repository hygiene =="
$PYTHON scripts/scan_repository_hygiene.py .

echo "PASS: System Builder project CI"
