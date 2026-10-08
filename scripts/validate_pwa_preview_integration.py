#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import yaml
from jsonschema import Draft202012Validator, ValidationError, FormatChecker

ROOT=Path(__file__).resolve().parents[1]
SCHEMA=ROOT/"schemas"/"pwa-preview-evidence.schema.json"
EXAMPLE=ROOT/"examples"/"pwa-preview-evidence.example.yaml"
RUNTIME=ROOT/"runtime"/"runtime-contract.json"
POLICY=ROOT/"docs"/"pwa-preview-integration.md"

def main()->int:
    schema=json.loads(SCHEMA.read_text(encoding="utf-8"))
    example=yaml.safe_load(EXAMPLE.read_text(encoding="utf-8"))
    validator=Draft202012Validator(schema, format_checker=FormatChecker())
    validator.validate(example)

    runtime=json.loads(RUNTIME.read_text(encoding="utf-8"))
    policy=runtime.get("capabilities",{}).get("pwa_preview",{})
    if policy.get("requirement")!="optional":
        raise SystemExit("FAIL: PWA Preview must remain optional")
    if policy.get("source_transport")!="https_archive_url":
        raise SystemExit("FAIL: PWA Preview source transport must be HTTPS archive URL")
    if policy.get("preview_is_functional_verification") is not False:
        raise SystemExit("FAIL: preview must not count as functional verification")
    if policy.get("preview_is_production_deployment") is not False:
        raise SystemExit("FAIL: preview must not count as production deployment")
    if policy.get("agent_workspace_policy")!="do_not_start_only_for_preview_when_cheaper_source_exists":
        raise SystemExit("FAIL: PWA Preview must not force unnecessary Agent Workspace execution")
    if policy.get("lifecycle")!=["create_or_update","get_if_needed","extend_only_if_needed","delete_or_expire"]:
        raise SystemExit("FAIL: PWA Preview lifecycle must preserve create/update/get/extend/delete-or-expire semantics")

    text=POLICY.read_text(encoding="utf-8").lower()
    for marker in ("zip", "tar.gz", "https", "github actions", "ready", "functional", "production", "5", "1440", "update", "extend", "delete"):
        if marker not in text:
            raise SystemExit(f"FAIL: PWA Preview policy missing marker: {marker}")

    invalid=copy.deepcopy(example)
    invalid["source"]["verified"]=False
    try:
        validator.validate(invalid)
    except ValidationError:
        pass
    else:
        raise SystemExit("FAIL: unverified artifact accepted for PWA Preview evidence")

    invalid=copy.deepcopy(example)
    invalid["functional_verification"]=True
    try:
        validator.validate(invalid)
    except ValidationError:
        pass
    else:
        raise SystemExit("FAIL: preview incorrectly accepted as functional verification")

    print("PASS: PWA Preview evidence and separation-of-concerns policy are valid")
    return 0

if __name__=="__main__":
    sys.exit(main())
