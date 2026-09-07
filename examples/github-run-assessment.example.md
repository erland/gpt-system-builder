# GitHub Run Assessment – Example

## Repository

- owner/repo: example/project
- default branch: main
- work branch: system-builder/cr-014-repository-visibility

## Active work series

- mode: CHANGE
- identifier: CR-014
- scope: add repository visibility selection

## Pull request

- number: 42
- state: open
- reuse: yes

## State discovery

- AGENTS.md: present
- work-status.yaml: present
- development plan: present
- functional spec: present
- architecture: present

## Drift / baseline

- branch drift: none detected
- base drift: main has no conflicting relevant changes
- CI baseline: pass

## Selected action

- DEV-004 – Add visibility selector to UI.

## Required verification

- frontend typecheck,
- component/API integration test,
- regression for default private behavior.

## Commit plan

- message: DEV-004: add repository visibility selector
- push branch: system-builder/cr-014-repository-visibility

## PR update

- title: CR-014: Add repository visibility selection
- summary update: mark DEV-004 completed and DEV-005 next.

## Stop condition

Stop after one verified step is committed/pushed and state/PR are updated.
