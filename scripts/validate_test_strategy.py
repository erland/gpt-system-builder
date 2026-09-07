#!/usr/bin/env python3
from pathlib import Path
import argparse, re, sys

def main():
    p=argparse.ArgumentParser()
    p.add_argument("file")
    a=p.parse_args()
    text=Path(a.file).read_text(encoding="utf-8")
    errors=[]
    for heading in ["Scope","Quality risks","Test levels","Automated checks","Regression strategy","Release gates"]:
        if not re.search(rf"^##\s+{re.escape(heading)}$", text, re.M):
            errors.append(f"missing section: {heading}")

    ids=re.findall(r"^###\s+(TEST-\d{3,})\b", text, re.M)
    if len(ids)!=len(set(ids)):
        errors.append("duplicate TEST ID")

    if "Release gates" in text and not re.search(r"pass|verified|block", text, re.I):
        errors.append("release gates do not contain observable outcome language")

    if errors:
        print("FAIL")
        for e in errors:
            print("-",e)
        return 1
    print(f"PASS: test strategy structure valid ({len(ids)} TEST IDs)")
    return 0

if __name__=="__main__":
    sys.exit(main())
