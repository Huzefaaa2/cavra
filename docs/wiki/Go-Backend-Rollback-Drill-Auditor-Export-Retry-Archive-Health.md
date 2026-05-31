# Go Backend Rollback Drill Auditor Export Retry and Archive Health

CAVRA now plans retries for failed final auditor export delivery and checks archive custody health for verified rollback drill auditor exports.

## Feature Details

- Added final auditor export delivery retry plans.
- Added archive reference health reports for verified auditor exports.
- Added Evidence Console **Plan Auditor Retry** and **Archive Health** controls.
- Added dashboard metrics for retry plan count, retryable auditor deliveries, archive health report count, and archive health alert count.
- Kept private connector redelivery and archive write operations outside Community Edition.

## API

```http
POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-auditor-export/delivery-retry-plan
GET  /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-archive-reference-health
```

## Evidence Metadata

- `go-backend-rollback-drill-acknowledgement-audit-delivery-final-reporting-auditor-export-delivery-retry-plan`
- `go-backend-rollback-drill-acknowledgement-audit-delivery-final-reporting-archive-reference-health`

## User Stories

- As a release manager, I can see which failed final auditor export deliveries are safe to retry.
- As an auditor, I can verify that final auditor exports are represented in immutable archive references.
- As a platform operator, I can identify archive custody gaps without exposing storage credentials or private endpoints.

## Enterprise Challenge Solved

This phase makes delivery retry posture and archive completeness measurable in Community Edition while keeping private connector execution and storage writes in Enterprise or operator-owned systems.

## Diagram

See `docs/diagrams/go-backend-rollback-drill-auditor-export-retry-archive-health.svg`.

## Next Recommended Work

Completed in the next slice: final auditor export retry worker execution records and archive health alert delivery acknowledgements. See `Go-Backend-Rollback-Drill-Auditor-Export-Retry-Worker-Archive-Alert-Acks.md`.
