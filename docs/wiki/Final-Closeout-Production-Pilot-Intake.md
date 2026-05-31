# Final Closeout Production Pilot Intake

This page converts a successful CAVRA final closeout trial into a scoped production pilot.

## Intake Outputs

- Repository and release workflow scope
- AI-agent and tool inventory
- CI/CD enforcement path
- Connector and evidence destination requirements
- SSO/RBAC and approval ownership
- Retention and audit requirements
- Enterprise or SaaS handoff plan
- Pilot success criteria

## Recommended Scope

| Area | Recommendation |
| --- | --- |
| Repositories | 1 to 3 repositories with real release governance needs. |
| Agents | 1 to 2 AI coding agents or CI runner automation paths. |
| CI/CD | 1 required-check workflow and 1 release-governance evidence path. |
| Connectors | 1 non-production alert route and 1 audit handoff route. |
| Identity | SSO/RBAC group mapping for release, security, and platform owners. |
| Retention | One agreed evidence retention window and exception workflow. |

## Pilot Success Criteria

- CAVRA required check runs on the selected repository or release workflow.
- Final closeout trial evidence is mapped to the customer's release record process.
- At least one release-governance evidence package is reviewed by release, security, and audit stakeholders.
- Retention requirement and exception owner are documented.
- Connector destinations are identified and tested with non-production routes.
- SSO/RBAC approver groups are mapped.
- Enterprise or SaaS deployment path is selected.

## Template

Use `examples/demos/final-closeout-trial/pilot-intake-template.json` as the public-safe starting template.

## Evidence Console Readiness Panel

The public Evidence Console now loads the same synthetic intake template and renders readiness cards, a pilot checklist, downloadable template access, and Enterprise/SaaS handoff links.

Customer-specific intake responses, private connector routes, identity mappings, commercial details, and production evidence must remain in private Enterprise or SaaS systems.

## Pilot Intake API

See `Final-Closeout-Pilot-Intake-API.md` for the public-safe API scaffold, readiness scoring, local persistence configuration, and Evidence Console save behavior.

## Recommended Next Issue

Add tenant-scoped private persistence, authenticated update permissions, encrypted storage, and connector-backed handoff tasks in Enterprise or SaaS.
