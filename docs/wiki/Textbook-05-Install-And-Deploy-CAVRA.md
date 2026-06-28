# Install And Deploy CAVRA

This chapter explains common installation and deployment paths. Exact package names and runtime commands can evolve, but the operating pattern is stable: install CAVRA, choose a policy pack, evaluate actions, generate evidence, and decide where enforcement belongs.

## Repository Setup

Clone the public repository:

```bash
git clone https://github.com/Huzefaaa2/cavra.git
cd cavra
```

Install the Python package in editable mode for local development:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Validate the CLI:

```bash
cavra version
cavra policy list
```

## Local Evaluation

Run a decision evaluation against a file operation:

```bash
cavra evaluate write_file iam/admin-role.tf --json
```

The result tells you whether the action is allowed, denied, or routed for approval. Use JSON output for automation and evidence workflows.

## Sandbox GUI

The public sandbox is a static UI under `apps/sandbox-ui`. Run it locally:

```bash
python -m http.server 5173 --directory apps/sandbox-ui
```

Open `http://localhost:5173` and explore the dashboard, demo scenarios, evidence console, approvals, registry views, and AISPM pages.

## API Deployment

CAVRA includes a public API surface for decisions, policy packs, approvals, evidence, AISPM samples, and sandbox workflows. See [API](API) for endpoint families. A local deployment normally starts the API, configures policy and storage paths, then allows the sandbox UI or automation scripts to call the API.

## CI/CD Deployment

CAVRA can be used in CI/CD to require policy decisions and evidence before merging or deploying. A typical flow is:

1. A pull request proposes a high-risk change.
2. CAVRA evaluates the change.
3. Required approvals are opened or verified.
4. Evidence is generated.
5. A CI required check verifies the evidence and attestation.

See [GitHub Required Checks And CI/CD Enforcement](GitHub-Required-Checks-and-CI-CD-Enforcement) and [Evidence Hub And Attestation](Evidence-Hub-and-Attestation).

## Enterprise Deployment

Enterprise deployment adds SSO, RBAC, tenant configuration, live connectors, private policy packs, report delivery, and AISPM live ingestion. Use [Enterprise Trial Self-Service Access](Enterprise-Trial-Self-Service-Access), [OIDC RBAC Deployment](OIDC-RBAC-Deployment), [Connector Execution Hooks](Connector-Execution-Hooks), and [AISPM Enterprise Live Ingestion](AISPM-Enterprise-Live-Ingestion) as the main references.

## Deployment Checklist

- Confirm edition and license boundary.
- Select policy packs.
- Configure evidence storage and trust roots.
- Configure approvals and break-glass rules.
- Configure agent and MCP trust registry entries.
- Add CI/CD enforcement where required.
- For Enterprise, configure tenant identity, connectors, SMTP or report provider settings, runtime workflows, and AISPM ingestion.
- Run readiness validators before production launch.
