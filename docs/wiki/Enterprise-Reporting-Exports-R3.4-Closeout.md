# CAVRA Enterprise Reporting Exports R3.4 Closeout

Last updated: 2026-07-07

R3.4 is closed for the public CAVRA repository. The repository now contains the public-safe report export generator, auditor Markdown export, BI CSV export, executive JSON export, board PDF manifest, readiness validator, sample packet, sanitized live-mode packet, strict CI gate, documentation, and tests needed to prove the reporting export boundary.

Private tenant PDFs, BI workbooks, board-ready decks, recipient delivery logs, GRC upload receipts, approval records, real evidence-room publication records, and customer-specific report distribution evidence belong to Managed or Enterprise evidence rooms, not public source.

## What Is Complete

- Public-safe report export generator in `src/cavra/enterprise_reporting_exports.py`.
- Auditor Markdown narrative export.
- BI CSV metrics export.
- Executive JSON summary export.
- Board PDF manifest for private Enterprise renderers.
- Export manifest with artifact hashes and sample package boundary.
- Readiness validator for sample and live packets.
- Public-safe sample report-export packet.
- Sanitized live-mode packet at `examples/reports/enterprise-report-exports.live.sanitized.example.json`.
- Strict live validation workflow.
- Tests for generated artifacts, parseability, live readiness, failure modes, and workflow coverage.
- Documentation for live evidence requirements and production operating boundary.

## Evidence Boundary

Public evidence proves export package generation, artifact hashing, report export contract validation, sample readiness, and sanitized live readiness. Private deployments attach real tenant data, recipient policy outputs, evidence-room publication records, email or portal delivery logs, GRC upload receipts, board-pack rendering evidence, and auditor handoff records.

## Verification

```bash
python3 scripts/validate_enterprise_report_exports.py \
  --export-dir dist/test/enterprise-report-exports \
  --output dist/test/enterprise-report-export-manifest-result.json

python3 scripts/validate_enterprise_report_exports.py \
  --packet examples/reports/enterprise-report-exports.sample.json \
  --output dist/test/enterprise-report-exports-sample.json

python3 scripts/validate_enterprise_report_exports.py \
  --packet examples/reports/enterprise-report-exports.live.sanitized.example.json \
  --require-live \
  --output dist/test/enterprise-report-exports-live-sanitized-result.json

python3 -m pytest tests/test_enterprise_reporting_exports.py -q
python3 -m ruff check \
  src/cavra/enterprise_reporting_exports.py \
  scripts/validate_enterprise_report_exports.py \
  tests/test_enterprise_reporting_exports.py
```

Expected sanitized live-style result:

```json
{
  "ready_for_enterprise_live_report_exports": true,
  "status": "ready",
  "blocker_count": 0,
  "warning_count": 0
}
```

## R4.1 Handoff

R4.1 connector SDK and certification must preserve the reporting guarantees from R3.4. Certified connectors should produce evidence that can be included in auditor exports, BI metrics, executive summaries, board manifests, immutable audit logs, compliance mappings, and AISPM posture reports.
