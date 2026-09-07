#!/usr/bin/env python3
from pathlib import Path
import argparse,yaml,sys
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("file"); a=ap.parse_args()
    d=yaml.safe_load(Path(a.file).read_text(encoding="utf-8")); errs=[]
    if d.get("decision") not in {"READY","READY_WITH_WARNINGS"}: errs.append("not releasable")
    if d.get("blockers"): errs.append("blockers present")
    bad=[g["gate"] for g in d.get("gates",[]) if g.get("required") and g.get("result")!="pass"]
    if bad: errs.append("required failures: "+",".join(bad))
    if d.get("required_gates_passed")!=d.get("required_gates_total"): errs.append("gate count mismatch")
    if d.get("decision")=="READY_WITH_WARNINGS" and not d.get("warnings"): errs.append("warning list required")
    if errs:
        print("FAIL"); [print("-",e) for e in errs]; return 1
    print(f"PASS: final release readiness {d['decision']} ({d['required_gates_total']} gates)")
    return 0
if __name__=="__main__": sys.exit(main())
