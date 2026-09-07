#!/usr/bin/env python3
from pathlib import Path
import argparse,subprocess,yaml,zipfile,hashlib,json,sys,re,shutil

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--scenario-root",required=True)
    a=ap.parse_args()
    base=Path(a.scenario_root)
    p=base/"generated-project"
    errs=[]

    # app tests
    t=subprocess.run([sys.executable,"-m","unittest","discover","-s","tests","-v"],cwd=p,capture_output=True,text=True)
    if t.returncode != 0:
        errs.append("app static tests failed")

    docker=(p/"Dockerfile").read_text(encoding="utf-8")
    if "FROM python:3.12-slim-bookworm" not in docker:
        errs.append("Docker base image not explicit")
    if "USER appuser" not in docker:
        errs.append("non-root USER missing")
    if 'EXPOSE 8080' not in docker:
        errs.append("internal port missing")
    if "postgresql" in docker.lower():
        errs.append("PostgreSQL must not be embedded in app image")
    if "PASSWORD" in docker or "TOKEN" in docker or "SECRET" in docker:
        errs.append("secret-like value declared in Dockerfile")
    if not (p/".dockerignore").exists():
        errs.append(".dockerignore missing")

    prof=yaml.safe_load((p/".system-builder/deployment-profile.yaml").read_text(encoding="utf-8"))
    if prof.get("profile")!="coolify-external-postgresql":
        errs.append("wrong deployment profile")
    if prof.get("database",{}).get("mode")!="external":
        errs.append("PostgreSQL must be external")
    if prof.get("database",{}).get("public_exposure") is not False:
        errs.append("DB should not be public by default")
    if prof.get("platform",{}).get("reverse_proxy_owner")!="Coolify":
        errs.append("Coolify must own reverse proxy")
    if prof.get("platform",{}).get("tls_owner")!="Coolify":
        errs.append("Coolify must own TLS")
    if prof.get("live_verification")!="pending":
        errs.append("live verification must be pending without live target")

    # Existing canonical validators where applicable.
    validator_results={}
    checks=[
        ("docker", [sys.executable, str(Path(__file__).resolve().parent/"validate_docker_baseline.py"), str(p/"Dockerfile"), "--dockerignore", str(p/".dockerignore")]),
        ("operational_configuration",[sys.executable,str(Path(__file__).resolve().parent/"validate_operational_docs.py"),"configuration",str(p/"docs"/"configuration.md")]),
        ("operational_installation",[sys.executable,str(Path(__file__).resolve().parent/"validate_operational_docs.py"),"installation",str(p/"docs"/"installation.md")]),
        ("operational_operations",[sys.executable,str(Path(__file__).resolve().parent/"validate_operational_docs.py"),"operations",str(p/"docs"/"operations.md")]),
    ]
    for name,cmd in checks:
        r=subprocess.run(cmd,cwd=Path(__file__).resolve().parents[1],capture_output=True,text=True)
        validator_results[name]="pass" if r.returncode==0 else "fail"
        if r.returncode!=0:
            errs.append(f"{name} validator failed: {r.stdout.strip()}")

    docker_runtime_available=shutil.which("docker") is not None
    runtime_build="not_run"
    if docker_runtime_available:
        # We intentionally do not require daemon access here; test only if info succeeds.
        info=subprocess.run(["docker","info"],capture_output=True,text=True)
        if info.returncode==0:
            build=subprocess.run(["docker","build","-t","system-builder-e2e-coolify:local","."],cwd=p,capture_output=True,text=True)
            runtime_build="pass" if build.returncode==0 else "fail"
            if build.returncode!=0:
                errs.append("actual Docker build failed")
        else:
            runtime_build="pending_no_daemon"

    out=base/"docker-coolify-fixture.zip"
    with zipfile.ZipFile(out,"w",zipfile.ZIP_DEFLATED) as z:
        for f in sorted(p.rglob("*")):
            if f.is_file() and "__pycache__" not in f.parts:
                z.write(f,f.relative_to(p).as_posix())
    with zipfile.ZipFile(out) as z:
        if z.testzip():
            errs.append("fixture ZIP corrupt")

    result={
        "result":"PASS" if not errs else "FAIL",
        "app_tests":"PASS" if t.returncode==0 else "FAIL",
        "validators":validator_results,
        "docker_runtime_available":docker_runtime_available,
        "docker_build":runtime_build,
        "live_coolify":"pending",
        "zip_sha256":hashlib.sha256(out.read_bytes()).hexdigest(),
        "errors":errs,
    }
    print(json.dumps(result,indent=2))
    return 0 if not errs else 1

if __name__=="__main__":
    sys.exit(main())
