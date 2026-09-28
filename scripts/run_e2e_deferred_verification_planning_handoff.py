#!/usr/bin/env python3
from pathlib import Path
import argparse
import sys
import yaml

def evaluate(case):
    i=case["input"]
    if i["phase"] == "plan" and i.get("planning_complete") and not i.get("handoff_zip_present"):
        return {
            "outcome": "planning_handoff",
            "allow_next_step": False,
            "selected_step": None,
            "in_progress": None,
            "next_recommended": i["implementation_step"],
            "dev001_implemented": False,
        }

    if i.get("handoff_zip_present") and i["phase"] == "execute":
        return {
            "outcome": "select_dev001",
            "allow_next_step": True,
            "selected_step": i["implementation_step"],
            "in_progress": i["implementation_step"],
            "next_recommended": i["implementation_step"],
            "dev001_implemented": False,
        }

    if i.get("project_failure_observed"):
        return {"outcome": "failed", "allow_next_step": False, "false_pass": False}

    if i.get("environment_limited"):
        if i.get("completion_blocking_risk"):
            return {"outcome": "blocked", "allow_next_step": False, "false_pass": False}
        return {"outcome": "passed_with_deferred", "allow_next_step": True, "false_pass": False}

    return {"outcome": "passed", "allow_next_step": True, "false_pass": False}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--scenario", required=True)
    args=ap.parse_args()
    data=yaml.safe_load(Path(args.scenario).read_text(encoding="utf-8"))
    errors=[]
    for case in data.get("cases", []):
        actual=evaluate(case)
        for key,value in case["expected"].items():
            if actual.get(key) != value:
                errors.append(f'{case["id"]}: {key} expected={value!r} actual={actual.get(key)!r}')
    if errors:
        print("FAIL")
        for e in errors:
            print("-", e)
        return 1
    print(f'PASS: deferred verification/planning handoff policy ({len(data.get("cases", []))} cases)')
    return 0

if __name__ == "__main__":
    sys.exit(main())
