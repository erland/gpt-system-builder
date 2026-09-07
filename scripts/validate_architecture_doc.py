#!/usr/bin/env python3
from pathlib import Path
import argparse, re, sys

def main():
    p = argparse.ArgumentParser()
    p.add_argument("file")
    args = p.parse_args()
    text = Path(args.file).read_text(encoding="utf-8")
    errors = []

    if not text.startswith("# "):
        errors.append("missing H1 title")

    required = [
        ("goals", r"^## .*?(Architecture goals|Goals)"),
        ("context", r"^## .*?(System context)"),
        ("components", r"^## .*?(Main components|Components and responsibilities)"),
        ("security", r"^## .*?(Security)"),
        ("deployment", r"^## .*?(Deployment)"),
    ]
    for name, pat in required:
        if not re.search(pat, text, re.M | re.I):
            errors.append(f"missing {name} section")

    # Flag obvious file-inventory anti-pattern if there are many source file names but no component headings.
    file_mentions = len(re.findall(r"\b[\w.-]+\.(java|ts|tsx|js|py|go|cs)\b", text))
    component_headings = len(re.findall(r"^###\s+", text, re.M))
    if file_mentions >= 8 and component_headings < 2:
        errors.append("architecture appears to be file inventory rather than component-level description")

    if errors:
        print("FAIL")
        for e in errors:
            print("-", e)
        return 1

    print("PASS: architecture structure valid")
    return 0

if __name__ == "__main__":
    sys.exit(main())
