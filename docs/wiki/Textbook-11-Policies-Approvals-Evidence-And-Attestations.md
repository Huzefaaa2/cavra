# Policies, Approvals, Evidence, And Attestations

CAVRA works because policies, approvals, evidence, and attestations are connected. A policy without evidence is hard to audit. Evidence without policy is hard to interpret. Approval without both is hard to trust.

## Policy Packs

Policy packs define what agents can do. A policy can account for action type, resource path, repository, environment, command class, MCP capability, trust tier, identity claims, and evidence requirements.

Good policy packs are:

- Specific enough to block risky behavior.
- Testable.
- Signed when used in stricter workflows.
- Mapped to rollout modes.
- Reviewed with the same discipline as infrastructure code.

## Approval Workflows

Some actions should not be automatically allowed or denied. They should be routed. CAVRA supports approval creation, listing, approval, denial, expiration, break-glass, notification export, provider request generation, provider delivery, and migration.

Use approvals when:

- The action is high impact but legitimate.
- The action changes production, identity, cloud, or CI/CD.
- The policy requires human review.
- The organization needs external change-management evidence.

See [Approval Workflows](Approval-Workflows).

## Evidence Hub

The Evidence Hub records what happened and why.

![Evidence hub](assets/textbook/evidence-hub.svg)

Evidence can include:

- Decision payloads.
- Policy references.
- Approval records.
- Attestation files.
- Trust roots and signatures.
- Connector delivery records.
- SIEM export events.
- Retention plans.
- Search metadata.
- AISPM report packets.

## PR Attestation

PR attestation connects runtime evidence to code review. A CI check can verify that the pull request includes valid CAVRA evidence and that the attestation matches the expected bundle.

Use this pattern when teams want GitHub branch protection to require governed agent activity before merge.

## Break Glass

Break glass is not a bypass. It is an emergency workflow that requires explicit actor identity, reason, external reference, and evidence. Break-glass usage should be reviewed after the incident and included in AISPM posture.

## Trust Roots

Evidence verification depends on trust roots. Treat evidence signing keys and trust-root bundles as security-critical operating assets. Rotate keys on schedule, restrict write access, and verify bundles in CI/CD and audit workflows.
