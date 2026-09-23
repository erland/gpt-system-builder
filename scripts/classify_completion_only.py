#!/usr/bin/env python3
from pathlib import Path
import argparse, sys

ALLOWED = {
    "project-status.yaml",
    "STATUS.md",
    ".system-builder/work-status.yaml",
    ".system-builder/traceability.yaml",
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--paths-file", required=True)
    args = ap.parse_args()
    paths = [line.strip() for line in Path(args.paths_file).read_text(encoding="utf-8").splitlines() if line.strip()]
    if not paths:
        print("not completion-only: no changed paths")
        return 1
    unexpected = [p for p in paths if p not in ALLOWED]
    if unexpected:
        print("not completion-only; unexpected paths:")
        for p in unexpected:
            print("-", p)
        return 1
    print("completion-only")
    return 0

if __name__ == "__main__":
    sys.exit(main())
