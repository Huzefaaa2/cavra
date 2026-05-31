# Final Closeout Pilot Readiness Checklists

Use these checklists to decide whether a customer is ready to move from trial evaluation to a scoped CAVRA production pilot.

## Repository And Agent Readiness

- [ ] Pilot repositories are named and owned.
- [ ] Protected branches and required checks are documented.
- [ ] AI coding agents, bot accounts, and CI runner identities are listed.
- [ ] MCP servers or local tools used by agents are listed.
- [ ] Block, warn, approval, and audit-only action classes are agreed.
- [ ] PR attestation and evidence expectations are agreed.

## CI/CD Readiness

- [ ] CI/CD platform and runner types are identified.
- [ ] CAVRA required-check placement is agreed.
- [ ] Evidence artifact upload location is agreed.
- [ ] Rollback or final closeout workflow to test is identified.
- [ ] Build logs and artifact retention requirements are documented.
- [ ] Pilot failure behavior is agreed: block, warn, or audit only.

## Connector Readiness

- [ ] Non-production SIEM, ITSM, ChatOps, GRC, or webhook route is available.
- [ ] Connector owners are identified.
- [ ] Connector delivery success criteria are documented.
- [ ] Redaction requirements are documented.
- [ ] Retry owner and retry approval path are documented.
- [ ] Production connector credential handling is assigned to Enterprise, SaaS, or operator-owned systems.

## SSO/RBAC Readiness

- [ ] Identity provider is identified.
- [ ] Release manager, security architect, platform owner, and auditor groups are mapped.
- [ ] Approval permissions are scoped by repository or release workflow.
- [ ] Break-glass ownership and audit expectations are documented.
- [ ] Pilot service accounts or bot identities are reviewed.
- [ ] Customer understands that production SSO/RBAC enforcement requires Enterprise or SaaS implementation.

## Retention And Audit Readiness

- [ ] Evidence retention window is documented.
- [ ] Legal hold expectations are documented.
- [ ] Retention exception owner is identified.
- [ ] Audit handoff destination is identified.
- [ ] Immutable archive requirement is documented.
- [ ] Customer understands that private archive mutation and retention enforcement are outside Community Edition.

## Commercial Handoff Readiness

- [ ] Preferred deployment model is selected: self-hosted Enterprise, SaaS, or hybrid.
- [ ] Required paid policy packs are identified.
- [ ] Required compliance reports are identified.
- [ ] Support model and pilot timeline are agreed.
- [ ] Procurement, security review, and legal stakeholders are identified.
- [ ] Pilot success criteria are accepted by customer sponsor.

## Readiness Rating

| Rating | Meaning |
| --- | --- |
| Green | Ready for a scoped paid pilot. |
| Yellow | Pilot can start after named prerequisites are resolved. |
| Red | Discovery is incomplete or critical owners are missing. |

