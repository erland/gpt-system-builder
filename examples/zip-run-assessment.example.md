# ZIP Run Assessment – Example

## Input artifact

- filename: example-project-v0.3.0-dev.zip
- checksum: 7f3f7f6f9e1b4a0d8d8f0a0a77f04aa2c59e5c41f19f44ef1111111111111111

## Project root

- root of archive

## Mode

CHANGE

## State discovery

- AGENTS.md: present
- project.yaml: present
- work-status.yaml: present
- development plan: present
- functional spec: present
- architecture: present

## Source drift

none

## Selected action

- DEV-014 – Add repository visibility support.

## Required verification

- API tests,
- regression test for default private behavior,
- build,
- schema validation.

## Output ZIP

- complete project: yes
- exclude transient artifacts: yes

## Delivery evidence

- integrity: pass
- checksum: calculated after packaging
- next recommended: DEV-015
