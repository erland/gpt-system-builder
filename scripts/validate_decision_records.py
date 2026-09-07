#!/usr/bin/env python3
from pathlib import Path
import argparse,re,sys

def main():
    p=argparse.ArgumentParser()
    p.add_argument("kind", choices=["adr","product"])
    p.add_argument("file")
    a=p.parse_args()
    t=Path(a.file).read_text(encoding="utf-8")
    pats = [
        r"^# ADR-\d{3,}\s+–\s+" if a.kind=="adr" else r"^# Product decisions$",
        r"^\*\*Status:\*\*",
        r"^\*\*Date:\*\*",
        r"^## Context$" if a.kind=="adr" else r"^### Context$",
        r"^## Decision$" if a.kind=="adr" else r"^### Decision$",
        r"^## Rationale$" if a.kind=="adr" else r"^### Rationale$",
    ]
    if a.kind=="product":
        pats.append(r"^## PD-\d{3,}\s+–\s+")
    errs=[x for x in pats if not re.search(x,t,re.M)]
    if errs:
        print("FAIL", errs)
        return 1
    print(f"PASS: {a.kind} decision record structure valid")
    return 0
if __name__=="__main__":
    sys.exit(main())
