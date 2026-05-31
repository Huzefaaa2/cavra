# Release Governance Final Closeout Release Criteria

These criteria define when the final closeout workflow is acceptable for Community Edition release governance, Enterprise trial demonstrations, and future SaaS onboarding. They are intentionally public-safe and do not include Enterprise implementation details.

## Required Criteria

| Criterion | Required Evidence | Pass Condition |
| --- | --- | --- |
| Final readiness | Final readiness bundle | Bundle exists and references readiness, approval, packet, auditor, archive, and alert evidence. |
| Signed archive manifest | Signed archive manifest metadata | Signature state is externally attached and no private signing key is stored. |
| Release closeout | Release closeout summary | `closeout_state` is `closed` and blocker count is zero. |
| Closeout delivery | Redacted connector delivery metadata | Delivery succeeded, or a retry plan and reviewed retry worker exist. |
| Retention approval | Retention review decision | Decision state is `approved`. |
| Artifact bundle | Closeout artifact bundle | Bundle exists, file hashes are present, and retention decision state is approved. |
| Retention health | Closeout retention health report | Health is healthy, or warnings/critical findings have documented owner acceptance. |
| Retention alerts | Alert plan and delivery metadata | Required alert providers were selected and delivery result is recorded. |
| Retry workflow | Retry plan, worker run, execution record | Failed closeout deliveries have retry decisions and worker evidence. |
| Documentation | README, docs, wiki | Release docs link the operator runbook, release criteria, and trial guidance. |

## Release States

`ready_for_release`: all required criteria pass.

`ready_with_accepted_risk`: non-critical warnings or retryable delivery failures are documented with an owner, external reference, and target resolution date.

`blocked`: closeout is open, retention is not approved, retention is expired, artifact bundle is missing, or failed delivery has no retry plan.

## Acceptance Checklist

- [ ] Final readiness bundle exists.
- [ ] Signed archive manifest references external signing authority.
- [ ] Release closeout summary is closed.
- [ ] Closeout delivery result is recorded.
- [ ] Retention review decision is approved.
- [ ] Closeout artifact bundle is downloadable.
- [ ] Retention health report exists.
- [ ] Retention health alerts were delivered or intentionally suppressed with reason.
- [ ] Failed closeout deliveries have retry plans.
- [ ] Retry worker was run in dry-run mode before live redelivery.
- [ ] Live retry, if used, was executed through an approved connector path.
- [ ] Final release decision is linked to the release record or audit case.

## Trial Acceptance

A trial can be marked successful when a customer can:

- see the full evidence chain in the Evidence Console,
- run the final closeout health check,
- understand which findings are Community metadata,
- understand which actions require Enterprise or operator-owned enforcement,
- receive a sample retention alert through a configured non-production connector,
- review a failed delivery retry plan without exposing connector secrets.

## Enterprise Acceptance

Enterprise readiness requires private implementation outside this repository for:

- license validation,
- authenticated connector delivery,
- SSO/RBAC policy enforcement,
- private archive mutation and retention enforcement,
- paid policy packs,
- organization dashboards,
- customer-specific templates.

## Exception Handling

Exceptions must include:

- owner,
- external change or risk reference,
- affected release or trial,
- reason,
- expiry date,
- compensating control,
- evidence refs proving the exception was reviewed.

## Next Recommended Issue

Delivered in enterprise/final-closeout-trial-walkthrough.md, enterprise/final-closeout-trial-sample-evidence.md, enterprise/final-closeout-sales-engineering-demo.md, and examples/demos/final-closeout-trial/sample-evidence-package.json. Continue by converting the onboarding package into an interactive public sandbox flow.
