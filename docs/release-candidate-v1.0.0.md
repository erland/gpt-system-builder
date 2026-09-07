# System Builder v1.0.0 Release Candidate

Version: `1.0.0-rc.1`
Planned tag: `v1.0.0-rc.1`

## Final hygiene cleanup

Removed or normalized before packaging:

- `release-smoke`
- `dist-smoke`
- `final-readiness-artifacts`
- `_chat_runtime`
- `_custom_gpt_runtime -> runtime/custom-gpt-source`

`runtime/custom-gpt-source/` is intentionally retained because it is the canonical source for the Custom GPT distribution.

Generated release ZIPs are intentionally **not** embedded in the source project ZIP. They are built and delivered separately.

## Release artifacts

- `system-builder-chat-1.0.0-rc.1.zip`
- `system-builder-custom-gpt-1.0.0-rc.1.zip`
- `SHA256SUMS.txt`
- `release-metadata.yaml`

## Verification

- Chat ZIP build/validation: PASS
- Custom GPT build/validation: PASS
- Static instruction adherence: PASS
- Runtime parity: PASS
- Source project ZIP integrity: PASS

## Readiness

**READY_WITH_WARNINGS**

Only warning: live Coolify target verification remains pending because no live target was available. It is not reported as PASS.

All planned steps SB-01 through SB-41 are complete.
