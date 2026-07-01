# CAVRA Community Self-Hosted Guide

CAVRA Community is the full public self-hosted product surface. It includes
runtime decisions, policy evaluation, approvals, evidence, AISPM, report center,
local dashboards, CI/CD enforcement, connector interfaces, reference connectors,
public policy packs, and public contracts.

## Self-Hosted Responsibilities

Operators configure the backing services they want to use:

- Identity provider and RBAC mapping.
- Audit store and evidence retention.
- Object storage and database.
- Report delivery provider such as SMTP or an approved reporting service.
- Policy registry.
- Connector credentials in a secret store.
- Monitoring, backup, recovery, and upgrade automation.

If one of these providers is missing, CAVRA should report `requires_configuration`.

## Quick Start

```bash
git clone https://github.com/Huzefaaa2/cavra.git
cd cavra
python -m venv .venv
source .venv/bin/activate
pip install -e .
cavra version
cavra demo before-the-agent-acts
```

For Azure deployment, use [Azure Community Deployment](Azure-Community-SaaS-Deployment.md).
