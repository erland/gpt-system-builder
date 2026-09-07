#!/usr/bin/env python3
from pathlib import Path
import argparse,zipfile,sys
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--source-dir",required=True); ap.add_argument("--output",required=True); a=ap.parse_args()
    src=Path(a.source_dir); out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True)
    for r in ["README.md","instructions.txt","custom-gpt.yaml"]:
        if not (src/r).exists(): raise FileNotFoundError(r)
    with zipfile.ZipFile(out,"w",zipfile.ZIP_DEFLATED) as z:
        for p in sorted(src.rglob("*")):
            if p.is_file(): z.write(p,p.relative_to(src).as_posix())
    print(out); return 0
if __name__=="__main__": sys.exit(main())
