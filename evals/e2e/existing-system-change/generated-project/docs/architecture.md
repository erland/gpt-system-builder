# Architecture – Counter Service

## Current structure
A dependency-free Python package with pure functions.

## Components
- `counter_service.counter`: counter operations.

## Data
No persistence.

## Change impact
FR-003 adds one pure function in the existing module. No deployment, data, security or integration impact.

## Decision
Keep the existing module; no new abstraction is justified for this bounded change.
