# Go Backend Rollback Drill Auditor Retry Worker and Archive Alert Acknowledgements

CAVRA now records governed final auditor export retry worker runs, live retry execution records, archive health alert delivery plans, and archive alert acknowledgements.

## Feature Details

- Added final auditor export delivery retry worker evidence.
- Added live retry execution records for final auditor export delivery attempts.
- Added archive reference health alert delivery plans.
- Added archive health alert acknowledgements and dashboard/history APIs.
- Added Evidence Console controls for running auditor retry workers and acknowledging archive health alerts.

## API

```http
POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-auditor-export/delivery-retry-worker-run
POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-archive-reference-health-alerts/deliver
POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-archive-reference-health-alerts/{health_id}/acknowledgements
GET  /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-archive-reference-health-alerts
GET  /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-archive-reference-health-alert-dashboard
```

## Evidence Metadata

- `go-backend-rollback-drill-acknowledgement-audit-delivery-final-reporting-auditor-export-delivery-retry-worker-run`
- `go-backend-rollback-drill-acknowledgement-audit-delivery-final-reporting-auditor-export-delivery-retry-execution-record`
- `go-backend-rollback-drill-acknowledgement-audit-delivery-final-reporting-archive-reference-health-alert-plan`
- `go-backend-rollback-drill-acknowledgement-audit-delivery-final-reporting-archive-reference-health-alert-ack`

## User Stories

- As a release manager, I can execute a retry worker after reviewing failed final auditor export delivery evidence.
- As an auditor, I can see whether an archive custody alert was delivered and acknowledged.
- As a platform operator, I can prove that final reporting retry and archive custody gaps were handled without exposing connector secrets.

## Enterprise Challenge Solved

This phase closes the public-safe evidence loop for final auditor export redelivery and archive custody alert acknowledgement while keeping private connector delivery, archive writes, and enterprise closeout workflows outside the Community repository.

## Diagram

See `docs/diagrams/go-backend-rollback-drill-auditor-export-retry-worker-archive-alert-acks.svg`.

## Next Recommended Work

Add final reporting readiness bundle export with signed archive manifest and release closeout summary.
