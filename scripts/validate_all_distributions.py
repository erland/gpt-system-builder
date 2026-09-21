#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, subprocess, sys
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]
REGISTRY=ROOT/"runtime"/"distribution-registry.yaml"

def render(parts, artifact):
    values={"{python}":sys.executable,"{artifact}":str(artifact)}
    return [values.get(part, part) for part in parts]

def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument("--manifest",required=True); a=ap.parse_args()
    registry=yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    manifest=json.loads(Path(a.manifest).read_text(encoding="utf-8"))
    artifacts=manifest.get("artifacts",{})
    expected=registry["active_targets"]
    if set(artifacts)!=set(expected):
        raise SystemExit("FAIL: build manifest runtime set does not match registry")
    for runtime in expected:
        artifact=Path(artifacts[runtime])
        if not artifact.is_absolute(): artifact=ROOT/artifact
        if not artifact.is_file(): raise SystemExit(f"FAIL: artifact missing for {runtime}: {artifact}")
        print(f"== validate {runtime}: {artifact} ==")
        subprocess.run(render(registry["targets"][runtime]["validator"],artifact),cwd=ROOT,check=True)
    print("PASS: all active runtime distributions validated"); return 0

if __name__=="__main__":
    sys.exit(main())
