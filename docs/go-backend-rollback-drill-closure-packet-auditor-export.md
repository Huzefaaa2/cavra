# Go Backend Rollback Drill Closure Packet Verification and Auditor Export

CAVRA now verifies attached final reporting release packets and generates a public-safe auditor export for rollback drill release records.

## Feature Details

- `GET /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-release-closure-packet-verification` validates that a release record attachment includes the expected readiness summary, approved readiness decision, operator runbook export, and final closure dashboard evidence.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-auditor-export` generates a Markdown and JSON auditor packet from the verified public-safe evidence chain.
- Evidence Console now includes **Verify Packet** and **Auditor Export** controls.
- Dashboard metrics show packet verification volume, verified packet count, and auditor export count.
- Community Edition stores metadata references only. External GRC, SIEM, ticketing, release-management, and archival implementation remain private connector or operator-owned work.

## How To Use

1. Generate final reporting release readiness.
2. Export the operator runbook.
3. Approve readiness and attach the evidence to a release record.
4. Run **Verify Packet** to confirm required release closure packet evidence exists.
5. Run **Auditor Export** to generate a public-safe export package for review.
6. Attach the export to the release record or forward it through private enterprise connectors.

```http
GET  /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-release-closure-packet-verification
POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-auditor-export
```

Verification query parameters:

- `release_record_ref`: optional release or change reference used to select the attached packet.
- `generated_by`: public-safe actor label.
- `persist`: defaults to true; set false to preview without storing metadata.

Auditor export request fields:

- `release_record_ref`: optional release or change reference used to select the attached packet.
- `generated_by`: public-safe actor label.

## Evidence Metadata

- `go-backend-rollback-drill-acknowledgement-audit-delivery-final-reporting-release-closure-packet-verification`
- `go-backend-rollback-drill-acknowledgement-audit-delivery-final-reporting-auditor-export`

Dashboard fields:

- `acknowledgement_audit_delivery_final_reporting_release_closure_packet_verification_count`
- `acknowledgement_audit_delivery_final_reporting_release_closure_packet_verified_count`
- `acknowledgement_audit_delivery_final_reporting_auditor_export_count`

## User Stories

- As a release manager, I can verify that the release record has the expected final rollback drill evidence before closing the release.
- As an auditor, I can receive a single packet that lists the readiness summary, approval decision, runbook export, closure verification, and public evidence references.
- As a platform operator, I can generate audit material without exposing connector credentials, private endpoints, customer data, or proprietary workflow automation.

## Enterprise Challenge Solved

Enterprise audit closure often fails because release evidence is scattered across dashboards, tickets, and manual notes. This slice creates a repeatable closure packet check and auditor export while preserving the open-core boundary: Community Edition owns public-safe metadata and Enterprise/private connectors can route the export to GRC, SIEM, archive, or release systems.

## Diagram

See `docs/diagrams/go-backend-rollback-drill-closure-packet-auditor-export.svg`.

## Next Recommended Work

Delivered in [Go Backend Rollback Drill Auditor Export Routing and Archive References](go-backend-rollback-drill-auditor-export-routing-archive.md). Next: add auditor export delivery retry planning, archive reference verification health checks, and Evidence Console drill-downs for archive custody gaps.
