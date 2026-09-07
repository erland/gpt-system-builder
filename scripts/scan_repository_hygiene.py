#!/usr/bin/env python3
from pathlib import Path
import argparse, json, os, re, sys

TEMP_NAMES = {".DS_Store", "Thumbs.db"}
TEMP_SUFFIXES = {".tmp", ".swp", ".log"}
GENERATED_DIRS = {"node_modules", "__pycache__", ".pytest_cache", "target", "dist", "build", "coverage", ".venv"}
SECRET_NAMES = {".env", ".env.production", ".env.local"}
KEY_PATTERNS = [
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"(?i)\b(api[_-]?key|token|password|secret)\s*[:=]\s*['\"]?[^\\s'\"]{8,}")
]

def scan(root: Path):
    findings = {"pass": [], "warning": [], "blocked": []}
    for p in root.rglob("*"):
        rel = p.relative_to(root).as_posix()
        parts = set(p.parts)
        if ".git" in parts:
            continue
        if p.is_dir() and p.name in GENERATED_DIRS:
            findings["warning"].append({"path": rel, "reason": "generated/dependency directory present"})
            continue
        if not p.is_file():
            continue
        if p.name in TEMP_NAMES or p.suffix in TEMP_SUFFIXES:
            findings["warning"].append({"path": rel, "reason": "temporary/local artifact"})
        if p.name in SECRET_NAMES:
            findings["blocked"].append({"path": rel, "reason": "secret/environment file candidate"})
        if p.suffix == ".zip":
            findings["warning"].append({"path": rel, "reason": "archive in source tree"})
        if p.stat().st_size <= 1024 * 1024:
            try:
                text = p.read_text(encoding="utf-8")
            except Exception:
                text = None
            if text:
                for pat in KEY_PATTERNS:
                    if pat.search(text):
                        findings["blocked"].append({"path": rel, "reason": "credential/private-key pattern candidate"})
                        break
    if not (root / ".gitignore").exists():
        findings["warning"].append({"path": ".gitignore", "reason": "missing .gitignore"})
    if (root / "Dockerfile").exists() and not (root / ".dockerignore").exists():
        findings["warning"].append({"path": ".dockerignore", "reason": "Dockerfile present but .dockerignore missing"})
    if not findings["blocked"]:
        findings["pass"].append({"reason": "no blocking hygiene findings detected"})
    return findings

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    result = scan(Path(args.root))
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        for level in ["pass","warning","blocked"]:
            print(level.upper())
            for item in result[level]:
                print("-", item.get("path",""), item["reason"])
    return 2 if result["blocked"] else 0

if __name__ == "__main__":
    sys.exit(main())
