# Architecture And Open-Core Design

CAVRA uses an open-core architecture. The public repository contains the Community Edition, public contracts, sample policy packs, API and CLI surfaces, sandbox UI, public-safe AISPM surfaces, and documentation. Enterprise source code lives outside the public repository.

![Architecture context](assets/textbook/architecture-context.svg)

## Core Components

| Component | Purpose |
| --- | --- |
| CLI | Local and automation-facing command interface for policy, decisions, approvals, evidence, registry, release, runtime, and demos. |
| API | HTTP surface for decisions, policy packs, agents, approvals, evidence, integrations, AISPM samples, and sandbox workflows. |
| Policy engine | Evaluates action requests against policy packs and runtime context. |
| Approval store | Tracks pending, approved, denied, expired, and break-glass decisions. |
| Evidence hub | Generates, signs, verifies, indexes, searches, exports, and retains decision evidence. |
| Agent registry | Tracks governed agent identities and capabilities. |
| MCP trust registry | Tracks MCP servers, trust tiers, approval states, capabilities, and tool classifications. |
| Sandbox GUI | Static public portal that demonstrates runtime governance, evidence, AISPM, reports, and trial flows. |
| AISPM | AI Security Posture Management surfaces for posture, findings, coverage, reports, trial readiness, and production gates. |

## Open-Core Boundary

Community Edition includes local governance and public-safe workflows. Enterprise features include organization-wide identity, live connectors, tenant isolation, private policy packs, central dashboards, compliance reporting, production report delivery, and live AISPM ingestion.

See [Edition Boundaries](Edition-Boundaries) and [Private Enterprise Repo Plan](Private-Enterprise-Repo-Plan) for detailed separation.

## Runtime Planes

CAVRA can be understood through four planes:

- Decision plane: policy evaluation, runtime decisions, command checks, MCP checks, and high-risk action handling.
- Identity and trust plane: agents, MCP trust, OIDC, RBAC, tenant context, and entitlement state.
- Evidence plane: signed evidence, trust roots, attestation, metadata, search, retention, SIEM export, and report packaging.
- Posture plane: AISPM dashboards, findings, control coverage, report center, trial readiness, and production readiness gates.

## Community To Enterprise Path

CAVRA Community Edition lets a team learn the operating model locally. A typical path is:

1. Run local evaluations with starter policies.
2. Generate evidence bundles and verify attestations.
3. Use the sandbox GUI to understand decisions and AISPM.
4. Add CI/CD enforcement and required evidence.
5. Move into Enterprise evaluation when SSO, RBAC, tenant isolation, live connectors, and production reporting are required.

![Enterprise sequence](assets/textbook/cavra-enterprise-sequence.svg)
