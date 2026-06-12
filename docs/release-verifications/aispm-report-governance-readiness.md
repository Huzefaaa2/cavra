# AISPM Report Governance Readiness

Status: ready

This public-safe release gate verifies that the AISPM Report Center documents
the Enterprise governance controls needed before reports can be scheduled,
sent, shared, excepted, or exposed through evidence rooms.

## Portal Packet

The AISPM dashboard renders Report Governance Readiness and can copy or
download `cavra-aispm-report-governance-readiness-packet.json`.

## Governance Areas

| Area | Status | Public Contract |
| --- | --- | --- |
| Schedule Policy | Enterprise | `src/cavra/schemas/aispm-report-schedule-policy.schema.json` |
| Recipient Policy | Enterprise | `src/cavra/schemas/aispm-report-recipient-policy.schema.json` |
| Approval Decisions | Enterprise | `src/cavra/schemas/aispm-report-approval-decision.schema.json` |
| Exception Lifecycle | Enterprise | `src/cavra/schemas/aispm-report-exception-lifecycle.schema.json` |
| Evidence Rooms | Enterprise | `src/cavra/schemas/aispm-report-evidence-room.schema.json` |

## Validation

```bash
python scripts/validate-aispm-report-governance-readiness.py
```

The validator checks portal DOM IDs, JavaScript packet export functions,
workflow wiring, release evidence index inclusion, launch readiness rollup
inclusion, schema/example availability, README links, wiki links, hosted
freshness markers, and public-safety boundaries.

## Public Safety Boundary

This gate includes public-safe schema names, example paths, and governance
readiness expectations only. It excludes recipient addresses, approver
identities, auditor identities, private justifications, raw report content,
signed download URLs, customer records, Enterprise source code, private policy
packs, and license secrets.
