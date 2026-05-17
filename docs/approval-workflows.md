# Approval Workflows

CAVRA routes risky actions to approver groups including Platform Security, Cloud Security, IAM, AppSec, Change Advisory Board, AI Governance, Data Protection, Healthcare Compliance, PCI Compliance, and Repository Owners.

## Current Implementation

Phase 4 introduces a local approval router for self-hosted pilots:

- Approval requests are created from CAVRA decisions that return `require_approval`.
- Requests persist in a JSON store or SQLite database.
- Default routing policies map IAM paths, GitHub workflow paths, default command approvals, Terraform operations, and MCP decisions to approver groups.
- Repository-specific JSON or YAML routing files can override default approver groups for local policy overlays.
- Optional OIDC-style actor claims can be mapped to approval groups before approve or deny decisions are accepted.
- Signed OIDC JWTs can be verified against JWKS with issuer, audience, expiry, and not-before checks before approve or deny decisions are accepted.
- Repository RBAC policy files can map enterprise groups to approval groups and grant repository-specific approval permissions.
- Approvers can approve, deny, or expire pending requests.
- Break-glass overrides require an actor, reason, expiry, approver group, and optional incident or change reference.
- Approval outcomes can be attached back to decisions so evidence bundles and PR attestations include approval state.
- Slack, Teams, Jira, ServiceNow, and webhook reference payloads can be exported without live provider credentials.
- Credential-free HTTP request specs can be exported for approval-provider integration testing.
- Live approval provider delivery can send Slack, Teams, Jira, ServiceNow, or generic webhook requests with secret-backed URLs and tokens.

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
cavra approval create /tmp/cavra-decision.json --sqlite .cavra/approvals.db --routing-file .cavra/approval-routing.json --requested-by developer
cavra approval route /tmp/cavra-decision.json
cavra approval route /tmp/cavra-decision.json --routing-file .cavra/approval-routing.json
cavra approval list --state pending
cavra approval approve apr_123 --actor platform-security --reason "Scoped IAM change reviewed" --external-ref CHG-123
cavra approval approve apr_123 --actor iam@example.com --actor-claims /tmp/oidc-claims.json --reason "Scoped IAM change reviewed"
cavra approval approve apr_123 --actor iam@example.com --actor-token /tmp/oidc.jwt --oidc-config .cavra/approval-oidc.json --rbac-file .cavra/approval-rbac.yaml --reason "Signed identity verified"
cavra approval deny apr_123 --actor platform-security --reason "Missing rollback plan"
cavra approval expire apr_123
cavra approval break-glass /tmp/cavra-decision.json --actor incident-commander --reason "Production recovery" --external-ref INC-777
cavra approval export-notifications apr_123 --output .cavra/approvals/notifications
cavra approval provider-requests apr_123 --output .cavra/approvals/provider-requests
cavra approval deliver apr_123 --config .cavra/approval-providers.yaml --provider jira --output .cavra/approvals/deliveries
```

Repository routing files can use `approval_routing` or `routing_rules` as the top-level key:

```json
{
  "approval_routing": [
    {
      "rule_id_prefix": "filesystem.write",
      "target_contains": "iam/",
      "approver_group": "Cloud IAM Owners"
    }
  ]
}
```

Claims-based authorization accepts a local claims JSON file for CLI decisions or an `actor_claims` object for API decisions:

```json
{
  "email": "iam@example.com",
  "groups": ["IAM"]
}
```

Signed OIDC authorization accepts a compact RS256 JWT. CLI approval decisions use `--actor-token`, `--oidc-config`, and optional `--rbac-file`. API approval decisions accept `actor_token` when `CAVRA_APPROVAL_OIDC_CONFIG` is configured.

OIDC config example:

```json
{
  "issuer": "https://login.example",
  "audience": "cavra-approvals",
  "jwks_path": ".cavra/approval-jwks.json",
  "leeway_seconds": 60
}
```

Repository RBAC policy example:

```yaml
approval_rbac:
  group_mappings:
    github-team:payments-owners: Payments Owners
  repository_permissions:
    - repository: payments/api
      approver_group: IAM
      groups:
        - Payments Owners
      actions:
        - approved
        - denied
```

## API Endpoints

- `GET /approvals`
- `POST /approvals`
- `GET /approvals/{approval_id}`
- `POST /approvals/{approval_id}/approve`
- `POST /approvals/{approval_id}/deny`
- `POST /approvals/{approval_id}/expire`
- `POST /approvals/{approval_id}/deliver`
- `POST /approvals/{approval_id}/attach-decision`
- `POST /approvals/break-glass`

## Console View

The sandbox console now includes an approval queue table. It loads `GET /approvals` when the API is reachable and falls back to sample approvals for static demos.

Pending rows expose approve, deny, and expire actions. When the API is reachable the console posts to the approval lifecycle endpoint; static demos update local sample state.

## Provider Payloads

`cavra approval export-notifications` writes:

- `slack-approval-payload.json`
- `teams-approval-payload.json`
- `jira-approval-payload.json`
- `servicenow-approval-payload.json`
- `webhook-approval-payload.json`

`cavra approval provider-requests` writes credential-free HTTP request specs for Slack, Teams, Jira, ServiceNow, and webhook providers. These specs intentionally use placeholder URLs or environment-token references so they can be reviewed without exposing secrets.

`cavra approval deliver` sends live HTTP requests and writes redacted delivery evidence:

```yaml
approval_providers:
  slack:
    enabled: true
    url_env: CAVRA_SLACK_WEBHOOK_URL
  jira:
    enabled: true
    url: https://jira.example/rest/api/3/issue
    token_env: JIRA_TOKEN
  servicenow:
    enabled: true
    url: https://instance.service-now.com/api/now/table/change_request
    token_env: SERVICENOW_TOKEN
  webhook:
    enabled: true
    url_env: CAVRA_APPROVAL_WEBHOOK_URL
```

Delivery evidence is written to `.cavra/approvals/deliveries` by default. Authorization headers and known webhook secret query strings are redacted in the evidence output.

## User Stories

- As an IAM owner, I can approve a scoped privilege change with an external change ticket.
- As a repository owner, I can override default approval routing for repo-specific risk boundaries.
- As a change manager, I can deny risky agent actions with a recorded reason.
- As an identity administrator, I can require approvers to carry matching OIDC groups before a decision is accepted.
- As an identity administrator, I can require signed OIDC tokens from trusted issuers before a human approval is accepted.
- As a repository owner, I can delegate approval rights to ownership groups for a specific repository without granting global approval authority.
- As a change manager, I can deliver approval requests to existing ITSM or ChatOps systems and retain delivery evidence.
- As an incident commander, I can use break glass only when a mandatory justification is captured.
- As an auditor, I can see approval state in CAVRA evidence and PR attestations.

## Enterprise Challenge Solved

The approval router preserves human oversight without stopping safe AI-assisted work. High-risk actions become explicit approval records with approver identity, state, rationale, expiry, and evidence references.
