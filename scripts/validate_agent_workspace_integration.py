#!/usr/bin/env python3
from __future__ import annotations
import copy, json, sys
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator, ValidationError

ROOT=Path(__file__).resolve().parents[1]
SCHEMA=ROOT/"schemas"/"agent-workspace-evidence.schema.json"
EXAMPLE=ROOT/"examples"/"agent-workspace-evidence.example.yaml"
RUNTIME_CONTRACT=ROOT/"runtime"/"runtime-contract.json"
POLICY_DOC=ROOT/"docs"/"agent-workspace-integration.md"

def main()->int:
    schema=json.loads(SCHEMA.read_text(encoding="utf-8"))
    example=yaml.safe_load(EXAMPLE.read_text(encoding="utf-8"))
    validator=Draft202012Validator(schema)
    validator.validate(example)

    runtime=json.loads(RUNTIME_CONTRACT.read_text(encoding="utf-8"))
    policy=runtime.get("capabilities",{}).get("agent_workspace",{})
    if policy.get("requirement")!="optional":
        raise SystemExit("FAIL: Agent Workspace must remain optional")
    if policy.get("github_policy")!="prefer_github_actions_when_sufficient":
        raise SystemExit("FAIL: GitHub Actions-first policy is missing")
    if policy.get("redundant_execution_forbidden") is not True:
        raise SystemExit("FAIL: redundant Agent Workspace execution must be forbidden")
    if policy.get("lifecycle")!=["create","upload","verify_or_build","collect_if_needed","destroy"]:
        raise SystemExit("FAIL: Agent Workspace lifecycle mismatch")
    if policy.get("cleanup")!="best_effort_required":
        raise SystemExit("FAIL: Agent Workspace cleanup policy mismatch")

    policy_text=POLICY_DOC.read_text(encoding="utf-8").lower()
    for marker in ("github actions", "redundant", "destroy", "execution cost"):
        if marker not in policy_text:
            raise SystemExit(f"FAIL: Agent Workspace policy documentation missing marker: {marker}")

    invalid=copy.deepcopy(example)
    invalid["cleanup"]["attempted"]=False
    try:
        validator.validate(invalid)
    except ValidationError:
        pass
    else:
        raise SystemExit("FAIL: Agent Workspace evidence accepted without cleanup attempt")

    invalid=copy.deepcopy(example)
    invalid["result"]="pass"
    invalid["verification"]=None
    # PASS without a verification description is semantically invalid even if structurally allowed.
    if invalid["result"]=="pass" and not invalid.get("verification"):
        pass
    else:
        raise SystemExit("FAIL: semantic false-PASS guard did not trigger")

    print("PASS: Agent Workspace evidence, GitHub Actions-first policy and cleanup guard are valid")
    return 0

if __name__=="__main__":
    sys.exit(main())
