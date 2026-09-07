#!/usr/bin/env python3
from pathlib import Path
import argparse,re,sys

REQ = [
    "Technical goal","Motivation","Behavior to preserve","Non-goals","Baseline",
    "Risk areas","Characterization tests needed","Proposed improvement steps",
    "Verification","Blocking issues"
]

def main():
    p=argparse.ArgumentParser()
    p.add_argument("file")
    a=p.parse_args()
    text=Path(a.file).read_text(encoding="utf-8")
    errs=[]
    for h in REQ:
        if not re.search(rf"^##\s+{re.escape(h)}$", text, re.M):
            errs.append(f"missing section: {h}")
    if not re.search(r"^## Characterization tests needed$\n\n(?:yes|no)\b", text, re.M):
        errs.append("characterization tests needed must be yes/no")
    if not re.search(r"Behavior to preserve", text):
        errs.append("behavior preservation not explicit")
    if errs:
        print("FAIL")
        for e in errs: print("-",e)
        return 1
    print("PASS: IMPROVE intake structure valid")
    return 0
if __name__=="__main__":
    sys.exit(main())
