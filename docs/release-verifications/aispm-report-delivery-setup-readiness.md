# AISPM Report Delivery Setup Readiness

Status: ready

This public-safe release gate verifies that the AISPM Report Center explains
what an Enterprise administrator must configure before scheduled or on-demand
report delivery can be enabled.

## Portal Packet

The AISPM dashboard renders Report Delivery Setup Readiness and can copy or
download `cavra-aispm-report-delivery-setup-packet.json`.

## Setup Areas

| Area | Status | Required Fields |
| --- | --- | --- |
| Organization Profile | Required | `CAVRA_REPORT_FROM_ADDRESS`, `CAVRA_REPORT_DEFAULT_TIMEZONE`, `CAVRA_REPORT_RETENTION_DAYS`, `CAVRA_REPORT_BRAND_PROFILE` |
| Delivery Provider | Enterprise | `CAVRA_REPORT_DELIVERY_MODE`, `CAVRA_REPORT_SMTP_HOST`, `CAVRA_REPORT_SMTP_PORT`, `CAVRA_REPORT_SMTP_USERNAME_REF`, `CAVRA_REPORT_SMTP_PASSWORD_REF`, `CAVRA_REPORT_PROVIDER_TOKEN_REF` |
| Recipient Governance | Required | `CAVRA_REPORT_ALLOWED_RECIPIENT_DOMAINS`, `CAVRA_REPORT_EXTERNAL_APPROVAL_REQUIRED`, `CAVRA_REPORT_ALLOWED_RBAC_ROLES` |
| Schedule And Audit | Required | `CAVRA_REPORT_DEFAULT_SCHEDULE`, `CAVRA_REPORT_RETRY_POLICY`, `CAVRA_REPORT_DELIVERY_AUDIT_RETENTION_DAYS`, `CAVRA_REPORT_AUDIT_EXPORT_REF` |
| Validation And Test Delivery | Enterprise | `provider_validation`, `test_delivery`, `delivery_audit`, `retry_evidence` |

## Validation

```bash
python scripts/validate-aispm-report-delivery-setup-readiness.py
```

The validator checks portal DOM IDs, JavaScript packet export functions,
workflow wiring, release evidence index inclusion, launch readiness rollup
inclusion, README links, wiki links, and public-safety boundaries.

## Public Safety Boundary

This gate includes setup field names and secret-manager reference names only.
It excludes raw SMTP passwords, provider tokens, recipient email addresses,
report contents, customer records, Enterprise source code, private policy
packs, provider responses, signed download URLs, and tenant telemetry.
