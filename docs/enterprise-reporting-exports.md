# Enterprise Reporting Exports

CAVRA Enterprise reporting exports package runtime evidence, AISPM posture, compliance mappings, immutable audit trails, and executive summaries into artifacts that auditors, BI teams, executives, and boards can consume.

R3.4 adds a public-safe reporting export contract with four export lanes:

- Auditor Markdown narrative.
- BI CSV metrics extract.
- Executive JSON summary.
- Board PDF manifest for Enterprise private rendering.

The public repository generates sample artifacts and validates the contract. Production PDF rendering, workbook generation, tenant-scoped evidence rooms, recipient delivery, GRC upload, and approval workflows remain Enterprise deployment responsibilities.

## What Is Implemented

- Public-safe report export builder in `src/cavra/enterprise_reporting_exports.py`.
- Sample artifact generation for JSON, CSV, Markdown, and board PDF manifest outputs.
- Readiness packet validator for sample and live Enterprise evidence.
- GitHub Actions workflow for sample and strict live validation.
- Sample and sanitized live readiness packets.

## Generate Sample Exports

```bash
python3 scripts/validate_enterprise_report_exports.py \
  --export-dir dist/test/enterprise-report-exports \
  --output dist/test/enterprise-report-export-manifest-result.json
```

The generated sample package contains:

- `executive-summary.json`
- `bi-metrics.csv`
- `auditor-narrative.md`
- `board-pack-pdf-manifest.json`
- `enterprise-report-export-manifest.json`

## Readiness Gates

Sample contract validation:

```bash
python3 scripts/validate_enterprise_report_exports.py \
  --packet examples/reports/enterprise-report-exports.sample.json \
  --output dist/test/enterprise-report-exports-sample.json
```

Live sanitized validation:

```bash
python3 scripts/validate_enterprise_report_exports.py \
  --packet examples/reports/enterprise-report-exports.live.sanitized.example.json \
  --require-live \
  --output dist/test/enterprise-report-exports-live-sanitized.json
```

## Live Evidence Requirements

For `ready_for_enterprise_live_report_exports: true`, the live packet must prove:

- Export catalog is approved, versioned, owned, and covers auditor, BI, executive, and board audiences.
- PDF, CSV, JSON, and Markdown formats are present.
- Auditor Markdown, BI CSV, executive JSON, and board PDF manifest exports are generated.
- Checksums, PDF render, CSV schema, JSON schema, Markdown render, and package manifest validation passed.
- Portal, email, and GRC upload distribution paths are tested.
- RBAC, recipient policy, watermarking, immutable storage, redaction, and export approval controls are enabled.
- Report owner, approval policy, export validation, evidence room, auditor handoff, and board pack review refs are present.

## Operating Boundary

The public CAVRA repository ships the export contract, sample artifacts, validator, workflow, and public-safe docs. Real Enterprise deployments attach private tenant metrics, real board PDFs, BI workbooks, recipient delivery logs, audit evidence rooms, and approved GRC upload evidence.
