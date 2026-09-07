# ADR-001 – Use a modular monolith for the first release

**Status:** Accepted  
**Date:** 2026-09-07

## Context
The first release is maintained by a small team and deployed as one containerized application.

## Decision
Use a modular monolith with explicit internal module boundaries.

## Alternatives considered
Microservices and an unstructured monolith.

## Rationale
This keeps deployment simple while preserving clear internal boundaries.

## Consequences
Simpler operations, but modules cannot scale independently.

## References
- `docs/architecture.md`

## Supersedes
- None.

## Superseded by
- None.
