# Integrations

Implemented: CLI, MCP stdio server, FastAPI, webhook exporter, PR attestation exporter, Claude Code repository initializer, GitHub required-check workflow, GitHub Actions, GitLab CI, and Azure Pipelines enforcement templates, approval-bound signed policy publishing, approval provider request specs, live approval provider delivery, SIEM export payloads, JSON/SQLite integration inventory, and live connector execution hooks for SIEM, ITSM, ChatOps, and generic webhooks.

Reference or planned integrations: GitHub App orchestrator, Azure DevOps, pre-commit, VS Code, Docker, Kubernetes, Homebrew, PyPI, Microsoft Sentinel, Splunk, Datadog, ServiceNow, Jira, Slack, Teams, Security Hub, CloudTrail, Azure Monitor, Google SCC, S3 Object Lock, Azure immutable blob, Entra ID, Okta, SAML, and RBAC.

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

## Connector Execution

Set `CAVRA_CONNECTOR_CONFIG` to enable the API delivery endpoint:

- `POST /integrations/{integration_id}/deliver`

Use the CLI for local or CI delivery:

```bash
cavra integration deliver .cavra/evidence/latest/siem-event.json \
  --config .cavra/connectors.json \
  --provider splunk
```

Supported delivery providers are Splunk, Microsoft Sentinel, Datadog, Slack, Microsoft Teams, Jira, ServiceNow, and generic webhooks. Delivery evidence redacts authorization headers, API keys, query strings, and sensitive webhook URLs.

## Connector SDK And Certification

CAVRA now includes a public connector SDK contract for certified Enterprise integrations. The SDK defines a versioned connector manifest, required security flags, certification test suites, compatibility metadata, a reference webhook connector manifest, a certification packet builder, and sample/live readiness gates.

Start with [Connector SDK And Certification](connector-sdk-certification.md). R4.1 provides the interface and certification harness; R4.2 will use it to certify provider-specific connectors across SCM, CI/CD, SIEM, ITSM, and communications systems.

## Priority Certified Connectors

The first certified connector wave is documented in [Priority Certified Connectors](priority-certified-connectors.md). It covers GitHub, GitLab, Azure Repos, GitHub Actions, Jenkins, Splunk, Microsoft Sentinel, ServiceNow, Jira, Slack, and Microsoft Teams.

The public repository validates manifests, provider coverage, compatibility metadata, request specs, redaction behavior, sample packets, and sanitized live packet shape. Production tenants still provide real credentials, provider sandbox logs, firewall evidence, credential custody records, and support ownership during deployment.
