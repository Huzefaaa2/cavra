# Diagrams

## C4 Context

See `docs/diagrams/c4-context.md`.

## C4 Container

See `docs/diagrams/c4-container.md`. The current container diagram marks the Approval Router as an implemented JSON/SQLite-backed lifecycle service with repository routing, signed OIDC/JWKS validation, repository RBAC, Entra/Okta deployment references, console actions, console break-glass creation, approval audit details, provider request specs, and live provider delivery evidence. It also marks the Agent and MCP Trust Registry as a JSON/SQLite implementation for governed agent identities, MCP trust decisions, predefined agent profiles, MCP capability classifications, and console registry views. The metadata store now includes JSON/SQLite evidence, session, decision, approval, registry, repository inventory, policy rollout metadata, policy authoring previews, approval-bound signed policy publishing, rollout change plans, deployment readiness checks, integration inventory, connector delivery records, backup/restore operations, retention planning, and governed evidence artifact retrieval. The evidence plane now feeds CI/CD required-check artifacts for GitHub, GitLab, and Azure DevOps templates, configured SIEM/ITSM/ChatOps/webhook connector hooks, and AWS/Azure immutable evidence storage references. The console security boundary and console session context are exposed as OIDC/RBAC/CORS readiness and authenticated actor metadata. The Go enforcement plane remains planned.

## Agent and MCP Registry

See `docs/diagrams/agent-mcp-registry.svg` for the dedicated registry view that separates profiles, registered identities, trust records, classifications, storage modes, runtime decisions, console views, and evidence consumers.

## Runtime Components

See `docs/diagrams/c4-component-runtime.md`.

## Runtime Decision Flow

See `docs/diagrams/runtime-decision-flow.md`.

## Evidence Lifecycle

See `docs/diagrams/evidence-lifecycle.md`.

## Immutable Evidence Storage

See `docs/diagrams/immutable-evidence-storage.svg` for the dedicated immutable storage flow from runtime decision, signed bundle, verifier gate, and storage plan into AWS S3 Object Lock and Azure Blob immutability.

## OIDC/RBAC Deployment

See `docs/diagrams/oidc-rbac-deployment.svg` for the dedicated identity flow from Entra ID or Okta discovery metadata and group claims into CAVRA OIDC config, repository RBAC, console sessions, approvals, and break-glass decisions.

## SVG Images

Repository diagram images:

- `docs/diagrams/architecture-context.svg`
- `docs/diagrams/c4-container.svg`
- `docs/diagrams/runtime-flow.svg`
- `docs/diagrams/evidence-hub.svg`
- `docs/diagrams/immutable-evidence-storage.svg`
- `docs/diagrams/oidc-rbac-deployment.svg`
- `docs/diagrams/policy-lifecycle.svg`
- `docs/diagrams/developer-journey.svg`
- `docs/diagrams/agent-orchestration.svg`
