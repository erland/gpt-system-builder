#!/usr/bin/env python3
from pathlib import Path
import subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
CASES=[
 ('schemas/project.schema.json','examples/project.example.yaml',0),
 ('schemas/work-status.schema.json','examples/work-status.example.yaml',0),
 ('schemas/project.schema.json','tests/invalid-project.yaml',1),
 ('schemas/work-status.schema.json','tests/invalid-work-status.yaml',1),
]
failed=[]
for schema,instance,expected in CASES:
    cp=subprocess.run([sys.executable,str(ROOT/'scripts/validate_yaml_schema.py'),'--schema',str(ROOT/schema),'--instance',str(ROOT/instance)],capture_output=True,text=True)
    ok=(cp.returncode==expected)
    print(('PASS' if ok else 'FAIL'), instance, f'expected={expected} actual={cp.returncode}')
    if not ok:
        print(cp.stdout,cp.stderr)
        failed.append(instance)
raise SystemExit(1 if failed else 0)
