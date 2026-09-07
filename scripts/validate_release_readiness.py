#!/usr/bin/env python3
from pathlib import Path
import argparse,re,sys

REQ = [
    "Release candidate","Scope","Gate summary","Acceptance","Verification evidence",
    "Security / risk","Packaging / deployment","Documentation","Known limitations",
    "Blockers","Decision","Decision rationale"
]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("file")
    a=ap.parse_args()
    t=Path(a.file).read_text(encoding="utf-8")
    errs=[]

    for h in REQ:
        if not re.search(rf"^##\s+{re.escape(h)}$", t, re.M):
            errs.append(f"missing section: {h}")

    m=re.search(r"^## Decision$\n\n(READY|READY_WITH_WARNINGS|NOT_READY)\s*$", t, re.M)
    if not m:
        errs.append("decision must be READY, READY_WITH_WARNINGS or NOT_READY")
        decision=None
    else:
        decision=m.group(1)

    rows=[]
    for line in t.splitlines():
        if line.startswith("|") and not re.match(r"^\|\s*-", line):
            cells=[c.strip() for c in line.strip("|").split("|")]
            if len(cells)>=4 and cells[0]!="Gate":
                rows.append(cells[:4])

    required_fail=[]
    warnings=[]
    for gate, required, result, evidence in rows:
        req=required.lower()=="yes"
        res=result.lower()
        if req and res != "pass":
            required_fail.append((gate,res))
        if res=="warning":
            warnings.append(gate)

    if decision in ("READY","READY_WITH_WARNINGS") and required_fail:
        errs.append(f"ready decision impossible with required non-pass gates: {required_fail}")
    if decision=="READY" and warnings:
        errs.append("READY cannot contain warning gate results")
    if decision=="READY_WITH_WARNINGS" and not warnings and "warning" not in t.lower():
        errs.append("READY_WITH_WARNINGS requires documented warning")
    if decision=="NOT_READY" and not required_fail and "block" not in t.lower():
        errs.append("NOT_READY should identify a required failure/blocker")

    if errs:
        print("FAIL")
        for e in errs: print("-",e)
        return 1

    print(f"PASS: release readiness valid ({decision})")
    return 0

if __name__=="__main__":
    sys.exit(main())
