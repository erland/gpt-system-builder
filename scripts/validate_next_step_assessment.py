#!/usr/bin/env python3
from pathlib import Path
import argparse,re,sys

REQ=[
    "Current mode","Current selected step","Blocking issues","Verification state",
    "Source drift","Dependency check","Recommended action","Lock state",
    "Completion evidence required","Stop condition"
]

def main():
    p=argparse.ArgumentParser()
    p.add_argument("file")
    a=p.parse_args()
    t=Path(a.file).read_text(encoding="utf-8")
    errs=[]
    for h in REQ:
        if not re.search(rf"^##\s+{re.escape(h)}$",t,re.M):
            errs.append(f"missing section: {h}")
    if not re.search(r"^## Source drift$\n\n(?:none|detected)\b",t,re.M):
        errs.append("source drift must be none/detected")
    if "Stop after" not in t:
        errs.append("explicit stop condition missing")
    if errs:
        print("FAIL")
        for e in errs: print("-",e)
        return 1
    print("PASS: next-step assessment structure valid")
    return 0
if __name__=="__main__":
    sys.exit(main())
