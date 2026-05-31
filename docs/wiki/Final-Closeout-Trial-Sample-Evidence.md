# Final Closeout Trial Sample Evidence

The sample evidence package at `examples/demos/final-closeout-trial/sample-evidence-package.json` demonstrates the public-safe metadata a customer can inspect during a final closeout trial.

## Package Sections

| Section | Purpose |
| --- | --- |
| `scenario` | Synthetic trial context and edition boundary. |
| `final_readiness_bundle` | Readiness, approval, packet, auditor, archive, and alert references. |
| `signed_archive_manifest` | External signature metadata without private signing keys. |
| `release_closeout_summary` | Closed release state and blocker count. |
| `retention_review` | Retention request and approval decision metadata. |
| `closeout_artifact_bundle` | Downloadable bundle metadata and file hashes. |
| `retention_health_report` | Retention health checks and severity. |
| `retention_alert_delivery` | Redacted alert delivery metadata. |
| `closeout_retry_plan` | Retry decision for a simulated failed delivery. |
| `retry_worker_run` | Dry-run worker evidence before live redelivery. |
| `release_decision` | Release-criteria classification. |

## Expected Trial Decision

The sample is designed to classify as `ready_with_accepted_risk`: release closeout is closed and retention is approved, but one simulated connector delivery failed and has a retry plan plus dry-run worker evidence.

## Open-Core Boundary

Community Edition can display and validate this evidence shape. Enterprise or SaaS should later provide authenticated connector execution, private archive operations, tenant dashboards, paid policy packs, SSO/RBAC enforcement, and commercial license validation.

