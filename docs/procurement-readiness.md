# Procurement Readiness

CAVRA procurement readiness is the public-safe evidence package a buyer,
security reviewer, platform team, or auditor can inspect before approving a
Community deployment, Enterprise pilot, or future SaaS evaluation. It should
connect product capability claims to verifiable release, operational, security,
and open-core boundary artifacts.

## Required Buyer Evidence

| Area | Public Evidence | Owner Question Answered |
| --- | --- | --- |
| License and source boundary | `LICENSE`, `NOTICE`, `docs/architecture/open-core-model.md`, and `docs/architecture/edition-boundaries.md`. | What is public Community source, and what stays private? |
| Security policy | `SECURITY.md`, `docs/vulnerability-disclosure.md`, and `docs/release-security-advisories.md`. | How do we report vulnerabilities and verify security releases? |
| Release integrity | `docs/release-signing-operations.md`, `docs/go-release-packaging.md`, release packets, checksums, SBOM, SLSA provenance, detached signatures, keyless attestations, and release evidence. | Can a runtime package be traced from source commit to verified artifact? |
| Operational continuity | `docs/persistent-api-operations.md`, `docs/evidence-metadata-migrations.md`, and `docs/production-deployment-guide-validation.md`. | Can operators back up, restore, migrate, and retain governance data? |
| Performance and concurrency | `docs/go-enforcement-production-hardening.md` and `BenchmarkEvaluateAllowCommand` in the Go runtime tests. | Is there a repeatable performance smoke path before promotion? |
| Enterprise integrations | `docs/enterprise-integration-validation.md`, GitHub/GitLab/Azure examples, identity references, and SIEM/ITSM connector docs. | Does CAVRA fit existing source-control, CI/CD, identity, SOC, and change workflows? |
| SOC 2 readiness | This document and `docs/production-readiness-procurement-closeout.md`. | Which Trust Services Criteria evidence does the public repo support today? |
| Data boundary | `docs/console-security-boundary.md`, `docs/security-model.md`, and open-core docs. | What data can remain local, and what must not be committed publicly? |

## SOC 2 Readiness Roadmap

This public Community repository is not a completed SOC 2 audit package. It
does provide evidence hooks that map to a future SOC 2 readiness program:

- Security: required CAVRA checks, PR attestation, release integrity,
  vulnerability disclosure, release advisory workflow, and public boundary
  validation.
- Availability: backup/restore guidance, retention plans, deployment
  validation, and rollback evidence for promoted runtime paths.
- Processing integrity: policy validation, release packet validation, evidence
  bundle verification, upgrade validation, checksums, SBOM, SLSA provenance,
  and keyless attestation.
- Confidentiality: open-core source boundaries, no public Enterprise source,
  redacted connector evidence, and no provider credentials in public examples.
- Privacy: Community documentation avoids customer records, license keys,
  tenant identifiers, provider tenant URLs, private policy packs, and SaaS
  implementation details.

Final SOC 2 scoping, control ownership, evidence retention, auditor access, and
customer-specific data-processing agreements require legal, security, and
compliance review.

## Procurement Closeout Checklist

Before a buyer-facing release or pilot packet is marked ready:

1. Run the Community release, maintenance-release, release-note, dashboard,
   portal, console, deployment, Go hardening, Enterprise integration, and
   production readiness validators.
2. Run `python -m pytest -q`, `python -m ruff check src tests scripts`, and
   `cd go/cavra-runtime && go test ./...`.
3. Confirm backup and restore commands are documented and exercised against a
   test directory before any live restore.
4. Confirm SQLite migrations are idempotent and documented before schema
   changes.
5. Confirm release packets and release notes link to verification evidence,
   README navigation, and wiki navigation.
6. Confirm security advisory drills include vulnerability disclosure intake,
   affected component analysis, mitigation, fixed release evidence, and
   verification commands.
7. Confirm release integrity evidence includes checksums, SBOM, SLSA
   provenance, signatures or signing operations metadata, keyless attestation
   guidance, upgrade validation, and artifact verification.
8. Confirm public docs contain no Enterprise source code, customer records,
   provider credentials, private keys, license-service internals, or private
   policy packs.

## Public Boundary

Procurement evidence in this public repository must remain public-safe. Do not
commit completed SOC 2 audit workpapers, customer questionnaires, customer
contracts, live support records, private security findings, provider
credentials, private signing keys, license keys, SaaS backend implementation,
Enterprise source code, or customer deployment records.

## Enterprise Challenge Solved

Procurement slows down when product claims are disconnected from auditable
evidence. This page gives buyers a single map from CAVRA's public Community
controls to release integrity, operational continuity, vulnerability response,
SOC 2 readiness planning, and open-core source boundaries.
