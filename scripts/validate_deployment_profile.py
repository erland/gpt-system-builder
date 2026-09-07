#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
import json
import sys
import yaml
import jsonschema

def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def semantic_errors(data):
    errors = []
    packaging = data["packaging"]
    target = data["target"]
    runtime = data["runtime"]
    database = data["database"]
    network = data["network"]
    health = data["health"]
    persistence = data.get("persistence", {"application_files": "none", "volumes": []})

    if target["platform"] in {"coolify", "kubernetes", "generic_container_platform"}:
        if packaging["type"] not in {"docker", "oci"}:
            errors.append(f"{target['platform']} requires docker/oci packaging")

    if target["platform"] == "coolify":
        if database["type"] == "postgresql" and database["deployment"] != "external":
            errors.append("Coolify PostgreSQL profile must use external database deployment")
        if network["reverse_proxy"] != "platform":
            errors.append("Coolify profile should use platform reverse proxy")
        if network["tls"] != "platform":
            errors.append("Coolify profile should use platform TLS")

    if database["type"] == "none" and database["deployment"] != "none":
        errors.append("database deployment must be none when database type is none")

    if database["type"] != "none" and database["deployment"] == "none":
        errors.append("non-empty database type requires a deployment mode")

    if runtime["stateless"] and persistence.get("application_files") == "volume":
        # Not always invalid, but a stateless declaration with app-managed persistent files is contradictory.
        errors.append("stateless runtime cannot declare application_files=volume")

    if health["enabled"]:
        if not any([
            health.get("liveness_endpoint"),
            health.get("readiness_endpoint"),
            health.get("startup_endpoint")
        ]):
            errors.append("health enabled requires at least one health endpoint")
    else:
        if any([
            health.get("liveness_endpoint"),
            health.get("readiness_endpoint"),
            health.get("startup_endpoint")
        ]):
            errors.append("health endpoints must be null/absent when health is disabled")

    if network["tls"] == "platform" and network["reverse_proxy"] == "none":
        errors.append("platform TLS requires a platform/external reverse proxy path")

    return errors

def validate(data, schema):
    jsonschema.Draft202012Validator(schema).validate(data)
    errors = semantic_errors(data)
    if errors:
        raise ValueError("\n".join(errors))

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--file", required=True)
    p.add_argument("--schema", required=True)
    p.add_argument("--expect-invalid", action="store_true")
    args = p.parse_args()

    try:
        validate(load_yaml(Path(args.file)), load_json(Path(args.schema)))
        valid = True
        detail = ""
    except Exception as e:
        valid = False
        detail = str(e)

    if args.expect_invalid:
        if valid:
            print("FAIL: expected invalid profile but validation passed")
            return 1
        print("PASS: invalid deployment profile rejected")
        return 0

    if not valid:
        print("FAIL:", detail)
        return 1

    print("PASS: deployment profile valid")
    return 0

if __name__ == "__main__":
    sys.exit(main())
