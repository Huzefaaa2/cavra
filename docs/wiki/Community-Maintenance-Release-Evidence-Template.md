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

## JSON Requirements

The JSON packet must validate against
`docs/release-verifications/community-maintenance-release.schema.json` and
include all required gate names from the checklist.

## Next Recommendation

Complete enterprise integration validation for GitHub App/orchestrator production hardening, GitLab/Azure DevOps parity, SAML identity readiness, and SIEM/ITSM workflow evidence.
