# CREATE Work Initiation – Example

## Need

Create a small web service that accepts a local project ZIP and creates a GitHub repository.

## Users / actors

- authenticated user,
- GitHub as external system.

## Goals

- eliminate manual repository setup,
- preserve project files correctly,
- give user a clear repository URL.

## Success criteria

- valid project ZIP creates repository,
- unsafe ZIP is rejected,
- container can run in target environment.

## Scope

### Must
- upload ZIP,
- validate archive,
- create GitHub repository,
- upload contents,
- return link.

### Should
- choose repository visibility.

### Could
- infer repository name.

### Out of scope
- automatic production deployment,
- multi-tenancy.

## Constraints

- deployment should support Docker/Coolify,
- PostgreSQL must be external if used.

## Integrations

- GitHub API.

## Data / persistence

Persistent workflow history is optional in first release.

## Deployment target

Docker-compatible platform, with Coolify as primary deployment profile.

## Security considerations

- user-controlled archive,
- delegated GitHub credentials,
- no secrets in image or logs.

## Blocking questions

- None.

## Complexity

medium

## Next artifact

Functional specification.
