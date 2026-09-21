#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, subprocess, sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "runtime" / "distribution-registry.yaml"

def render(parts, output):
    values={"{python}":sys.executable,"{output}":str(output)}
    return [values.get(part, part) for part in parts]

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--output-dir",required=True)
    ap.add_argument("--version",required=True)
    a=ap.parse_args()
    registry=yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    out=Path(a.output_dir); out.mkdir(parents=True,exist_ok=True)
    artifacts={}
    for runtime in registry["active_targets"]:
        cfg=registry["targets"][runtime]
        artifact=out/cfg["artifact_pattern"].format(version=a.version)
        print(f"== build {runtime}: {artifact} ==")
        subprocess.run(render(cfg["builder"],artifact),cwd=ROOT,check=True)
        if not artifact.is_file():
            raise SystemExit(f"FAIL: builder did not create {artifact}")
        artifacts[runtime]=artifact.as_posix()
    manifest={"schema_version":1,"version":a.version,"registry":REGISTRY.relative_to(ROOT).as_posix(),"artifacts":artifacts}
    mp=out/"distribution-build-manifest.json"
    mp.write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
    print(mp); return 0

if __name__=="__main__":
    sys.exit(main())
