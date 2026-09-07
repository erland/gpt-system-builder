# Product decisions

## PD-001 – Multi-tenancy is excluded from the first release

**Status:** Accepted  
**Date:** 2026-09-07

### Context
Initial users operate within one organization.

### Decision
Do not include organization-level multi-tenancy in the first release.

### Rationale
It would add authorization and data-ownership complexity before there is a validated need.

### Consequences
A future multi-tenancy change requires dedicated analysis.

### Affected requirements / use cases
- FR-001

### Supersedes
- None.

### Superseded by
- None.
