# Community GA Release Checklist

This checklist defines the public Community release path for CAVRA. It ties the
policy engine, runtime modes, Evidence Console, deployment validation, and Go
runtime readiness into one user-verifiable release gate.

## Scope

This checklist applies to public Community Edition releases. It does not
approve Enterprise source code, customer policy packs, SaaS backend services,
license-service internals, customer evidence, private signing services,
production private keys, KMS/HSM integrations, private approval routers, or
paid policy-pack implementation.

## Required Gates

| Gate | Required Evidence | Pass Condition |
| --- | --- | --- |
| Public boundary | `scripts/validate-boundaries.sh` | Public boundary validation passes and no prohibited Enterprise material is committed. |
| Policy signing | `cavra policy keygen`, `policy sign`, `policy verify` | Policy pack is signed with Ed25519 and verified with the matching public key. |
| Runtime modes | `cavra evaluate ... --policy-mode ... --json` | `audit_only`, `enforce`, `strict`, and `break_glass` behavior is explicit and parseable. |
| Golden decisions | `tests/test_golden_decisions.py` | Critical file, command, Git, MCP, and strict-mode decisions match the public fixture. |
| Evidence Console | Hosted sandbox smoke check | Community GA Control Hardening appears in the Evidence Console with docs and command links. |
| Deployment validation | `/deployment/production-readiness` | Production readiness checks are visible and attachable to release evidence. |
| Go runtime readiness | Go parity and readiness checks | Go remains opt-in; Python remains authoritative unless readiness and rollback gates pass. |
| Documentation | README, docs, wiki-source, live wiki | Public documentation and wiki navigation are current for the release. |
| CI evidence | Required GitHub checks | Required checks, public-boundary, and matrix tests pass. |

## Operator Runbook

1. Run `scripts/validate-boundaries.sh`.
2. Run policy validation, compile, diff, Ed25519 signing, and verification.
3. Verify runtime modes through `cavra evaluate ... --policy-mode ... --json`.
4. Run `python3 -m pytest -q tests/test_golden_decisions.py`.
5. Run static Evidence Console syntax and smoke tests.
6. Attach `/deployment/production-readiness` output.
7. Confirm Go backend remains disabled unless opt-in readiness, promotion,
   rollback, rehearsal, and drill evidence pass.
8. Run full local validation and confirm GitHub checks pass.
9. Sync README, docs, wiki-source pages, and the live wiki.

## Release States

`ready_for_community_ga`: all required gates pass.

`ready_with_accepted_risk`: non-critical warnings have an owner, expiry, and
compensating control.

`blocked`: public boundary validation fails, policy signatures do not verify,
golden decisions regress, runtime modes are ambiguous, required checks fail, or
Go promotion is requested without complete readiness and rollback evidence.

## Public Evidence Packet

Use the Community GA release packet template and JSON schema for every public
Community GA release packet.

## Next Recommendation

Continue with automated JSON schema validation for Community GA release packets
in CI.
