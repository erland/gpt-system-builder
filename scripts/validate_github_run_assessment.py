#!/usr/bin/env python3
from pathlib import Path
import argparse,re,sys

REQ = [
    "Repository","Active work series","Pull request","State discovery",
    "Drift / baseline","Selected action","Required verification",
    "Commit plan","PR update","Stop condition"
]

def main():
    p=argparse.ArgumentParser()
    p.add_argument("file")
    a=p.parse_args()
    t=Path(a.file).read_text(encoding="utf-8")
    errs=[]
    for h in REQ:
        if not re.search(rf"^##\s+{re.escape(h)}$", t, re.M):
            errs.append(f"missing section: {h}")
    if not re.search(r"- reuse:\s+(yes|no)\b", t):
        errs.append("PR reuse must be yes/no")
    if "Stop after one verified step" not in t:
        errs.append("explicit one-step stop condition missing")
    if not re.search(r"- message:\s+\S", t):
        errs.append("commit message missing")
    if errs:
        print("FAIL")
        for e in errs:
            print("-", e)
        return 1
    print("PASS: GitHub run assessment structure valid")
    return 0

if __name__=="__main__":
    sys.exit(main())
