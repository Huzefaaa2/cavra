# AISPM Report Operations Readiness

Status: ready

This public-safe release gate verifies that the AISPM Report Center documents
the Enterprise operational controls needed after report delivery is configured:
audit events, operations health, retention lifecycle, RBAC-scoped retrieval,
and signed export manifests.

## Portal Packet

The AISPM dashboard renders Report Operations Readiness and can copy or
download `cavra-aispm-report-operations-readiness-packet.json`.

## Operations Areas

| Area | Status | Public Contract |
| --- | --- | --- |
| Delivery Audit Events | Enterprise | `src/cavra/schemas/aispm-report-delivery-audit-event.schema.json` |
| Operations Dashboard | Enterprise | `src/cavra/schemas/aispm-report-operations-dashboard.schema.json` |
| Retention Lifecycle | Enterprise | `src/cavra/schemas/aispm-report-retention-lifecycle.schema.json` |
| Search And Retrieval | Enterprise | `src/cavra/schemas/aispm-report-search-retrieval.schema.json` |
| Export Package Manifest | Enterprise | `src/cavra/schemas/aispm-report-export-package-manifest.schema.json` |

## Validation

```bash
python scripts/validate-aispm-report-operations-readiness.py
```

The validator checks portal DOM IDs, JavaScript packet export functions,
workflow wiring, release evidence index inclusion, launch readiness rollup
inclusion, schema/example availability, README links, wiki links, hosted
freshness markers, and public-safety boundaries.

## Public Safety Boundary

This gate includes public-safe schema names, example paths, and operations
readiness expectations only. It excludes raw report payloads, provider response
payloads, recipient addresses, customer identity payloads, signed download
URLs, tenant telemetry, Enterprise source code, private policy packs, and
license secrets.
