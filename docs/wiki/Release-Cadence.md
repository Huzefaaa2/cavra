# CAVRA Release Cadence

Last updated: 2026-07-07

This policy defines how CAVRA Community releases, maintenance updates, security fixes, and Enterprise public-contract updates move through governance. It supports R1.2 by making release cadence explicit and testable.

## Release Types

| Release Type | Purpose | Minimum Governance |
| --- | --- | --- |
| Community GA | Stable public Community release. | Release trust gate, release security validation, OpenAPI validation, SBOM/provenance, release notes, maintainer approval. |
| Community maintenance | Patch release for defects, dependency updates, docs corrections, or small public-contract updates. | Maintenance checklist, release note freshness, release security validation, focused tests. |
| Security advisory | Fix for vulnerability or sensitive security issue. | Security maintainer review, advisory draft, supported-version impact, regression tests, coordinated disclosure if needed. |
| Enterprise public contract | Public-safe docs, validators, examples, or schemas that describe Enterprise readiness without exposing private implementation. | Public/private boundary review, roadmap update, docs/wiki sync, focused tests. |
| Experimental reference | Demo, sample, reference deployment, or preview adapter. | Clear experimental label, rollback path, docs boundary, focused validation. |

## Cadence

| Cadence | Action |
| --- | --- |
| Weekly | Triage open security, release, docs, roadmap, and dependency issues. |
| Biweekly | Review roadmap status and close stale `In Progress` rows that have passing evidence or reclassify them as blocked/deferred. |
| Monthly | Produce a release-readiness review for Community and public Enterprise contracts. |
| Quarterly | Review maintainer coverage, CODEOWNERS, RFC backlog, release process, and public trust documentation. |
| Emergency | Security fixes can bypass normal cadence but still require security review, regression evidence, and advisory tracking. |

## Release Readiness Checklist

A release can proceed only when:

- required tests pass;
- release-security validation passes;
- OpenAPI contract validation passes when API behavior changes;
- release trust gate passes for package releases;
- SBOM/provenance/signature or attestation artifacts are generated when applicable;
- docs and wiki links are current;
- risk and rollback notes are included;
- public/private boundary is reviewed;
- roadmap rows are updated only when implementation evidence exists.

## Human Approval Boundary

Automation can prepare release artifacts, evidence bundles, and validation outputs. A human maintainer must approve:

- public release publication;
- protected branch merges;
- package publishing;
- security advisories;
- legal, pricing, SLA, compliance, or buyer trust claims;
- roadmap status changes from `In Progress` to `Completed`.

## Roadmap Hygiene

The roadmap must not use endless recurring rows for normal operations. Recurring customer evidence, monitoring, and scorecard activities should be recorded in evidence rooms or operating packets. A new roadmap item is appropriate only when CAVRA gains a new product capability, public contract, API, CLI command, validator, connector, deployment target, evidence schema, or trust artifact.

## Verification

Use:

```bash
python3 scripts/validate_release_security.py
python3 scripts/validate_openapi_contract.py
python3 scripts/validate_release_trust_gate.py
python3 -m pytest tests/test_phase1_trust_governance.py -q
```

