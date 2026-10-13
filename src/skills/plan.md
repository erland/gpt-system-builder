## 6. Functional specification

Functional specification describes **what the system is intended to do**, not how it is implemented. During implementation it is a governing current-intent document, not a progress log.

Use stable identifiers when useful:

- `FR-xxx`
- `NFR-xxx`
- `AC-xxx`

Cover proportionally:

- purpose/goals,
- scope and Must/Should/Could,
- actors/use cases,
- functional requirements,
- business rules,
- information needs,
- integrations,
- authentication/authorization,
- errors/exceptions,
- NFR,
- acceptance criteria,
- out-of-scope,
- open questions.

Canonical standard: `docs/functional-specification-standard.md`.

## 7. Architecture

Architecture describes the **intended** current structure and significant technical choices. During implementation it governs the target structure even when the implementation has not reached that target yet.

Cover proportionally:

- context,
- components/responsibilities,
- data flow/ownership,
- integrations,
- security,
- deployment,
- observability,
- key tradeoffs.

Use ADR only for significant decisions.

Canonical standards:
- `docs/architecture-standard.md`
- `docs/decision-records-standard.md`

## 8. Development plan

Plan implementation as small, verifiable steps, each normally executable in one prompt/run.

Each `DEV-xxx` step should define:

- objective,
- scope,
- prerequisites,
- implementation/touched areas,
- verification,
- done criteria,
- dependencies.

Plan describes **what remains**.
Work status describes **where execution currently is**.

Canonical standard: `docs/development-plan-standard.md`.

## 9. Risk and feasibility

Before risky work, assess:

- technical uncertainty,
- integration risk,
- data/migration risk,
- security,
- deployment/operations,
- performance,
- policy/legal constraints when relevant.

Use a spike/PoC when uncertainty is larger than the implementation itself.

Canonical standard: `docs/risk-feasibility-standard.md`.

## 15. Project complexity

Use adaptive rigor:

- **small** – compressed artifacts, minimal ceremony.
- **medium** – normal separated contracts and verification.
- **large/high-risk** – deeper risk, architecture, traceability and acceptance.

Complexity is based on aggregate risk, integrations, data, security and deployment—not code size alone.

Canonical standard: `docs/project-complexity.md`.

## 28. Questions

Ask only when a real user/business decision cannot be safely derived.

Do not ask about routine internal implementation choices when a sensible default exists.

If the task is large, make a best effort and move the project forward rather than stopping for avoidable clarification.

## 29. Default technical preferences

Unless project context indicates otherwise:

- prefer simple architecture over distributed complexity,
- prefer modular monolith for smaller systems,
- prefer stateless web/API services,
- prefer external PostgreSQL for relational persistence,
- prefer Docker/OCI for container targets,
- use current project tooling rather than introducing unnecessary replacements.

These are defaults, not hard requirements.

