# Go Backend Rollback Drill Auditor Export Retry and Archive Health

CAVRA now plans retries for failed final auditor export delivery and checks archive custody health for verified rollback drill auditor exports.

## Feature Details

- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-auditor-export/delivery-retry-plan` classifies failed auditor export deliveries into `retry`, `wait`, or `suppress` decisions.
- `GET /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-archive-reference-health` reports verified auditor exports that are missing immutable archive references, retention timestamps, or archive hashes.
- Evidence Console now includes **Plan Auditor Retry** and **Archive Health** controls.
- Dashboard metrics show auditor delivery retry plans, retryable auditor deliveries, archive health reports, and archive health alerts.
- Community Edition still performs no private connector redelivery or archive write operation. It records public-safe plans and health evidence only.

## How To Use

1. Generate and deliver the final auditor export.
2. Run **Plan Auditor Retry** after failed delivery evidence appears.
3. Capture immutable archive references after the export is stored externally.
4. Run **Archive Health** to verify that each verified export has an archive reference.
5. Use detail drill-downs to inspect retry decisions and archive custody alerts.

```http
POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-auditor-export/delivery-retry-plan
GET  /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-archive-reference-health
```

Retry plan request fields:

- `generated_by`: public-safe actor label.
- `retry_policy.max_retry_attempts`: maximum failed delivery attempts before suppression.
- `retry_policy.retry_delay_minutes`: delay before a failed delivery is eligible.
- `retry_policy.allow_immediate_retry`: allows zero-minute retry delay.
- `retry_policy.backoff_multiplier`: multiplier applied after repeated failures.

Archive health query parameters:

- `generated_by`: public-safe actor label.
- `require_archive_hash`: defaults to true.
- `require_retention_until`: defaults to true.
- `persist`: defaults to true; set false to preview without storing metadata.

## Evidence Metadata

- `go-backend-rollback-drill-acknowledgement-audit-delivery-final-reporting-auditor-export-delivery-retry-plan`
- `go-backend-rollback-drill-acknowledgement-audit-delivery-final-reporting-archive-reference-health`

Dashboard fields:

- `acknowledgement_audit_delivery_final_reporting_auditor_export_delivery_retry_plan_count`
- `acknowledgement_audit_delivery_final_reporting_auditor_export_delivery_retryable_count`
- `acknowledgement_audit_delivery_final_reporting_archive_reference_health_count`
- `acknowledgement_audit_delivery_final_reporting_archive_reference_health_alert_count`

## User Stories

- As a release manager, I can see which failed final auditor export deliveries are safe to retry.
- As an auditor, I can verify that final auditor exports are represented in immutable archive references.
- As a platform operator, I can identify archive custody gaps without exposing storage credentials or private endpoints.

## Enterprise Challenge Solved

Final release audit evidence is not complete until failed delivery paths are visible and archive custody is checked. This phase makes delivery retry posture and archive completeness measurable in Community Edition while keeping private connector execution and storage writes in Enterprise or operator-owned systems.

## Diagram

See `docs/diagrams/go-backend-rollback-drill-auditor-export-retry-archive-health.svg`.

## Next Recommended Work

Completed in the next slice: final auditor export retry worker execution records and archive health alert delivery acknowledgements. See `docs/go-backend-rollback-drill-auditor-export-retry-worker-archive-alert-acks.md`.
