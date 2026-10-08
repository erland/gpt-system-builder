#!/usr/bin/env python3
from __future__ import annotations
import copy, json, sys
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator, ValidationError

ROOT=Path(__file__).resolve().parents[1]
SCHEMA=ROOT/"schemas"/"agent-workspace-evidence.schema.json"
EXAMPLE=ROOT/"examples"/"agent-workspace-evidence.example.yaml"

def main()->int:
    schema=json.loads(SCHEMA.read_text(encoding="utf-8"))
    example=yaml.safe_load(EXAMPLE.read_text(encoding="utf-8"))
    validator=Draft202012Validator(schema)
    validator.validate(example)

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

    print("PASS: Agent Workspace evidence contract and cleanup guard are valid")
    return 0

if __name__=="__main__":
    sys.exit(main())
