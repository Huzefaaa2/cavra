# CAVRA Maintainer Governance

Last updated: 2026-07-03

This document implements the Phase 1 governance baseline for CAVRA. It reduces bus-factor risk by defining review ownership, maintainer onboarding, decision records, and security-sensitive change gates. It does not claim that the project already has multiple active maintainers; that remains an explicit roadmap follow-up until additional maintainers are onboarded.

## Maintainer Roles

| Role | Responsibility | Required Before Assignment |
| --- | --- | --- |
| Project Maintainer | Final merge authority, release approval, roadmap status changes. | Repository admin approval, signed-off security policy, release process walkthrough. |
| Security Maintainer | Reviews policy bypass, evidence integrity, auth/RBAC, KMS, audit, connector trust, and release security changes. | Security disclosure workflow review, evidence-verification walkthrough, CODEOWNERS entry. |
| API Maintainer | Reviews API shape, OpenAPI compatibility, SDK/connector contracts, and versioning. | API versioning policy review, OpenAPI validator run, compatibility test review. |
| Documentation Maintainer | Reviews README, wiki, trust docs, deployment docs, diagrams, and product boundaries. | Public-safe documentation checklist and wiki publishing workflow review. |
| Release Maintainer | Reviews release packets, SBOM, provenance, signatures, publish workflows, and advisories. | Release checklist rehearsal and artifact verification workflow review. |

## Security-Sensitive Change Classes

The following changes require at least one Project Maintainer and one Security Maintainer review before merge:

- runtime decision behavior, default-deny/default-allow behavior, or policy evaluation;
- evidence signing, verification, retention, archive, or export;
- approval routing, OIDC/RBAC/ABAC, break-glass, or actor context;
- connector authentication, outbound delivery, SIEM/ITSM/GRC integration, or MCP trust classification;
- API compatibility, generated OpenAPI contract, public schemas, or SDK interfaces;
- release workflows, package manifests, SBOM, provenance, signature, and advisory tooling;
- docs that describe public security posture, Enterprise boundaries, or buyer trust claims.

## Maintainer Onboarding Checklist

1. Read `SECURITY.md`, `docs/vulnerability-disclosure.md`, and `docs/release-security-advisories.md`.
2. Run `python3 scripts/validate_release_security.py`.
3. Run `python3 scripts/validate_openapi_contract.py`.
4. Read `docs/api-versioning-and-openapi.md`.
5. Review the current roadmap at `docs/product/cavra-unified-enterprise-product-enhancement-roadmap.md`.
6. Complete a dry-run review of one runtime/policy/evidence PR.
7. Confirm no private customer data, credentials, private keys, or Enterprise source code are included in public docs or examples.
8. Receive CODEOWNERS assignment for a bounded area.

## Review Rules

- Every PR must have a clear product area, risk level, test evidence, and documentation impact.
- Roadmap status may only be changed when code/docs and test evidence are both included.
- Public docs must distinguish implemented capabilities from planned roadmap items.
- Breaking API changes require a new versioned path, media type, or major API contract.
- Security fixes should include regression tests and advisory evidence.

## RFC Requirement

An RFC is required for:

- new policy language or policy engine changes;
- new tenant isolation model;
- KMS/HSM custody design;
- connector SDK or certification rules;
- zero-trust scanner architecture;
- model/artifact metadata schema;
- event bus or HA topology;
- public API breaking changes.

Use [RFC Process](rfc-process.md) for template and approval flow.
