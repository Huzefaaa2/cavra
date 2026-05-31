# Final Closeout Trial Sample Evidence

The sample evidence package at `examples/demos/final-closeout-trial/sample-evidence-package.json` demonstrates the public-safe metadata a customer can inspect during a final closeout trial.

## Package Contents

| Section | Purpose |
| --- | --- |
| `scenario` | Identifies the synthetic trial scenario and edition boundary. |
| `final_readiness_bundle` | Shows final readiness, approval, packet, auditor, archive, and alert references. |
| `signed_archive_manifest` | Shows external signature metadata without private signing keys. |
| `release_closeout_summary` | Shows the closed release state and blocker count. |
| `retention_review` | Shows retention request and approval decision metadata. |
| `closeout_artifact_bundle` | Shows downloadable bundle metadata and file hashes. |
| `retention_health_report` | Shows retention health checks and severity. |
| `retention_alert_delivery` | Shows redacted alert delivery metadata. |
| `closeout_retry_plan` | Shows a retry decision for a simulated failed delivery. |
| `retry_worker_run` | Shows dry-run worker evidence before live redelivery. |
| `release_decision` | Shows how the sample maps to release criteria. |

## How To Use The Sample

1. Open the JSON file in the repository.
2. Compare each section with `docs/release-governance-final-closeout-release-criteria.md`.
3. Confirm all identifiers are synthetic.
4. Confirm no connector credentials, signing keys, license secrets, archive write controls, or customer-specific records are present.
5. Use the package to drive the customer walkthrough in `docs/enterprise/final-closeout-trial-walkthrough.md`.

## Expected Trial Decision

The sample is designed to classify as `ready_with_accepted_risk`: release closeout is closed and retention is approved, but one simulated connector delivery failed and has a retry plan plus dry-run worker evidence.

## Open-Core Boundary

Community Edition can display and validate this evidence shape. Enterprise or SaaS should later provide authenticated connector execution, private archive operations, tenant dashboards, paid policy packs, SSO/RBAC enforcement, and commercial license validation.

