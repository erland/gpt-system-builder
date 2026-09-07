# Architecture – Tiny Status API

## Goals
Keep the first release dependency-free and easy to test.

## System context
A local client calls the service over HTTP.

## Components and responsibilities
- `tiny_status.app`: pure response logic.
- planned HTTP adapter: Python standard library server.
- `STATUS_MESSAGE`: runtime configuration.

## Data flow
Health → pure static response.
Message → environment lookup → JSON response.

## Data model and persistence
No persistent data.

## Security
Local-only first release; no request bodies or credentials.

## Deployment
Local Python process. Containerization intentionally deferred.

## Key choices and tradeoffs
Use standard library and pure functions first; add HTTP adapter in DEV-002.
