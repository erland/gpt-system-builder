#!/usr/bin/env python3
from pathlib import Path
import argparse, sys, yaml

def decide(case):
    i=case["inputs"]
    if i.get("source_mode")=="zip":
        if i.get("equivalent_local_verification_available"):
            return {
                "action":"run_local_equivalent",
                "manual_verification_required":False,
                "completion_allowed":bool(i.get("local_verification_passes")) and not i.get("genuine_external_gate_required",False),
            }
        if i.get("genuine_external_gate_required") and not i.get("external_gate_available",False):
            return {
                "action":"checkpoint_pending_external",
                "manual_verification_required":True,
                "completion_allowed":False,
            }
    if not i.get("implementation_matches_intent", True):
        if i.get("explicit_direction_change"):
            return {
                "action":"update_governing_docs",
                "update_governing_docs":True,
                "release_readiness_allowed":False,
            }
        if i.get("final_reconciliation") and i.get("mismatch_kind")=="decision":
            return {
                "action":"ask_user",
                "update_governing_docs":False,
                "release_readiness_allowed":False,
            }
        return {
            "action":"repair_implementation",
            "update_governing_docs":False,
            "release_readiness_allowed":False,
        }
    return {"action":"no_op"}

def require_text(root, path, phrases, errors):
    text=(root/path).read_text(encoding="utf-8").lower()
    for phrase in phrases:
        if phrase.lower() not in text:
            errors.append(f"{path}: missing policy phrase: {phrase}")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--scenario", required=True)
    a=ap.parse_args()
    root=Path(__file__).resolve().parents[1]
    data=yaml.safe_load(Path(a.scenario).read_text(encoding="utf-8"))
    errors=[]
    for case in data.get("cases",[]):
        actual=decide(case)
        for key,value in case["expected"].items():
            if actual.get(key)!=value:
                errors.append(f"{case['id']}: {key} expected={value!r} actual={actual.get(key)!r}")

    require_text(root,"docs/change-mode.md",["Governing intent during CHANGE","Final documentation reconciliation"],errors)
    require_text(root,"docs/zip-mode.md",["Best-effort automatic verification","GitHub Actions är inte i sig en unik verifieringsgate"],errors)
    require_text(root,"docs/completion-verification.md",["CI-gate är inte automatiskt extern"],errors)
    require_text(root,"runtime/canonical-instructions.md",["governing intent","CI is not inherently an external gate"],errors)

    if errors:
        print("FAIL")
        for error in errors:
            print("-",error)
        return 1
    print(f"PASS: documentation/ZIP policy regression ({len(data.get('cases',[]))} scenarios)")
    return 0

if __name__=="__main__":
    sys.exit(main())
