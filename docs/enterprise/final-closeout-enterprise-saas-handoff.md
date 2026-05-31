# Final Closeout Enterprise And SaaS Handoff

This handoff plan explains how a successful final closeout trial should move into private Enterprise implementation or SaaS onboarding without exposing private source code in the public Community repository.

## Handoff Inputs

- Completed final closeout trial walkthrough
- Synthetic sample evidence review notes
- Production pilot intake worksheet
- Connector readiness checklist
- SSO/RBAC readiness checklist
- Retention and audit readiness checklist
- Preferred deployment model
- Pilot success criteria

## Deployment Path Decision

| Path | Use When |
| --- | --- |
| Self-hosted Enterprise | Customer needs private network deployment, local control, or air-gapped operation. |
| SaaS Control Plane | Customer wants hosted dashboards, tenant management, managed policy registry, and centralized audit history. |
| Hybrid | Customer needs local enforcement with hosted reporting, licensing, or policy distribution. |

## Enterprise Handoff Responsibilities

| Responsibility | Community | Enterprise Or SaaS |
| --- | --- | --- |
| Public evidence metadata | Yes | Yes |
| Trial documentation | Yes | Yes |
| License validation | No | Yes |
| SSO/RBAC enforcement | No | Yes |
| Authenticated connector delivery | No | Yes |
| Private archive mutation | No | Yes |
| Paid policy packs | No | Yes |
| Organization dashboard | No | Yes |
| Customer-specific templates | No | Yes |

## Handoff Steps

1. Confirm pilot scope and owners.
2. Select deployment path.
3. Confirm commercial terms and trial-to-pilot timeline.
4. Prepare private Enterprise repository or SaaS tenant access.
5. Configure identity and approval groups.
6. Configure non-production connector routes.
7. Configure evidence retention and archive references.
8. Run pilot release workflow with CAVRA evidence capture.
9. Review release closeout evidence with stakeholders.
10. Decide proceed, extend, or pause.

## Production Pilot Deliverables

- Pilot architecture diagram
- Repository and agent inventory
- CI/CD enforcement plan
- Connector routing plan
- SSO/RBAC mapping
- Retention and audit plan
- Evidence review summary
- Commercial rollout recommendation

## Public Repository Boundary

The public repository may include intake templates, documentation, and synthetic sample evidence. It must not include private Enterprise source code, license validation secrets, connector credentials, signing keys, private policy packs, customer templates, or production customer evidence.

