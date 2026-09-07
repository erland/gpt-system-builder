#!/usr/bin/env python3
from pathlib import Path
import argparse, json, sys, yaml
from jsonschema import Draft202012Validator

def validate(schema_path, instance_path):
    schema=json.loads(Path(schema_path).read_text(encoding="utf-8"))
    instance=yaml.safe_load(Path(instance_path).read_text(encoding="utf-8"))
    errors=sorted(Draft202012Validator(schema).iter_errors(instance), key=lambda e:list(e.path))
    if errors:
        for e in errors:
            loc='.'.join(map(str,e.path)) or '<root>'
            print(f"{instance_path}: {loc}: {e.message}")
        return False
    print(f"PASS {instance_path}")
    return True

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--schema', required=True)
    p.add_argument('--instance', required=True)
    args=p.parse_args()
    raise SystemExit(0 if validate(args.schema,args.instance) else 1)

if __name__=='__main__':
    main()
