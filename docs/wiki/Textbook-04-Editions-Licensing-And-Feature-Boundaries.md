# Editions, Licensing, And Feature Boundaries

CAVRA is organized into Community, Trial, Enterprise, and SaaS operating models. The editions share the same philosophy: agent actions must pass through runtime authority and produce evidence. They differ in scale, identity integration, connector depth, tenancy, reporting, and support model.

![CAVRA edition map](assets/textbook/cavra-edition-map.svg)

## Community Edition

Community Edition is the public open-core foundation. It is designed for individuals, open source maintainers, small teams, platform experiments, and public-safe demonstrations.

Community includes:

- `cavra` CLI.
- Public API.
- Static sandbox GUI.
- Starter policy packs.
- Runtime decision examples.
- Evidence bundle generation and verification.
- Agent and MCP trust registry surfaces.
- Public-safe AISPM dashboard samples.
- Public schema contracts and examples.

Community does not include Enterprise source code, private tenant data, live production connector credentials, SSO-backed org administration, or paid reporting workflows.

## Trial Edition

Trial Edition is for controlled evaluation of Enterprise workflows. It can be delivered through private binaries, private containers, or hosted environments. Trial users should follow the [CAVRA Trial Field Guide](CAVRA-Trial-Field-Guide.md) and [Enterprise Trial Availability](Enterprise-Trial-Availability.md).

Trial adds evaluation packaging:

- Trial labs and role paths.
- Report center evaluation.
- Operator handoff.
- Pilot evidence rooms.
- Trial revocation, expiry, and closeout evidence.
- Trial-to-pilot readiness checks.

## Enterprise Edition

Enterprise Edition is for organization-wide production governance. It adds:

- SSO and RBAC.
- Tenant isolation.
- Private policy packs.
- Live SIEM, ITSM, ChatOps, SMTP, cloud, endpoint, and evidence connectors.
- Central dashboards.
- Compliance and executive reporting.
- Production AISPM live ingestion.
- Production readiness gates.
- Support handoff and customer operating review workflows.

Enterprise boundaries are documented in [Edition Boundaries](Edition-Boundaries.md), [Enterprise Challenges](Enterprise-Challenges.md), [Enterprise Integration Validation](Enterprise-Integration-Validation.md), and [AISPM Enterprise Live Ingestion](AISPM-Enterprise-Live-Ingestion.md).

## SaaS Control Plane

The SaaS model hosts the Enterprise control plane and centralizes tenant onboarding, entitlement status, policy registry operations, billing boundaries, customer dashboards, support handoff, and recurring operating automation. Public contracts are documented in [SaaS Control Plane Contract](SaaS-Control-Plane-Contract.md), [Tenant Onboarding Contract](Tenant-Onboarding-Contract.md), and [Customer Operating Dashboard And Support Handoff Contract](Customer-Operating-Dashboard-And-Support-Handoff-Contract.md).

## Feature Matrix

| Capability | Community | Trial | Enterprise | SaaS |
| --- | --- | --- | --- | --- |
| Local CLI and policies | Yes | Yes | Yes | Yes |
| Public sandbox GUI | Yes | Yes | Yes | Yes |
| Evidence bundles | Yes | Yes | Yes | Yes |
| AISPM sample posture | Yes | Yes | Yes | Yes |
| SSO and RBAC | No | Evaluation | Yes | Yes |
| Tenant isolation | No | Evaluation | Yes | Yes |
| Live connectors | No | Limited | Yes | Yes |
| Report delivery | Public-safe sample | Evaluation | Production | Managed |
| Central dashboards | No | Limited | Yes | Yes |
| Production readiness gate | Public contract | Trial gate | Live gate | Managed gate |
