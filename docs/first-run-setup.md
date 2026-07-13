# CAVRA First-Run Setup

CAVRA includes a default working environment so a new operator can install the
product, prove policy decisions, seed AISPM activity, and configure report
delivery without creating risky test files by hand.

## What Setup Creates

`cavra setup init` creates a local setup state file at `.cavra/setup-state.json`
unless `CAVRA_SETUP_STATE_STORE` points somewhere else. The state records:

- workspace name, edition, and environment;
- default policy pack, enforcement mode, and editable policy-action catalog;
- local evidence artifact root;
- AISPM enabled state;
- default agent integration expectations for Claude Code, Codex, and Copilot;
- SMTP/report delivery placeholders using a password secret reference, not a raw
  password;
- a demo workspace path and built-in validation scenarios.

## Quick Start

```bash
cavra setup init --workspace-name local-community
cavra setup demo-env --output .cavra/demo-workspace
cavra setup validate --record-decisions
cavra setup complete
```

For the fastest local path, run the non-interactive setup wizard:

```bash
cavra setup wizard
```

The wizard creates or reuses setup state, generates the default demo workspace,
runs validation, reports the setup result, and tells the operator what remains
before AI-agent onboarding.

Validation covers representative file, command, Git, and MCP decisions:

- safe file read is allowed;
- `.env` read is blocked;
- `terraform plan` is allowed;
- `terraform apply -auto-approve` is blocked;
- `iam/admin-role.tf` write requires approval;
- `kubectl delete namespace prod` is blocked;
- direct push to `origin/main` is blocked;
- unknown MCP filesystem server calls are blocked.

When `--record-decisions` is used, validation decisions are written to the
activity store so AISPM has immediate posture events to summarize.

## Demo Workspace

The demo workspace is generated locally and contains fake data only:

```text
.cavra/demo-workspace/
├── .env
├── README.md
├── fake.env
├── iam/admin-role.tf
├── kubernetes/delete-prod.yaml
├── safe-notes.md
├── scripts/deploy.sh
└── terraform/main.tf
```

This workspace is intentionally local. It gives Claude Code, Codex, Copilot,
MCP tools, and manual CLI tests predictable files and commands that trigger the
default policies without touching real repositories, secrets, cloud accounts, or
production infrastructure.

## Policy Action Catalog

Operators can inspect policy-controlled actions:

```bash
cavra setup policy-actions
```

They can test how a proposed action would be decided:

```bash
cavra setup policy-action-test \
  --action-type execute_command \
  --target "terraform apply -auto-approve"
```

They can also generate a safe policy draft plan:

```bash
cavra setup policy-action-plan \
  --operation add \
  --section commands \
  --action block \
  --value "rm -rf /"
```

The plan returns a policy draft and `publish_required: true`. It does not bypass
policy review or directly mutate the active policy pack.

## SMTP Report Delivery Setup

SMTP setup stores connection metadata and a password reference. It does not
store the SMTP password value.

```bash
export CAVRA_REPORT_SMTP_PASSWORD='replace-with-secret-value'

cavra setup smtp \
  --host smtp.example.com \
  --port 587 \
  --username hello@example.com \
  --from-email hello@example.com \
  --recipient security@example.com \
  --password-ref CAVRA_REPORT_SMTP_PASSWORD
```

Use your deployment secret manager for production. For Kubernetes, store the
secret in a Kubernetes Secret or external secret manager. For Azure, use Key
Vault and inject the secret through the deployment runtime.

## API Endpoints

Self-hosted GUI or automation can drive setup through the API:

| Endpoint | Purpose |
| --- | --- |
| `GET /setup/status` | Show setup state, next steps, policy pack availability, demo workspace, and report status. |
| `GET /setup/defaults` | Return the default setup state template. |
| `POST /setup/bootstrap` | Create or overwrite setup state. |
| `POST /setup/demo-workspace` | Generate the demo workspace and record the selected path in setup state. |
| `POST /setup/smtp/test` | Validate SMTP metadata and optional live connectivity without storing a password. |
| `POST /setup/validate` | Run setup validation scenarios and optionally record AISPM activity. |
| `POST /setup/complete` | Mark setup complete after validation. |
| `GET /policy-action-catalog` | List editable policy action entries from the active policy pack. |
| `POST /policy-action-catalog` | Plan an add operation as a policy draft. |
| `PATCH /policy-action-catalog/{entry_id}` | Plan an update operation as a policy draft. |
| `DELETE /policy-action-catalog/{entry_id}` | Plan a delete operation as a policy draft. |
| `POST /policy-action-catalog/test` | Evaluate a sample action against the active policy pack. |

## GUI Setup Flow

The public sandbox includes a First-Run Setup page. When it is served on
`localhost` and the CAVRA API is running on `http://localhost:8000`, the page
automatically connects to the local API and exposes an interactive setup panel
for:

- checking setup status;
- creating default setup state;
- generating the demo workspace;
- validating default scenarios and recording AISPM activity;
- marking setup complete;
- testing SMTP report-delivery metadata without storing the password value;
- loading policy action catalog entries;
- testing a known risky action.

A self-hosted authenticated GUI should use the same setup endpoints above and
present a setup wizard flow:

1. Show setup status and recommended next steps.
2. Let the operator accept defaults or change workspace, policy pack, evidence,
   AISPM, agents, and report settings.
3. Generate the demo workspace with fake high-risk fixtures.
4. Configure SMTP using a secret reference.
5. Run validation and record decisions.
6. Show AISPM posture updated from validation events.
7. Mark setup complete and move to agent onboarding.

## Container And Kubernetes Note

The Community container includes the default policy packs. The setup flow can be
run inside the container or through the API service. For Kubernetes, use the Helm
chart and mount a persistent volume or external database for state that should
survive pod replacement.
