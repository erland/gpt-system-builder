# Risk and Feasibility – Example ZIP-to-GitHub Service

## Assumptions

- GitHub API access is available through an authenticated integration.
- Target deployments can run a stateless Docker container.
- PostgreSQL is external if application state must be persisted.

## Risks

### RISK-001 – Unsafe ZIP paths

**Category:** security  
**Probability:** medium  
**Impact:** high  
**Level:** high  
**Status:** mitigated

**Risk / assumption**

Uploaded archives can contain parent traversal or absolute paths.

**Evidence / trigger**

ZIP entries are user-controlled.

**Handling**

Validate all archive entries before extraction and cover with dedicated tests.

**Related requirements / steps**

- NFR-001
- DEV-002

### RISK-002 – GitHub upload approach may hit practical API limits

**Category:** integration  
**Probability:** medium  
**Impact:** high  
**Level:** high  
**Status:** open

**Risk / assumption**

The initially selected upload strategy may be too slow or rate-limit heavy for larger project ZIPs.

**Evidence / trigger**

Repository size and number of files vary significantly.

**Handling**

Run a bounded feasibility spike before expanding the full integration flow.

**Related requirements / steps**

- FR-003
- DEV-003

### RISK-003 – Persistent local files would conflict with stateless deployment

**Category:** deployment  
**Probability:** low  
**Impact:** high  
**Level:** medium  
**Status:** mitigated

**Risk / assumption**

Writing durable application data to local container filesystem would make replacement/restart unsafe.

**Evidence / trigger**

Target profile declares stateless runtime.

**Handling**

Use database/external storage for persistent state; local files remain temporary only.

**Related requirements / steps**

- DEV-004

## Feasibility questions

1. Can the selected GitHub API strategy upload representative repositories within acceptable operational limits?
2. Can all required persistent state live outside the application container?

## Spikes / PoCs

### DEV-003A – GitHub upload feasibility spike

**Question:** Can representative project ZIPs be uploaded reliably using the selected API approach?

**Evidence:**
- small repository upload,
- representative larger repository upload,
- failure/rate-limit observations.

**Exit:** Accept the approach, replace it, or revise the architecture and plan.

## Blocking issues

RISK-002 blocks scaling the GitHub integration implementation beyond the minimal proof until the spike produces evidence.

## Accepted risks

None.

## Review outcome

Proceed with safe ZIP implementation immediately. Resolve RISK-002 before broad GitHub upload implementation.
