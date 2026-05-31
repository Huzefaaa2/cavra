# Go Backend Rollback Drill Readiness Approval and Release Record Attachment

CAVRA now records explicit release-readiness approval evidence and public-safe release record attachment evidence for the rollback drill final reporting package.

## Feature Details

- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-release-readiness/{summary_id}/approval-decisions` records a governed decision for a release-readiness summary.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-release-record-attachment` records that the readiness summary, approval decision, final closure dashboard, and operator runbook export were attached to a release record.
- Blocked readiness summaries require `override_blockers=true` before they can be approved.
- Attachments require an approved readiness decision.
- Community Edition records evidence references only. External ticket, release-management, ChatOps, or ITSM mutation remains private connector or operator-owned work.

## How To Use

1. Generate final reporting release readiness.
2. Export the operator runbook.
3. Approve the readiness summary with an external release/change reference.
4. Attach the approved evidence package to the release record.
5. Review the Evidence Console metrics for final approvals and release attachments.

```http
POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-release-readiness/{summary_id}/approval-decisions
POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-release-record-attachment
```

## Evidence Metadata

- `go-backend-rollback-drill-acknowledgement-audit-delivery-final-reporting-release-readiness-approval-decision`
- `go-backend-rollback-drill-acknowledgement-audit-delivery-final-reporting-release-record-attachment`

Dashboard fields:

- `acknowledgement_audit_delivery_final_reporting_release_readiness_approval_decision_count`
- `acknowledgement_audit_delivery_final_reporting_release_readiness_approved_count`
- `acknowledgement_audit_delivery_final_reporting_release_record_attachment_count`

## User Stories

- As a release manager, I can approve or hold final rollback drill readiness using a decision tied to the generated summary.
- As an auditor, I can see which readiness summary was approved and which release record received the evidence package.
- As an operator, I can attach evidence references without exposing customer data, connector secrets, or private release-system implementation.

## Enterprise Challenge Solved

Enterprise release gates often fail because approval, evidence, and release-record attachment live in separate systems. This slice creates a public-safe audit bridge: CAVRA captures the approval decision and the release attachment record while leaving proprietary ticket mutation and private workflow automation outside the Community repository.

## Diagram

See `docs/diagrams/go-backend-rollback-drill-readiness-approval-release-record.svg`.

## Next Recommended Work

Add final reporting release closure packet SIEM/GRC delivery routing and immutable archive references.
