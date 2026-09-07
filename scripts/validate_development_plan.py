#!/usr/bin/env python3
from pathlib import Path
import argparse, re, sys

STEP_RE = re.compile(r"^##\s+(DEV-\d{3,})\s+–\s+(.+)$", re.M)
REQUIRED_SUBSECTIONS = [
    "Mål", "Scope", "Förutsättningar", "Implementation", "Verifiering", "Klart-kriterier", "Beroenden"
]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    args = ap.parse_args()
    text = Path(args.file).read_text(encoding="utf-8")
    errors = []
    matches = list(STEP_RE.finditer(text))
    ids = [m.group(1) for m in matches]

    if not matches:
        errors.append("no DEV steps found")
    if len(ids) != len(set(ids)):
        errors.append("duplicate DEV step ID")

    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i+1].start() if i+1 < len(matches) else len(text)
        block = text[start:end]
        sid = m.group(1)
        for sub in REQUIRED_SUBSECTIONS:
            if not re.search(rf"^###\s+{re.escape(sub)}$", block, re.M):
                errors.append(f"{sid}: missing subsection {sub}")
        if not re.search(r"^- \[[ xX]\]", block, re.M):
            errors.append(f"{sid}: no checkbox clear criteria found")

    if errors:
        print("FAIL")
        for e in errors:
            print("-", e)
        return 1
    print(f"PASS: development plan valid ({len(matches)} steps)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
