# Approval Workflows

CAVRA routes risky AI-agent actions to human approvers while safe actions continue.

## Current Implementation

- Approval requests are created from CAVRA decisions.
- Requests persist in a JSON approval store or SQLite database.
- Default routing policies map IAM paths, GitHub workflow paths, command approvals, Terraform operations, and MCP decisions to approver groups.
- Repository-specific JSON or YAML routing files can override approver groups.
- Optional OIDC-style actor claims can authorize approve and deny decisions against approver groups.
- Approvers can approve, deny, or expire pending requests.
- Break-glass overrides require actor, reason, approver group, expiry, and optional external reference.
- Approval outcomes can be attached to decisions so evidence bundles and PR attestations include approval state.
- Slack, Teams, Jira, ServiceNow, and webhook reference payloads can be exported.
- Credential-free provider request specs can be exported for integration testing without secrets.
- Live provider delivery can send approval requests to Slack, Teams, Jira, ServiceNow, or generic webhooks with secret-backed URLs and tokens.

## API

- `GET /approvals`
- `POST /approvals`
- `GET /approvals/{approval_id}`
- `POST /approvals/{approval_id}/approve`
- `POST /approvals/{approval_id}/deny`
- `POST /approvals/{approval_id}/expire`
- `POST /approvals/{approval_id}/deliver`
- `POST /approvals/{approval_id}/attach-decision`
- `POST /approvals/break-glass`

## CLI

```bash
cavra evaluate write_file iam/admin-role.tf --json > /tmp/cavra-decision.json
cavra approval migrate --sqlite .cavra/approvals.db
cavra approval create /tmp/cavra-decision.json --requested-by developer
cavra approval create /tmp/cavra-decision.json --sqlite .cavra/approvals.db --routing-file .cavra/approval-routing.json --requested-by developer
cavra approval route /tmp/cavra-decision.json
cavra approval route /tmp/cavra-decision.json --routing-file .cavra/approval-routing.json
cavra approval list --state pending
cavra approval approve apr_123 --actor platform-security --reason "Scoped IAM change reviewed" --external-ref CHG-123
cavra approval approve apr_123 --actor iam@example.com --actor-claims /tmp/oidc-claims.json --reason "Scoped IAM change reviewed"
cavra approval break-glass /tmp/cavra-decision.json --actor incident-commander --reason "Production recovery" --external-ref INC-777
cavra approval export-notifications apr_123 --output .cavra/approvals/notifications
cavra approval provider-requests apr_123 --output .cavra/approvals/provider-requests
cavra approval deliver apr_123 --config .cavra/approval-providers.yaml --provider jira --output .cavra/approvals/deliveries
```

Provider delivery config example:

```yaml
approval_providers:
  slack:
    enabled: true
    url_env: CAVRA_SLACK_WEBHOOK_URL
  jira:
    enabled: true
    url: https://jira.example/rest/api/3/issue
    token_env: JIRA_TOKEN
```

## User Stories

- As an IAM owner, I can approve a scoped privilege change.
- As a repository owner, I can route approvals to repo-specific ownership groups.
- As a change manager, I can deny risky agent actions with a reason.
- As an identity administrator, I can require approvers to carry matching identity groups.
- As a change manager, I can deliver approval requests to ITSM or ChatOps systems and retain redacted delivery evidence.
- As an incident commander, I can use break glass only with mandatory evidence.
- As an auditor, I can see approval outcomes in evidence and PR attestations.

See repository source page: `docs/approval-workflows.md`.
