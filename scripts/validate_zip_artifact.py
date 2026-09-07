#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path, PurePosixPath
import argparse, hashlib, zipfile, shutil, os, sys

FORBIDDEN_PREFIXES = ("/", "\\")
TRANSIENT_NAMES = {".DS_Store"}

def safe_members(zf: zipfile.ZipFile):
    for info in zf.infolist():
        raw = info.filename.replace("\\", "/")
        p = PurePosixPath(raw)
        if raw.startswith(FORBIDDEN_PREFIXES):
            raise ValueError(f"absolute path in ZIP: {info.filename}")
        if any(part == ".." for part in p.parts):
            raise ValueError(f"path traversal in ZIP: {info.filename}")
        yield info

def extract_safe(src: Path, dest: Path):
    dest.mkdir(parents=True, exist_ok=True)
    for info in safe_members(zipfile.ZipFile(src, "r")):
        raw = info.filename.replace("\\", "/")
        if not raw or raw.endswith("/"):
            (dest / raw).mkdir(parents=True, exist_ok=True)
            continue
        target = (dest / raw).resolve()
        if dest.resolve() not in target.parents and target != dest.resolve():
            raise ValueError(f"path escapes destination: {raw}")
        target.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(src, "r").open(info, "r") as r, target.open("wb") as w:
            shutil.copyfileobj(r, w)

def sha256(path: Path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()

def detect_root(dest: Path):
    entries = [p for p in dest.iterdir() if p.name not in TRANSIENT_NAMES]
    files = [p for p in entries if p.is_file()]
    dirs = [p for p in entries if p.is_dir()]
    if files:
        return dest
    if len(dirs) == 1:
        return dirs[0]
    return dest

def main():
    p=argparse.ArgumentParser()
    p.add_argument("zipfile")
    p.add_argument("--extract-to")
    args=p.parse_args()
    src=Path(args.zipfile)
    with zipfile.ZipFile(src,"r") as z:
        bad=z.testzip()
        if bad:
            print(f"FAIL: corrupt member {bad}")
            return 1
        list(safe_members(z))
    print("PASS: ZIP integrity and path safety")
    print("SHA-256:",sha256(src))
    if args.extract_to:
        dest=Path(args.extract_to)
        if dest.exists():
            shutil.rmtree(dest)
        extract_safe(src,dest)
        print("Project root:",detect_root(dest))
    return 0
if __name__=="__main__":
    sys.exit(main())
