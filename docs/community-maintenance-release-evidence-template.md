# Community Maintenance Release Evidence Template

Use this template for every public CAVRA Community maintenance release after
Community GA v0.1.0.

The packet is public-safe by design. Do not include Enterprise source code,
trial package internals, paid policy packs, SaaS backend implementation,
license-service secrets, customer data, private keys, private registry tokens,
or private deployment evidence.

## Packet Files

| File | Purpose |
| --- | --- |
| `docs/release-verifications/community-vX.Y.Z-maintenance-verification.md` | Human-readable release verification and approval summary. |
| `docs/release-verifications/community-vX.Y.Z-maintenance-verification.json` | Machine-readable maintenance-release evidence packet. |
| `docs/releases/community-vX.Y.Z.md` | Public release notes. |

## Markdown Template

````markdown
# Community vX.Y.Z Maintenance Release Verification

Release: CAVRA Community vX.Y.Z
Release State: <ready_for_publication|ready_with_accepted_risk|blocked>
Prepared By: <release-agent-or-maintainer>
Prepared At: <ISO-8601 timestamp>

## Scope

- Edition: Community
- Release tag: `community-vX.Y.Z`
- GitHub Release:
- Release notes:
- Verification workflow run:
- Wiki sync commit:

## Required Gate Results

| Gate | Status | Evidence Reference | Owner | Notes |
| --- | --- | --- | --- | --- |
| Release notes | <pass/fail/warn> | <path or URL> | <owner> | <summary> |
| Changelog | <pass/fail/warn> | <path or commit> | <owner> | <summary> |
| README link | <pass/fail/warn> | <path or commit> | <owner> | <summary> |
| Wiki link | <pass/fail/warn> | <page or commit> | <owner> | <summary> |
| Verification workflow | <pass/fail/warn> | <workflow run URL> | <owner> | <summary> |
| Artifact checksums | <pass/fail/warn> | <verification packet> | <owner> | <summary> |
| Install smoke | <pass/fail/warn> | <command output> | <owner> | <summary> |
| Public boundary | <pass/fail/warn> | <command output> | <owner> | <summary> |
| CI evidence | <pass/fail/warn> | <checks URL> | <owner> | <summary> |

## Validation Commands

```bash
python3 scripts/validate-maintenance-release-evidence.py
python3 scripts/validate-release-packets.py
bash scripts/validate-boundaries.sh .
python3 -m pytest -q
```

## Accepted Risks

Use `None` when there are no accepted risks.

| Risk | Severity | Owner | Expiry | Compensating Control | Decision |
| --- | --- | --- | --- | --- | --- |
| <risk> | <low/medium/high> | <owner> | <date> | <control> | <accepted/rejected> |

## Public Boundary Review

- Enterprise source included: <yes/no>
- Paid policy packs included: <yes/no>
- Customer records included: <yes/no>
- Private keys included: <yes/no>
- Private registry credentials included: <yes/no>

## Decision

Decision: <approve/block/defer>
Rationale:

## Next Recommendation

<next maintenance release follow-up>
````

## JSON Requirements

The JSON packet must validate against
`docs/release-verifications/community-maintenance-release.schema.json` and
include all required gate names from the checklist.

## Next Recommendation

Harden the Go enforcement plane production path for Unix-socket/gRPC interface completion, air-gapped packaging, reproducibility, upgrade validation, performance, and operational readiness evidence.
