#!/usr/bin/env python3
"""Regression checks for modular Chat and Plugin resource packaging."""
from collections import Counter
from pathlib import Path
from zipfile import ZipFile
import sys
import yaml

root = Path(__file__).resolve().parents[1]
version = sys.argv[1] if len(sys.argv) > 1 else (root / "VERSION").read_text().strip()
cfg = yaml.safe_load((root / "gpt-project.yaml").read_text(encoding="utf-8"))
assert cfg["skills"]["resource_policy"] == "explicit"
skills = {s["id"]: s for s in cfg["skills"]["definitions"]}
assert len(skills) == 8
for name, definition in skills.items():
    for kind in ("references", "assets", "scripts"):
        assert isinstance(definition.get(kind), list), (name, kind)
plugin = root / "dist" / f"system-builder-plugin-{version}.zip"
chat = root / "dist" / f"system-builder-chat-{version}.zip"
with ZipFile(plugin) as archive:
    members = set(archive.namelist())
    assert len(members) == len(archive.namelist())
    scripts = Counter()
    for name, definition in skills.items():
        base = f"skills/{name}/"
        skill_md = base + "SKILL.md"
        assert skill_md in members, skill_md
        skill_text = archive.read(skill_md).decode("utf-8")
        assert "## Canonical behavior" in skill_text, name
        for kind in ("references", "assets", "scripts"):
            declared = {Path(p).name for p in definition[kind]}
            actual = {
                Path(p).name for p in members
                if p.startswith(base + kind + "/")
                and "/" not in p[len(base + kind + "/"):]
                and not p.endswith("/")
            }
            assert actual == declared, (name, kind, actual, declared)
        scripts[name] = len(definition["scripts"])
    assert sum(scripts.values()) == 6, scripts
    assert sum(bool(n) for n in scripts.values()) == 3, scripts
with ZipFile(chat) as archive:
    members = set(archive.namelist())
    for name in skills:
        path = f"assistant/skills/{name}/SKILL.md"
        assert path in members, path
        text = archive.read(path).decode("utf-8")
        assert "## Canonical behavior" in text, name
        assert len(text) > 200, name
    assert "assistant/instructions.md" in members
print("PASS: modular Chat and scoped Plugin resources")
