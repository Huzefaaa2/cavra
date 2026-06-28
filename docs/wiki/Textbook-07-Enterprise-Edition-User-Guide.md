# Enterprise Edition User Guide

Enterprise Edition extends CAVRA from local governance into organization-wide agentic control. It is intended for platform security, application security, cloud security, release engineering, compliance, and executive reporting teams.

![Enterprise runtime sequence](assets/textbook/cavra-enterprise-sequence.svg)

## Enterprise Responsibilities

Enterprise operators manage:

- Tenant identity and isolation.
- SSO and RBAC.
- Private policy packs.
- Live connector credentials.
- Approval routing.
- Runtime workflow enforcement.
- Evidence storage and retention.
- AISPM live ingestion.
- Report delivery.
- Pilot and production readiness gates.

## Tenant Setup

A production tenant needs:

- Tenant ID and display name.
- SSO provider configuration.
- RBAC role mappings.
- Repository and environment inventory.
- Policy pack assignment.
- Evidence store path or provider.
- Connector configuration.
- Report delivery recipients.
- Operating contacts and escalation routes.

See [Tenant Onboarding Contract](Tenant-Onboarding-Contract), [Tenant Audit Store Operating Contract](Tenant-Audit-Store-Operating-Contract), and [Entitlement Status Contract](Entitlement-Status-Contract).

## Connector Setup

Enterprise connectors can deliver or retrieve evidence, tickets, alerts, reports, and operating records. Typical connector families include:

- SIEM.
- ITSM.
- ChatOps.
- SMTP or report delivery provider.
- GitHub, GitLab, Azure DevOps, and CI/CD systems.
- Cloud and endpoint inventory systems.
- Private queues or internal webhooks.

Connector configuration should always avoid storing secrets in source control. Use environment variables, secret stores, or deployment-level secret management.

## Runtime Workflow Validation

Before production, Enterprise users must run validators against real workflows:

- Live ingestion.
- Streaming.
- Connector delivery.
- Tenant isolation.
- SMTP or provider report delivery.
- Agent and tool workflows.
- Runtime control enforcement.
- AISPM production readiness gate.

The production completion condition is a final packet that returns `ready_for_aispm_production: true` with no blockers.

## Enterprise Operating Reviews

After launch, Enterprise teams should use recurring operating reviews:

- Weekly posture review.
- Open finding review.
- Approval and exception review.
- Report delivery audit.
- Tenant isolation audit.
- Connector health review.
- Security advisory drill.
- Production readiness archive closeout.

These reviews are described through the product contract pages and preserved historical records in [Development And Testing Artifacts](Development-And-Testing-Artifacts).
