#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
import sys
import yaml
import jsonschema

TERMINAL_OK = {"implemented", "verified"}

def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_json(path: Path):
    import json
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def schema_validate(data, schema):
    jsonschema.Draft202012Validator(schema).validate(data)

def semantic_errors(data):
    errors = []
    reqs = data.get("requirements", {})
    acs = data.get("acceptance_criteria", {})
    steps = data.get("development_steps", {})
    tests = data.get("verification", {})

    # Cross-reference existence
    for rid, r in reqs.items():
        for sid in r.get("development_steps", []):
            if sid not in steps:
                errors.append(f"{rid}: references missing development step {sid}")
        for aid in r.get("acceptance_criteria", []):
            if aid not in acs:
                errors.append(f"{rid}: references missing acceptance criterion {aid}")
        for tid in r.get("verification", []):
            if tid not in tests:
                errors.append(f"{rid}: references missing verification {tid}")

    for aid, a in acs.items():
        rid = a["requirement"]
        if rid not in reqs:
            errors.append(f"{aid}: references missing requirement {rid}")
        for tid in a.get("verification", []):
            if tid not in tests:
                errors.append(f"{aid}: references missing verification {tid}")

    for sid, s in steps.items():
        for rid in s.get("requirements", []):
            if rid not in reqs:
                errors.append(f"{sid}: references missing requirement {rid}")

    for tid, t in tests.items():
        for rid in t.get("requirements", []):
            if rid not in reqs:
                errors.append(f"{tid}: references missing requirement {rid}")
        for aid in t.get("acceptance_criteria", []):
            if aid not in acs:
                errors.append(f"{tid}: references missing acceptance criterion {aid}")

    # Bidirectional consistency where both sides are present
    for rid, r in reqs.items():
        for sid in r.get("development_steps", []):
            if sid in steps and rid not in steps[sid].get("requirements", []):
                errors.append(f"{rid}/{sid}: asymmetric requirement-step relation")

    # Orphan and must checks
    for rid, r in reqs.items():
        status = r["status"]
        priority = r["priority"]
        steps_for_req = r.get("development_steps", [])
        verification = r.get("verification", [])
        ac_list = r.get("acceptance_criteria", [])

        if status not in {"identified", "cancelled", "deferred"} and not steps_for_req:
            errors.append(f"{rid}: orphan requirement has no development_steps")

        if priority == "must" and status in TERMINAL_OK and not verification:
            errors.append(f"{rid}: must requirement is {status} but has no verification")

        if status == "verified":
            if not verification:
                errors.append(f"{rid}: verified requirement has no verification reference")
            for tid in verification:
                if tid in tests and tests[tid]["status"] != "passed":
                    errors.append(f"{rid}: verified but {tid} is not passed")

        for aid in ac_list:
            if aid in acs and acs[aid]["requirement"] != rid:
                errors.append(f"{rid}/{aid}: acceptance criterion points to a different requirement")

    return errors

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--file", required=True)
    p.add_argument("--schema", required=True)
    p.add_argument("--expect-invalid", action="store_true")
    args = p.parse_args()

    data = load_yaml(Path(args.file))
    schema = load_json(Path(args.schema))
    try:
        schema_validate(data, schema)
        errs = semantic_errors(data)
        if errs:
            raise ValueError("\n".join(errs))
        valid = True
        detail = "valid"
    except Exception as e:
        valid = False
        detail = str(e)

    if args.expect_invalid:
        if valid:
            print("FAIL: expected invalid but validation passed")
            return 1
        print("PASS: invalid fixture rejected")
        return 0

    if not valid:
        print("FAIL:", detail)
        return 1
    print("PASS: traceability contract valid")
    return 0

if __name__ == "__main__":
    sys.exit(main())
