#!/usr/bin/env python3
from pathlib import Path
import argparse, re, sys

RISK_RE = re.compile(r"^###\s+(RISK-\d{3,})\s+–\s+(.+)$", re.M)
FIELDS = ["Category", "Probability", "Impact", "Level", "Status"]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    args = ap.parse_args()
    text = Path(args.file).read_text(encoding="utf-8")
    errors = []
    matches = list(RISK_RE.finditer(text))
    ids = [m.group(1) for m in matches]

    if len(ids) != len(set(ids)):
        errors.append("duplicate RISK ID")

    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i+1].start() if i+1 < len(matches) else len(text)
        block = text[start:end]
        rid = m.group(1)
        for field in FIELDS:
            if not re.search(rf"^\*\*{field}:\*\*\s+\S+", block, re.M):
                errors.append(f"{rid}: missing {field}")
        if not re.search(r"^\*\*Handling\*\*", block, re.M):
            errors.append(f"{rid}: missing Handling")

    if errors:
        print("FAIL")
        for e in errors:
            print("-", e)
        return 1

    print(f"PASS: risk/feasibility structure valid ({len(matches)} risks)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
