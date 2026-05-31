# Final Closeout Production Pilot Intake

This intake package converts a successful CAVRA final closeout trial into a scoped production pilot. It is public-safe and should be used before moving a customer into private Enterprise artifacts, SaaS tenant setup, or paid implementation work.

## Pilot Objective

The pilot should prove that CAVRA can govern AI-agent release workflows for a small set of production-like repositories while preserving approval, evidence, retention, and audit handoff requirements.

The intake should produce:

- repository and release workflow scope,
- AI-agent and tool inventory,
- CI/CD enforcement path,
- connector and evidence destination requirements,
- SSO/RBAC and approval ownership,
- retention and audit requirements,
- Enterprise or SaaS handoff plan,
- pilot success criteria.

## Recommended Pilot Scope

| Area | Recommendation |
| --- | --- |
| Repositories | 1 to 3 repositories with real release governance needs. |
| Agents | 1 to 2 AI coding agents or CI runner automation paths. |
| CI/CD | 1 required-check workflow and 1 release-governance evidence path. |
| Connectors | 1 non-production alert route and 1 audit handoff route. |
| Identity | SSO/RBAC group mapping for release, security, and platform owners. |
| Retention | One agreed evidence retention window and exception workflow. |
| Duration | 2 to 4 weeks after technical prerequisites are ready. |

## Repository And Release Workflow Worksheet

| Question | Customer Response |
| --- | --- |
| Which repositories are in scope? |  |
| Which branches are protected? |  |
| Which release workflows require CAVRA evidence? |  |
| Which release record system owns final closeout? |  |
| Which teams own release approval, security review, and platform operations? |  |
| Which existing required checks must remain authoritative? |  |
| Which CAVRA checks should block, warn, or audit only during the pilot? |  |
| Which evidence artifacts must be attached to release records? |  |

## Agent And Tool Inventory

| Question | Customer Response |
| --- | --- |
| Which AI coding agents are used today? |  |
| Which agents can run shell commands or CI tasks? |  |
| Which MCP servers or local tools are used? |  |
| Which agent actions require human approval? |  |
| Which actions are always blocked? |  |
| Which actions can run in audit-only mode during pilot week one? |  |
| Which agent identities or bot accounts appear in Git history or PRs? |  |

## CI/CD Inventory

| Question | Customer Response |
| --- | --- |
| Which CI/CD platform is in scope? |  |
| Which pipeline stages can call CAVRA? |  |
| Which job publishes evidence artifacts? |  |
| Which required check should represent CAVRA enforcement? |  |
| Which runner environments need CAVRA installed? |  |
| Which rollback or closeout workflow should be tested? |  |
| Which artifact retention policy applies to CI evidence? |  |

## Connector And Evidence Destination Inventory

| Destination | Required? | Owner | Notes |
| --- | --- | --- | --- |
| SIEM |  |  |  |
| ITSM |  |  |  |
| ChatOps |  |  |  |
| GRC or audit system |  |  |  |
| Release record system |  |  |  |
| Immutable evidence archive |  |  |  |
| Webhook endpoint |  |  |  |

## Pilot Success Criteria

- CAVRA required check runs on the selected repository or release workflow.
- Final closeout trial evidence is mapped to the customer's release record process.
- At least one release-governance evidence package is reviewed by release, security, and audit stakeholders.
- Retention requirement and exception owner are documented.
- Connector destinations are identified and tested with non-production routes.
- SSO/RBAC approver groups are mapped.
- Enterprise or SaaS deployment path is selected.
- Production blockers are captured with owner and target date.

## Pilot Exit Decision

| Decision | Criteria |
| --- | --- |
| Proceed to paid pilot | Success criteria are met and blockers have owners. |
| Extend pilot | Evidence works but connector, identity, or retention requirements need more time. |
| Pause | Required systems, owners, or security prerequisites are not ready. |

## Template

A machine-readable public-safe intake template is available at `examples/demos/final-closeout-trial/pilot-intake-template.json`.

## Evidence Console Readiness Panel

The public Evidence Console loads the same synthetic intake template and renders:

- readiness cards for repository, agent, CI/CD, connector, SSO/RBAC, and retention scope,
- a checklist for converting trial evidence into pilot prerequisites,
- downloadable access to the public-safe intake template,
- links to the pilot readiness checklist and Enterprise/SaaS handoff guide.

Customer-specific intake responses, private connector routes, identity mappings, commercial details, and production evidence must be captured in a private Enterprise repository, customer tenant, or SaaS control plane. Do not commit customer pilot responses to this public Community repository.
