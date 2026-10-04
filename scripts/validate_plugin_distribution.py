#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path

REQUIRED = {
    "plugin.json",
    "README.md",
    "compatibility.md",
    "runtime-contract.json",
    "skills/system-builder/SKILL.md",
}

FORBIDDEN_PARTS = {
    ".git",
    ".github",
    "tests",
    "evals",
    "research",
    "dist",
    "dist-ci",
    "__pycache__",
    ".pytest_cache",
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("artifact")
    args = ap.parse_args()
    path = Path(args.artifact)

    errors = []
    with zipfile.ZipFile(path) as zf:
        names = set(zf.namelist())
        missing = sorted(REQUIRED - names)
        if missing:
            errors.append("missing required files: " + ", ".join(missing))

        for name in names:
            parts = set(Path(name).parts)
            if parts & FORBIDDEN_PARTS:
                errors.append(f"forbidden runtime path: {name}")

        if "plugin.json" in names:
            manifest = json.loads(zf.read("plugin.json").decode("utf-8"))
            for key in ("$schema", "name", "version", "description"):
                if not manifest.get(key):
                    errors.append(f"plugin.json missing {key}")

        if "skills/system-builder/SKILL.md" in names:
            skill = zf.read("skills/system-builder/SKILL.md").decode("utf-8")
            for marker in (
                "name: system-builder",
                "## Runtime requirements",
                "Code execution: required",
                "Never simulate a deterministic verification result",
                "## Canonical behavior",
            ):
                if marker not in skill:
                    errors.append(f"SKILL.md missing marker: {marker}")

        if "runtime-contract.json" in names:
            snapshot = json.loads(zf.read("runtime-contract.json").decode("utf-8"))
            if snapshot.get("runtime_id") != "openai_plugin":
                errors.append("runtime-contract runtime_id mismatch")
            req = snapshot.get("runtime_requirements", {})
            if req.get("filesystem", {}).get("write") != "required":
                errors.append("filesystem write requirement missing")
            if req.get("code_execution", {}).get("level") != "required":
                errors.append("code execution requirement missing")
            if req.get("persistent_state", {}).get("level") != "required":
                errors.append("persistent state requirement missing")
            projection = snapshot.get("tool_projection", {})
            if projection.get("mcp_generated") is not False:
                errors.append("plugin must not claim generated MCP tools")
            if projection.get("strategy") != "host_capability_mapping":
                errors.append("tool projection strategy mismatch")

        if "compatibility.md" in names:
            compat = zf.read("compatibility.md").decode("utf-8").lower()
            for phrase in ("host-dependent", "filesystem read/write", "code execution", "persistent workspace/state", "github"):
                if phrase not in compat:
                    errors.append(f"compatibility limitation missing: {phrase}")

    if errors:
        print("FAIL")
        for error in errors:
            print("-", error)
        return 1

    print("PASS: OpenAI Plugin distribution validated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
