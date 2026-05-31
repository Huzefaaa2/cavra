# Release Governance Final Closeout Release Criteria

These criteria define when the final closeout workflow is acceptable for Community release governance, Enterprise trial demonstrations, and future SaaS onboarding.

## Required Criteria

| Criterion | Pass Condition |
| --- | --- |
| Final readiness | Bundle exists and references readiness, approval, packet, auditor, archive, and alert evidence. |
| Signed archive manifest | Signature state is externally attached and no private signing key is stored. |
| Release closeout | `closeout_state` is `closed` and blocker count is zero. |
| Closeout delivery | Delivery succeeded, or a retry plan and reviewed retry worker exist. |
| Retention approval | Decision state is `approved`. |
| Artifact bundle | Bundle exists, file hashes are present, and retention decision state is approved. |
| Retention health | Health is healthy, or findings have owner acceptance. |
| Retry workflow | Failed closeout deliveries have retry decisions and worker evidence. |

## Release States

- `ready_for_release`: all required criteria pass.
- `ready_with_accepted_risk`: warnings or retryable delivery failures have documented owner acceptance.
- `blocked`: closeout is open, retention is not approved, retention is expired, artifact bundle is missing, or failed delivery has no retry plan.

## Trial Acceptance

A trial is successful when the customer can see the evidence chain, run closeout health, understand Community metadata boundaries, and review retry plans without exposing connector secrets or Enterprise source.

## Enterprise Acceptance

Enterprise readiness requires private implementation for license validation, authenticated connector delivery, SSO/RBAC, private archive mutation, paid policy packs, organization dashboards, and customer-specific templates.

## Recommended Next Issue

Add customer onboarding assets for final closeout trials: a trial walkthrough, sample evidence package, and sales-engineering demo script.
