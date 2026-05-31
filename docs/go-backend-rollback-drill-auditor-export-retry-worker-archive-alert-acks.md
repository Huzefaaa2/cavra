# Go Backend Rollback Drill Auditor Retry Worker and Archive Alert Acknowledgements

CAVRA now turns final auditor export retry plans into governed worker runs and records acknowledgement evidence for archive reference health alerts.

## Feature Details

- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-auditor-export/delivery-retry-worker-run` creates dry-run or live retry worker evidence for failed final auditor export deliveries.
- Live worker execution records capture the retry decision, connector delivery metadata, execution status, and public evidence references.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-archive-reference-health-alerts/deliver` sends archive custody health alerts through configured public connector abstractions.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-archive-reference-health-alerts/{health_id}/acknowledgements` records operator review of archive custody alerts.
- Evidence Console now includes **Run Auditor Retry**, **Send Archive Alert**, and **Ack Archive Alert** controls.

## How To Use

1. Generate a final auditor export and capture failed delivery evidence.
2. Run **Plan Auditor Retry** to classify retryable failed delivery providers.
3. Run **Run Auditor Retry** with `execute=true` when the operator is ready to retry delivery.
4. Run **Archive Health** before or after immutable archive references are captured.
5. Use **Send Archive Alert** when health reports show missing archive references, retention timestamps, or hashes.
6. Use **Ack Archive Alert** after release governance or audit operations reviews the alert.

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

Dashboard fields:

- `acknowledgement_audit_delivery_final_reporting_auditor_export_delivery_retry_worker_run_count`
- `acknowledgement_audit_delivery_final_reporting_auditor_export_delivery_retry_execution_record_count`
- `acknowledgement_audit_delivery_final_reporting_auditor_export_delivery_retry_execution_failed_count`
- `acknowledgement_audit_delivery_final_reporting_archive_reference_health_alert_plan_count`
- `acknowledgement_audit_delivery_final_reporting_archive_reference_health_alert_ack_count`
- `acknowledgement_audit_delivery_final_reporting_archive_reference_health_alert_delivery_count`

## User Stories

- As a release manager, I can execute a retry worker after reviewing failed final auditor export delivery evidence.
- As an auditor, I can see whether an archive custody alert was delivered and acknowledged.
- As a platform operator, I can prove that failed final reporting delivery and archive custody gaps were handled without exposing connector secrets.

## Enterprise Challenge Solved

Regulated releases need final audit artifacts to be deliverable, retryable, archived, and reviewable. This phase closes the public-safe evidence loop for final auditor export redelivery and archive custody alert acknowledgement while leaving private delivery connectors, archive writes, and enterprise workflows outside the Community repository.

## Diagram

See `docs/diagrams/go-backend-rollback-drill-auditor-export-retry-worker-archive-alert-acks.svg`.

## Next Recommended Work

Add final reporting readiness bundle export with signed archive manifest and release closeout summary.
