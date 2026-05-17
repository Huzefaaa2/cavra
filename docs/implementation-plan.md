# CAVRA Implementation Plan

This plan explains how CAVRA will be implemented to production readiness. Each phase must produce code, tests, docs, diagrams, and wiki updates.

## Delivery Rules

- Every phase ends with a README update.
- Every phase adds or updates wiki-ready pages under `docs/wiki/`.
- Every phase updates diagrams when architecture, flows, or user journeys change.
- Every phase includes user stories and enterprise challenge mapping.
- Every implemented behavior gets tests or an explicit validation note.
- Planned integrations must be labeled as reference architecture until working code exists.

## Phase Template

Each phase uses this implementation checklist:

- Scope: what changes.
- Acceptance criteria: how completion is judged.
- Code changes: modules, APIs, CLI commands, schemas, examples.
- Tests: unit, integration, CLI, API, Docker, sandbox, policy.
- Documentation: README, docs, wiki, diagrams, examples.
- Enterprise story: buyer, user, risk, control, evidence.
- Release note: what changed and what remains.

## Architecture Workstreams

Runtime governance:
- File Guard.
- Command Guard.
- Git Guard.
- MCP Guard.
- Cloud and IaC operation guard.
- Approval request guard.

Management plane:
- Policy registry.
- Policy inheritance.
- Policy signing and verification.
- Evidence Hub.
- Approval Router.
- Agent Registry.
- MCP Trust Registry.
- FastAPI backend.
- Console UI.

Enforcement plane:
- Python runtime interface.
- Protobuf contract.
- Go runtime backend.
- Local daemon.
- CI runner mode.
- Air-gapped binary.

Enterprise integrations:
- GitHub required check.
- GitLab CI.
- Azure DevOps.
- SIEM exporters.
- ITSM approval connectors.
- OIDC/RBAC.
- Immutable evidence storage.

Developer adoption:
- Claude Code MCP flow.
- Local demo.
- Sandbox.
- Docker image.
- PyPI and pipx.
- Homebrew formula.

## Phase Completion Documentation

After each phase, update:
- `README.md`: feature summary, how to use, enterprise value.
- `docs/production-roadmap.md`: status and next recommendation.
- `docs/current-feature-inventory.md`: implemented capabilities and gaps.
- `docs/wiki/Home.md`: phase completion summary.
- `docs/wiki/White-Paper.md`: architecture and control model updates.
- `docs/wiki/User-Stories.md`: new user stories.
- `docs/wiki/Diagrams.md`: current C4 and flow diagrams.

## Initial Production Backlog

High priority:
- Policy schema enforcement.
- Policy inheritance.
- Signed policies and signed evidence.
- Persistent API storage.
- Approval queue.
- GitHub required check.
- MCP Trust Registry.
- Agent Registry.
- Evidence bundle verification.

Medium priority:
- Console UI.
- SIEM exporters.
- ServiceNow/Jira reference connectors.
- OIDC and RBAC.
- Hosted sandbox deployment.
- Go enforcement backend.

Later:
- Homebrew formula.
- VS Code extension.
- Marketplace listings.
- CAVRA Certified program.
- OEM packaging.
