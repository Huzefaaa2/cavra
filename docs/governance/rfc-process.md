# CAVRA RFC Process

Last updated: 2026-07-03

The RFC process governs architecture changes that affect CAVRA's decision, identity, evidence, posture, connector, scanner, or API surfaces.

## RFC Lifecycle

| State | Meaning |
| --- | --- |
| Draft | Author is collecting requirements and alternatives. |
| Review | Maintainers and impacted stakeholders are reviewing. |
| Accepted | Direction is approved and implementation can begin. |
| Superseded | A later RFC replaces this decision. |
| Rejected | The proposal should not be implemented as written. |

## Required RFC Sections

1. **Summary:** one paragraph explaining the change.
2. **Problem statement:** what enterprise, security, or operator gap this solves.
3. **Roadmap mapping:** roadmap item IDs, such as R2.2 or R4.4.
4. **Threat model:** bypass, misuse, data-exfiltration, privilege, and evidence-integrity risks.
5. **Public/private boundary:** what can be in Community and what must remain private.
6. **Compatibility:** API, CLI, schema, policy, storage, and deployment impact.
7. **Migration:** how existing users move safely.
8. **Observability and evidence:** logs, metrics, audit trail, and verification artifacts.
9. **Test plan:** unit, integration, contract, security, and documentation tests.
10. **Alternatives considered:** at least two alternatives for L or security-sensitive changes.
11. **Rollout and rollback:** feature flags, shadow mode, canary, and rollback path.

## Approval Rules

- Security-sensitive RFCs require Project Maintainer and Security Maintainer approval.
- API RFCs require API Maintainer approval and OpenAPI compatibility review.
- Tenant/data RFCs require migration and restore validation before implementation can be marked complete.
- KMS/HSM, immutable audit, and scanner-agent RFCs require explicit no-secret/no-raw-model-egress assertions.

## RFC File Naming

Use:

```text
docs/governance/rfcs/YYYY-NNN-short-title.md
```

Examples:

```text
docs/governance/rfcs/2026-001-tenant-isolation.md
docs/governance/rfcs/2026-002-kms-evidence-signing.md
docs/governance/rfcs/2026-003-zero-trust-scanner-agent.md
```

## Roadmap Status Updates

After an RFC is accepted and implemented, update:

- source roadmap: `docs/product/cavra-unified-enterprise-product-enhancement-roadmap.md`;
- wiki mirror: `docs/wiki/CAVRA-Unified-Enterprise-Enhancement-Roadmap.md`;
- live wiki clone when publishing;
- tests or validators that prove the implementation.
