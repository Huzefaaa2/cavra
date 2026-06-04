# Community GA Release Packet Template

This template turns the Community GA release checklist into a repeatable
evidence packet. Use it for every public Community Edition GA release PR so a
maintainer, user, security reviewer, or auditor can verify what was released,
which checks passed, which risks were accepted, and which documentation was
synced.

The packet is public-safe by design. Do not include Enterprise source code,
customer evidence, license-service secrets, private signing keys, private policy
packs, private container credentials, or customer-specific deployment records.

## Packet Files

Each release should attach or commit the following public-safe files:

| File | Purpose |
| --- | --- |
| `community-ga-release-packet.md` | Human-readable release decision and evidence summary. |
| `community-ga-release-packet.json` | Machine-readable packet for automation and audit indexing. |
| `community-ga-release-packet.schema.json` | JSON schema for validating packet structure. |

The public schema is maintained in
`docs/release-packets/community-ga-release-packet.schema.json`. A safe example
packet is maintained in
`examples/release-packets/community-ga-release-packet.example.json`.

## Markdown Template

````markdown
# CAVRA Community GA Release Packet

Release: <version-or-release-name>
Packet ID: <community-ga-YYYYMMDD-or-release-id>
Release State: <ready_for_community_ga|ready_with_accepted_risk|blocked>
Prepared By: <release-agent-or-maintainer>
Approved By: <maintainer>
Prepared At: <ISO-8601 timestamp>

## Scope

- Edition: Community
- Public repository: Huzefaaa2/cavra
- Release branch:
- Release PR:
- Release commit:
- Release tag:
- Wiki sync commit:

## Required Gate Results

| Gate | Status | Evidence Reference | Owner | Notes |
| --- | --- | --- | --- | --- |
| Public boundary | <pass/fail/warn> | <command, check, or artifact link> | <owner> | <summary> |
| Policy signing | <pass/fail/warn> | <verification output or artifact> | <owner> | <summary> |
| Policy validation | <pass/fail/warn> | <command/check link> | <owner> | <summary> |
| Runtime modes | <pass/fail/warn> | <command/check link> | <owner> | <summary> |
| Golden decisions | <pass/fail/warn> | <test/check link> | <owner> | <summary> |
| Evidence Console | <pass/fail/warn> | <smoke result or screenshot link> | <owner> | <summary> |
| Deployment validation | <pass/fail/warn> | <readiness report link> | <owner> | <summary> |
| Go runtime readiness | <pass/fail/warn/disabled> | <readiness report or disabled output> | <owner> | <summary> |
| Documentation | <pass/fail/warn> | <README/docs/wiki commit> | <owner> | <summary> |
| CI evidence | <pass/fail/warn> | <GitHub checks link> | <owner> | <summary> |

## Validation Commands

```bash
scripts/validate-boundaries.sh
python3 -m ruff check src tests
python3 -m pytest -q
git diff --check
```

Add any release-specific policy signing, policy compile, runtime mode, Evidence
Console, deployment readiness, or Go backend readiness commands here.

## Accepted Risks

| Risk | Severity | Owner | Expiry | Compensating Control | Decision |
| --- | --- | --- | --- | --- | --- |
| <risk> | <low/medium/high> | <owner> | <date> | <control> | <accepted/rejected> |

Use `None` if there are no accepted risks. A `ready_for_community_ga` packet
should normally have no accepted risks.

## Public Boundary Review

- Enterprise code present in public repo: <yes/no>
- Secrets present in public repo: <yes/no>
- Customer material present in public repo: <yes/no>
- Private policy packs present in public repo: <yes/no>
- Boundary validation result:

## Release Decision

Decision: <approve/block/defer>
Decision rationale:

## Follow-Up Work

- <next recommendation or release follow-up>
````

## JSON Packet Requirements

The JSON packet should mirror the Markdown packet and include release identity,
repository references, gate results for every Community GA release checklist
gate, validation commands, accepted risks, public boundary review flags, final
decision, and next recommended work.

## Release State Rules

`ready_for_community_ga` is allowed only when all required gates pass and there
are no unresolved high-severity accepted risks.

`ready_with_accepted_risk` is allowed when release blockers are absent, any
remaining warnings have owners and expiry dates, and compensating controls are
documented.

`blocked` is required when public boundary validation fails, required tests fail,
policy signing cannot be verified, runtime modes are ambiguous, documentation is
not synced, or Go promotion is requested without required readiness evidence.

## Next Recommendation

Continue with automated JSON schema validation for Community GA release packets
in CI.
