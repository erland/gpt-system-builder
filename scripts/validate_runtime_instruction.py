#!/usr/bin/env python3
from pathlib import Path
import argparse,re,sys,yaml

REQUIRED_PHRASES = [
    "CREATE",
    "CHANGE",
    "IMPROVE",
    "one safe development step",
    "READ",
    "ASSESS",
    "SELECT",
    "LOCK",
    "IMPLEMENT",
    "VERIFY",
    "STOP",
    "actual current source",
    "Do not automatically continue",
    "Never report an unrun check as PASS",
    "complete project ZIP",
    "reuse the active PR",
    "READY_WITH_WARNINGS",
    "PostgreSQL server must not be embedded",
    "critical runtime rules",
]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("root")
    a=ap.parse_args()
    root=Path(a.root)
    ins=root/"runtime"/"canonical-instructions.md"
    man=root/"runtime"/"runtime-manifest.yaml"
    errs=[]

    if not ins.exists():
        errs.append("runtime/canonical-instructions.md missing")
        text=""
    else:
        text=ins.read_text(encoding="utf-8")

    if not man.exists():
        errs.append("runtime/runtime-manifest.yaml missing")
        data={}
    else:
        try:
            data=yaml.safe_load(man.read_text(encoding="utf-8"))
        except Exception as e:
            errs.append(f"runtime manifest YAML invalid: {e}")
            data={}

    for phrase in REQUIRED_PHRASES:
        if phrase not in text:
            errs.append(f"canonical instruction missing required concept: {phrase}")

    if len(text) < 5000:
        errs.append("canonical instruction unexpectedly short")
    if len(text) > 30000:
        errs.append("canonical instruction too large for practical runtime core")

    if data.get("primary_instruction") != "runtime/canonical-instructions.md":
        errs.append("runtime manifest primary_instruction mismatch")

    refs = list(data.get("core_references", [])) + list(data.get("standards", []))
    for ref in refs:
        if not (root/ref).exists():
            errs.append(f"manifest reference missing: {ref}")

    rules=data.get("rules",{})
    if rules.get("critical_behavior_in_knowledge_only") is not False:
        errs.append("critical_behavior_in_knowledge_only must be false")
    if rules.get("default_completed_steps_per_run") != 1:
        errs.append("default_completed_steps_per_run must be 1")
    if rules.get("source_state_over_chat_memory") is not True:
        errs.append("source_state_over_chat_memory must be true")
    if rules.get("false_pass_forbidden") is not True:
        errs.append("false_pass_forbidden must be true")

    if errs:
        print("FAIL")
        for e in errs:
            print("-",e)
        return 1

    print(f"PASS: canonical runtime instruction valid ({len(text)} chars, {len(refs)} direct references)")
    return 0

if __name__=="__main__":
    sys.exit(main())
