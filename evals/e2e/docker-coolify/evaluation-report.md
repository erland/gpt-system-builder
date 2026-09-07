# SB-36 Evaluation Report – Docker/Coolify

## Result
**PASS**

## Verified

- App static tests: **PASS**
- Docker baseline validator: **PASS**
- Configuration docs validator: **PASS**
- Installation docs validator: **PASS**
- Operations docs validator: **PASS**
- PostgreSQL external: **PASS**
- DB public exposure default false: **PASS**
- Coolify owns proxy/TLS: **PASS**
- Bind `0.0.0.0:8080`: **PASS**
- Health contract `/health`: **PASS**
- Secrets externalized: **PASS**

## Docker runtime evidence

Docker executable available: `False`

Docker build result: `not_run`

A build is only counted as PASS if an actual Docker daemon build ran successfully.

## Live Coolify verification

**PENDING**

No live Coolify instance is available to this eval, therefore DNS, public HTTPS, proxy routing and live external PostgreSQL connectivity are intentionally not reported as PASS.

## Resume

The fixture recommends a later `DEV-002` for live Coolify deployment verification.

## Artifact

Fixture ZIP SHA-256: `8f9bfb8e9b6c7d74e4735383bf6241bd5da70945a6b2b85f9c06de81d9d83fe1`
