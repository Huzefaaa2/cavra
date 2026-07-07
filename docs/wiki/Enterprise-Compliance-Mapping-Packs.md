# Enterprise Compliance Mapping Packs

Last updated: 2026-07-07

CAVRA Enterprise compliance mapping packs convert runtime evidence and AISPM findings into clause-level control mappings for auditor, CISO, board, and customer-success workflows.

R3.3 adds a public-safe contract for five required framework packs:

- NIST AI RMF 1.0
- ISO/IEC 42001
- OWASP LLM/GenAI
- NIST SSDF SP 800-218
- EU AI Act

The public repository includes representative clause mappings and deterministic finding-to-clause tests. Customer-specific control narratives, legal interpretations, and live evidence rooms remain deployment-specific Enterprise operating evidence.

R3.3 is public-repository complete. The closeout boundary is documented in [CAVRA Enterprise Compliance Mapping Packs R3.3 Closeout](Enterprise-Compliance-Mapping-Packs-R3.3-Closeout.md). Customer-specific legal interpretations, approved exceptions, private AISPM findings, evidence-room references, and auditor handoff notes remain Managed or Enterprise deployment evidence.

## What Is Implemented

- Built-in clause-level pack registry in `src/cavra/compliance_packs.py`.
- Deterministic mapping from AISPM/runtime finding tags to framework clauses.
- JSON mapping report builder for auditor and AISPM report center use.
- Readiness packet validator for sample and live Enterprise evidence.
- GitHub Actions workflow for sample and strict live validation.
- Sample findings and sanitized live readiness packet.

## Readiness Gates

Sample contract validation:

```bash
python3 scripts/validate_enterprise_compliance_packs.py \
  --packet examples/compliance/enterprise-compliance-packs.sample.json \
  --output dist/test/enterprise-compliance-packs-sample.json
```

Live sanitized validation:

```bash
python3 scripts/validate_enterprise_compliance_packs.py \
  --packet examples/compliance/enterprise-compliance-packs.live.sanitized.example.json \
  --require-live \
  --output dist/test/enterprise-compliance-packs-live-sanitized.json
```

Finding-to-clause mapping report:

```bash
python3 scripts/validate_enterprise_compliance_packs.py \
  --findings examples/compliance/sample-findings.json \
  --output dist/test/enterprise-compliance-mapping-report.json
```

Built-in registry export:

```bash
python3 scripts/validate_enterprise_compliance_packs.py \
  --registry \
  --output dist/test/enterprise-compliance-pack-registry.json
```

## Live Evidence Requirements

For `ready_for_enterprise_live_compliance_mapping: true`, the live packet must prove:

- The pack registry is approved, versioned, clause-level, and owned.
- All five required frameworks are present.
- Finding-to-clause mapping is enabled and deterministic.
- Mapping taxonomy and report schema are versioned.
- At least 25 clauses are covered with required framework-level tests.
- Coverage is at least 90 percent.
- JSON, Markdown, CSV, and AISPM report outputs are supported.
- Auditor trace, evidence bundle linking, and AISPM report linking are enabled.
- Compliance owner, pack review, exception register, auditor handoff, and latest validation evidence references are present.

## Operating Boundary

The public CAVRA repository ships the contract, schema, sample packs, tests, and public-safe readiness evidence. Production Enterprise deployments must attach their own legal review, customer control mappings, evidence room references, approved exception register, and auditor handoff evidence.

Public completion means the mapper, registry, readiness contract, samples, sanitized live gate, workflow, docs, and tests are present and repeatable. Production completion means the customer-specific legal review and auditor evidence room have been attached to the live deployment.
