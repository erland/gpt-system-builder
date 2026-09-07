#!/usr/bin/env python3
from pathlib import Path
import argparse,re,sys

REQUIRED = [
    "Need","Users / actors","Goals","Success criteria","Scope","Constraints",
    "Integrations","Data / persistence","Deployment target","Security considerations",
    "Blocking questions","Complexity","Next artifact"
]

def main():
    p=argparse.ArgumentParser()
    p.add_argument("file")
    a=p.parse_args()
    text=Path(a.file).read_text(encoding="utf-8")
    errors=[]
    for h in REQUIRED:
        if not re.search(rf"^##\s+{re.escape(h)}$", text, re.M):
            errors.append(f"missing section: {h}")
    if not re.search(r"^## Complexity$\n\n(?:small|medium|large)\b", text, re.M):
        errors.append("complexity must be small/medium/large")
    if errors:
        print("FAIL")
        for e in errors:
            print("-",e)
        return 1
    print("PASS: CREATE intake structure valid")
    return 0

if __name__=="__main__":
    sys.exit(main())
