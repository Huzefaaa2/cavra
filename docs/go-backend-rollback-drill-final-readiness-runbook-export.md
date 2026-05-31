# Go Backend Rollback Drill Final Readiness And Runbook Export

CAVRA now creates a release-readiness summary and operator runbook export for the completed rollback drill reporting loop.

## What This Adds

- `GET /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-release-readiness` generates a public-safe release-readiness summary.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-operator-runbook-export` generates a public-safe operator runbook export with Markdown content.
- Evidence Console now includes **Release Readiness** and **Export Runbook** actions.
- Rollback drill notification dashboard now counts release readiness summaries and runbook exports.

The summary and runbook export are generated from public-safe metadata only. They do not include connector credentials, private URLs, customer payloads, enterprise source code, license secrets, or SaaS backend implementation.

## Operator Flow

1. Complete rollback drill notification delivery, acknowledgements, recovery escalation, executive reporting, health alert retries, and final closure checks.
2. Open **Release Readiness** to generate and persist a release gate summary.
3. Open **Export Runbook** to generate a Markdown-ready operator runbook export.
4. Attach the readiness summary, runbook export, final closure dashboard, and relevant evidence references to the release record.
5. Keep credential rotation, ticket mutation, and chat side effects in private connectors or operator-owned systems.

## API

```text
GET  /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-release-readiness
POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-operator-runbook-export
```

Readiness query parameters:

- `generated_by`: public-safe actor label.
- `persist`: defaults to true; set false to preview without indexing metadata.

Runbook request fields:

- `generated_by`: public-safe actor label.

## Evidence

New metadata kinds:

- `go-backend-rollback-drill-acknowledgement-audit-delivery-final-reporting-release-readiness-summary`
- `go-backend-rollback-drill-acknowledgement-audit-delivery-final-reporting-operator-runbook-export`

New dashboard fields:

- `acknowledgement_audit_delivery_final_reporting_release_readiness_summary_count`
- `acknowledgement_audit_delivery_final_reporting_release_ready_count`
- `acknowledgement_audit_delivery_final_reporting_operator_runbook_export_count`

## User Stories

- As a release manager, I can see whether the final rollback drill reporting loop is ready for release closure.
- As an auditor, I can inspect the checks and evidence counts used to hold or approve release closure.
- As an operator, I can export a public-safe runbook that explains what evidence to attach and what actions remain private.

## Enterprise Challenge Solved

Enterprise release closure often depends on tribal knowledge and unstructured tickets. This phase turns the final rollback drill reporting loop into a repeatable release gate with an exportable operator runbook, while keeping secrets and enterprise automation outside the public Community repository.

## Diagram

See `docs/diagrams/go-backend-rollback-drill-final-readiness-runbook-export.svg`.

## Next Work

Final reporting release closure packet verification and auditor export are now covered in [Go Backend Rollback Drill Closure Packet Verification and Auditor Export](go-backend-rollback-drill-closure-packet-auditor-export.md).
