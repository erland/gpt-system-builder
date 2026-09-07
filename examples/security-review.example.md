# Security Review – Example ZIP-to-GitHub Service

## Context

Internet-facing service accepts user-provided ZIP files and creates GitHub repositories using delegated credentials.

## Authentication

Users authenticate before repository creation. GitHub credentials are provided through an external integration and are not stored in source code.

## Authorization

Repository creation is enforced server-side. The backend verifies that the authenticated user has permission to invoke the operation.

## Inputs and file handling

Uploaded ZIP files are untrusted.

Controls:
- upload size limit,
- parent traversal rejection,
- absolute path rejection,
- safe temporary extraction directory,
- cleanup after processing,
- no execution of uploaded content.

## Secrets and configuration

GitHub credentials and database credentials are externalized through environment/platform secrets. `.env` values with real credentials are not committed.

## Sensitive data

Application logs must not contain GitHub tokens or database passwords. Project contents are transient unless explicitly persisted.

## Integrations

GitHub API access uses minimum required scopes. Integration errors return safe user messages and detailed internal diagnostics without secrets.

## Database

If PostgreSQL is used, it is external to the application image and accessed with a least-privilege application account.

## Logging and errors

Use operation IDs. Do not return stack traces to users. Redact credentials.

## Container / deployment

- multi-stage image,
- non-root runtime where practical,
- no embedded database,
- platform-managed TLS/reverse proxy,
- health endpoint exposed.

## Security verification

- TEST-001 rejects parent traversal ZIP.
- unauthorized repository creation request is denied.
- automated check ensures known secret fixtures do not appear in logs.
- container runtime user is verified.

## Blockers

None for baseline implementation. A public production deployment requires the GitHub auth flow and rate/abuse behavior to be verified end-to-end.

## Specialist review needed

No for the current small/medium scope. Reassess if multi-tenancy, sensitive persisted project contents or privileged organization-wide GitHub permissions are introduced.
