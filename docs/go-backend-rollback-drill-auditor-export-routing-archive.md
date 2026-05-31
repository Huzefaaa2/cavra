# Go Backend Rollback Drill Auditor Export Routing and Archive References

CAVRA now routes verified final reporting auditor exports through configured public-safe connector delivery and records immutable archive references for release closure evidence.

## Feature Details

- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-auditor-export/deliver` builds the verified auditor export event, sends it through the requested connector provider, and persists redacted delivery metadata.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-immutable-archive-reference` records an external immutable archive pointer for the verified auditor export without storing private archive credentials or payloads.
- Evidence Console now includes **Deliver Auditor** and **Archive Ref** controls.
- Dashboard metrics show auditor export delivery count, failed auditor export delivery count, and immutable archive reference count.
- Community Edition stores only public-safe event, delivery, and archive reference metadata. Enterprise/private modules own authenticated GRC, SIEM, release-management, and immutable archive integrations.

## How To Use

1. Complete final readiness, runbook export, readiness approval, release record attachment, closure packet verification, and auditor export.
2. Select a public-safe connector provider in the Evidence Console or pass `provider` in the API request.
3. Run **Deliver Auditor** to deliver the final auditor export event and persist redacted connector metadata.
4. Run **Archive Ref** after the export is stored in an external immutable archive.
5. Search rollback drill notification history by kind, delivery source, provider, or delivery result.

```http
POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-auditor-export/deliver
POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-immutable-archive-reference
```

Auditor export delivery request fields:

- `release_record_ref`: optional release or change reference used to select the verified packet.
- `generated_by`: public-safe actor label.
- `provider`: connector provider such as `webhook`, `splunk`, `sentinel`, `jira`, or `servicenow`.
- `retries`: connector retry count.
- `timeout_seconds`: connector timeout.

Archive reference request fields:

- `archive_ref`: required external immutable archive reference.
- `archive_provider`: public-safe provider label.
- `archived_by`: public-safe actor label.
- `retention_until`: optional retention timestamp.
- `legal_hold`: optional legal hold flag.
- `archive_hash`: optional external object digest.
- `notes`: optional public-safe operator notes.

## Evidence Metadata

- Connector delivery source: `go_backend_rollback_drill_acknowledgement_audit_final_reporting_auditor_export`
- Archive metadata kind: `go-backend-rollback-drill-acknowledgement-audit-delivery-final-reporting-immutable-archive-reference`

Dashboard fields:

- `acknowledgement_audit_delivery_final_reporting_auditor_export_delivery_count`
- `failed_acknowledgement_audit_delivery_final_reporting_auditor_export_delivery_count`
- `acknowledgement_audit_delivery_final_reporting_immutable_archive_reference_count`

## User Stories

- As a release manager, I can route the verified rollback drill auditor packet to a release or audit destination from the Evidence Console.
- As an auditor, I can see both the exported evidence packet and the immutable archive reference that preserves it.
- As a platform operator, I can prove delivery and archive custody without exposing connector secrets, archive credentials, private endpoints, or customer payloads.

## Enterprise Challenge Solved

Enterprise release closure needs more than an export file. Teams must prove the final packet was routed to the right audit destination and retained under the correct archive controls. This phase turns delivery and archive custody into searchable, public-safe evidence while leaving private connector implementation and archive credentials outside the Community repository.

## Diagram

See `docs/diagrams/go-backend-rollback-drill-auditor-export-routing-archive.svg`.

## Next Recommended Work

Delivered in [Go Backend Rollback Drill Auditor Export Retry and Archive Health](go-backend-rollback-drill-auditor-export-retry-archive-health.md). Next: add final auditor export retry worker execution records and archive health alert delivery acknowledgements.
