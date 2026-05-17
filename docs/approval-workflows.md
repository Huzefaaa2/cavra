# Approval Workflows

CAVRA routes risky actions to approver groups including Platform Security, Cloud Security, IAM, AppSec, Change Advisory Board, AI Governance, Data Protection, Healthcare Compliance, PCI Compliance, and Repository Owners.

## Current Implementation

Phase 4 introduces a local approval router for self-hosted pilots:

- Approval requests are created from CAVRA decisions that return `require_approval`.
- Requests persist in a JSON store or SQLite database.
- Default routing policies map IAM paths, GitHub workflow paths, default command approvals, Terraform operations, and MCP decisions to approver groups.
- Approvers can approve, deny, or expire pending requests.
- Break-glass overrides require an actor, reason, expiry, approver group, and optional incident or change reference.
- Approval outcomes can be attached back to decisions so evidence bundles and PR attestations include approval state.
- Slack, Teams, Jira, ServiceNow, and webhook reference payloads can be exported without live provider credentials.

Default approval store:

```text
.cavra/approvals.json
```

API deployments can override this with:

```bash
CAVRA_APPROVAL_STORE=.cavra/api/approvals.json uvicorn cavra.api:app --reload
```

SQLite deployments can use:

```bash
cavra approval migrate --sqlite .cavra/approvals.db
CAVRA_APPROVAL_DB=.cavra/approvals.db uvicorn cavra.api:app --reload
```

## CLI Examples

Create a decision that requires approval:

```bash
cavra evaluate write_file iam/admin-role.tf --json > /tmp/cavra-decision.json
```

Create, approve, deny, expire, or break glass:

```bash
cavra approval create /tmp/cavra-decision.json --requested-by developer
cavra approval create /tmp/cavra-decision.json --sqlite .cavra/approvals.db --requested-by developer
cavra approval route /tmp/cavra-decision.json
cavra approval list --state pending
cavra approval approve apr_123 --actor platform-security --reason "Scoped IAM change reviewed" --external-ref CHG-123
cavra approval deny apr_123 --actor platform-security --reason "Missing rollback plan"
cavra approval expire apr_123
cavra approval break-glass /tmp/cavra-decision.json --actor incident-commander --reason "Production recovery" --external-ref INC-777
cavra approval export-notifications apr_123 --output .cavra/approvals/notifications
```

## API Endpoints

- `GET /approvals`
- `POST /approvals`
- `GET /approvals/{approval_id}`
- `POST /approvals/{approval_id}/approve`
- `POST /approvals/{approval_id}/deny`
- `POST /approvals/{approval_id}/expire`
- `POST /approvals/{approval_id}/attach-decision`
- `POST /approvals/break-glass`

## Console View

The sandbox console now includes an approval queue table. It loads `GET /approvals` when the API is reachable and falls back to sample approvals for static demos.

## Provider Payloads

`cavra approval export-notifications` writes:

- `slack-approval-payload.json`
- `teams-approval-payload.json`
- `jira-approval-payload.json`
- `servicenow-approval-payload.json`
- `webhook-approval-payload.json`

## User Stories

- As an IAM owner, I can approve a scoped privilege change with an external change ticket.
- As a change manager, I can deny risky agent actions with a recorded reason.
- As an incident commander, I can use break glass only when a mandatory justification is captured.
- As an auditor, I can see approval state in CAVRA evidence and PR attestations.

## Enterprise Challenge Solved

The approval router preserves human oversight without stopping safe AI-assisted work. High-risk actions become explicit approval records with approver identity, state, rationale, expiry, and evidence references.
