# Integrations

Implemented: CLI, MCP stdio server, FastAPI, webhook exporter, PR attestation exporter, Claude Code repository initializer, approval provider request specs, live approval provider delivery, SIEM export payloads, and JSON/SQLite integration inventory.

Reference or planned integrations: GitHub App, GitHub Action, GitLab CI, Azure DevOps, pre-commit, VS Code, Docker, Kubernetes, Homebrew, PyPI, Sentinel, Splunk, Datadog, ServiceNow, Jira, Slack, Teams, Security Hub, CloudTrail, Azure Monitor, Google SCC, S3 Object Lock, Azure immutable blob, Entra ID, Okta, SAML, and RBAC.

## Integration Inventory

CAVRA now persists enterprise integration records through:

- `GET /integrations`
- `POST /integrations`
- `GET /integrations/{integration_id}`

Records include provider, category, owner, environment, auth mode, endpoint reference, status, health status, capabilities, repository scope, and evidence references.

Configure JSON persistence:

```bash
export CAVRA_INTEGRATION_STORE=.cavra/api/integrations.json
```

Configure SQLite persistence:

```bash
export CAVRA_INTEGRATION_DB=.cavra/api/integrations.db
cavra evidence migrate --sqlite .cavra/api/integrations.db
```

Supported categories are `source_control`, `ci_cd`, `siem`, `itsm`, `chatops`, `identity`, `cloud`, `storage`, `security`, and `observability`.
