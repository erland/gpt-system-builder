#!/usr/bin/env python3
from pathlib import Path
import argparse, re, sys

REQUIRED_HEADINGS = [
    r"^# ",
    r"^## .*Purpose|^## .*Syfte",
]
ID_PATTERNS = {
    "FR": re.compile(r"^###\s+(FR-\d{3,})\b", re.M),
    "NFR": re.compile(r"^###\s+(NFR-\d{3,})\b", re.M),
    "AC": re.compile(r"^###\s+(AC-\d{3,})\b", re.M),
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    args = ap.parse_args()
    text = Path(args.file).read_text(encoding="utf-8")

    errors = []
    if not text.startswith("# "):
        errors.append("missing H1 title")

    if not re.search(r"^## .*?(Purpose|Syfte)", text, re.M | re.I):
        errors.append("missing purpose section")

    if not re.search(r"^## .*?(Scope)", text, re.M | re.I):
        errors.append("missing scope section")

    if not re.search(r"^## .*?(Functional requirements|Funktionella krav)", text, re.M | re.I):
        errors.append("missing functional requirements section")

    if not re.search(r"^## .*?(Acceptance criteria)", text, re.M | re.I):
        errors.append("missing acceptance criteria section")

    seen = {}
    for kind, pat in ID_PATTERNS.items():
        ids = pat.findall(text)
        for ident in ids:
            if ident in seen:
                errors.append(f"duplicate ID: {ident}")
            seen[ident] = kind

    # Every AC should mention related requirement(s) in the following block before next H3.
    for match in re.finditer(r"^###\s+(AC-\d{3,})\b(.*?)(?=^###\s+|\Z)", text, re.M | re.S):
        aid, block = match.group(1), match.group(2)
        if not re.search(r"(FR|NFR)-\d{3,}", block):
            errors.append(f"{aid}: no related FR/NFR reference found")

    if errors:
        print("FAIL")
        for e in errors:
            print("-", e)
        return 1

    print("PASS: functional specification structure valid")
    return 0

if __name__ == "__main__":
    sys.exit(main())
