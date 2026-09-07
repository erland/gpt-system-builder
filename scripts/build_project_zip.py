#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import zipfile

EXCLUDED_DIRS = {"dist", ".git", "__pycache__", ".pytest_cache"}
EXCLUDED_FILES = {".DS_Store"}


def should_include(path: Path, root: Path) -> bool:
    rel = path.relative_to(root)
    if any(part in EXCLUDED_DIRS for part in rel.parts):
        return False
    if path.name in EXCLUDED_FILES:
        return False
    return path.is_file()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--output")
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    version = (root / "VERSION").read_text(encoding="utf-8").strip()
    dist = root / "dist"
    dist.mkdir(parents=True, exist_ok=True)
    output = Path(args.output).resolve() if args.output else dist / f"system-builder-project-v{version}.zip"

    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(root.rglob("*")):
            if should_include(path, root):
                archive.write(path, path.relative_to(root).as_posix())

    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
