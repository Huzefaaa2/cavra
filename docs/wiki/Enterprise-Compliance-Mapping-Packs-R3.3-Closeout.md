# CAVRA Enterprise Compliance Mapping Packs R3.3 Closeout

Last updated: 2026-07-07

R3.3 is closed for the public CAVRA repository. The repository now contains the clause-level compliance pack registry, deterministic finding-to-clause mapper, mapping report builder, readiness validator, sample packet, sanitized live-mode packet, strict CI gate, documentation, and tests needed to prove the implementation boundary without publishing customer legal interpretation or private auditor evidence.

Customer-specific legal interpretations, control narratives, approved exceptions, auditor notes, customer evidence-room references, tenant names, private AISPM findings, and production auditor handoff records belong to Managed or Enterprise evidence rooms, not public source.

## What Is Complete

- Clause-level registry for NIST AI RMF, ISO/IEC 42001, OWASP LLM/GenAI, NIST SSDF, and EU AI Act.
- 25 public-safe clause mappings across required frameworks.
- Deterministic finding-to-clause mapper.
- Mapping report builder for JSON reports.
- Sample findings with full mapped coverage.
- Readiness validator for sample and live packets.
- Public-safe sample compliance packet.
- Sanitized live-mode packet at `examples/compliance/enterprise-compliance-packs.live.sanitized.example.json`.
- Strict live validation workflow.
- Coverage checks for clause tests, mapped findings, and coverage percent.
- Reporting checks for JSON, Markdown, CSV, and AISPM report outputs.
- Auditor trace, evidence bundle linking, and AISPM report linking checks.
- Compliance owner, pack review, exception register, auditor handoff, and latest validation evidence checks.

## Evidence Boundary

Public evidence proves registry shape, deterministic mapping behavior, report generation, and sanitized live readiness. Private deployments attach customer legal review, approved exception registers, tenant-specific control narratives, live AISPM findings, evidence room links, and auditor handoff evidence.

## Verification

```bash
python3 scripts/validate_enterprise_compliance_packs.py \
  --registry \
  --output dist/test/enterprise-compliance-pack-registry.json

python3 scripts/validate_enterprise_compliance_packs.py \
  --packet examples/compliance/enterprise-compliance-packs.sample.json \
  --output dist/test/enterprise-compliance-packs-sample.json

python3 scripts/validate_enterprise_compliance_packs.py \
  --packet examples/compliance/enterprise-compliance-packs.live.sanitized.example.json \
  --require-live \
  --output dist/test/enterprise-compliance-packs-live-sanitized-result.json

python3 scripts/validate_enterprise_compliance_packs.py \
  --findings examples/compliance/sample-findings.json \
  --output dist/test/enterprise-compliance-mapping-report.json

python3 -m pytest tests/test_compliance_packs.py -q
python3 -m ruff check \
  src/cavra/compliance_packs.py \
  scripts/validate_enterprise_compliance_packs.py \
  tests/test_compliance_packs.py
```

Expected sanitized live-style result:

```json
{
  "ready_for_enterprise_live_compliance_mapping": true,
  "status": "ready",
  "blocker_count": 0,
  "warning_count": 0
}
```

## R3.4 Handoff

R3.4 reporting exports must consume the R3.3 mappings and preserve auditor traceability from runtime evidence to compliance clauses, AISPM posture, immutable audit log references, executive reports, and board-ready packages.
