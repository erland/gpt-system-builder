#!/usr/bin/env python3
from pathlib import Path
import argparse,re,sys

def require(text, headings):
    errs=[]
    for h in headings:
        if not re.search(rf"^##\s+{re.escape(h)}$", text, re.M):
            errs.append(f"missing section: {h}")
    return errs

def main():
    p=argparse.ArgumentParser()
    p.add_argument("kind", choices=["request","impact"])
    p.add_argument("file")
    a=p.parse_args()
    t=Path(a.file).read_text(encoding="utf-8")
    if a.kind=="request":
        errs=require(t,["Current problem","Desired outcome","Scope","Affected users / actors",
                        "Compatibility expectations","Data / migration expectations","Acceptance","Open questions"])
        if not re.search(r"^# CR-\d{3,}\s+–\s+",t,re.M):
            errs.append("missing CR ID/title")
    else:
        errs=require(t,["Summary","Functional impact","Architecture impact","Data / migration impact",
                        "Integration / API impact","Security / authorization impact","UI impact",
                        "Test / regression impact","Configuration / deployment impact",
                        "Installation / operations impact","Blast radius","Risks / blockers",
                        "Recommended plan implications"])
        if not re.search(r"^## Blast radius$\n\n(?:local|cross-component|system-wide)\b",t,re.M):
            errs.append("invalid blast radius")
    if errs:
        print("FAIL")
        for e in errs: print("-",e)
        return 1
    print(f"PASS: CHANGE {a.kind} structure valid")
    return 0
if __name__=="__main__":
    sys.exit(main())
