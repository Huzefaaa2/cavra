# Final Closeout Pilot Readiness Checklists

Use these checklists to decide whether a customer is ready to move from trial evaluation to a scoped CAVRA production pilot.

## Repository And Agent Readiness

- Pilot repositories are named and owned.
- Protected branches and required checks are documented.
- AI coding agents, bot accounts, and CI runner identities are listed.
- MCP servers or local tools used by agents are listed.
- Block, warn, approval, and audit-only action classes are agreed.

## CI/CD Readiness

- CI/CD platform and runner types are identified.
- CAVRA required-check placement is agreed.
- Evidence artifact upload location is agreed.
- Rollback or final closeout workflow to test is identified.
- Pilot failure behavior is agreed.

## Connector Readiness

- Non-production SIEM, ITSM, ChatOps, GRC, or webhook route is available.
- Connector owners are identified.
- Connector delivery success criteria are documented.
- Redaction requirements are documented.
- Production connector credential handling is assigned to Enterprise, SaaS, or operator-owned systems.

## SSO/RBAC Readiness

- Identity provider is identified.
- Release manager, security architect, platform owner, and auditor groups are mapped.
- Approval permissions are scoped by repository or release workflow.
- Break-glass ownership and audit expectations are documented.

## Retention And Audit Readiness

- Evidence retention window is documented.
- Legal hold expectations are documented.
- Retention exception owner is identified.
- Audit handoff destination is identified.
- Immutable archive requirement is documented.

## Readiness Rating

| Rating | Meaning |
| --- | --- |
| Green | Ready for a scoped paid pilot. |
| Yellow | Pilot can start after named prerequisites are resolved. |
| Red | Discovery is incomplete or critical owners are missing. |
