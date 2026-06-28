# Deployment

## Install

Local CLI: install the Python package and run `cavra`.

API: run `uvicorn cavra.api:app --host 0.0.0.0 --port 8000`.

Sandbox UI: run `python -m http.server 5173 --directory apps/sandbox-ui`.

## Azure Community SaaS

CAVRA Community can be deployed from GitHub to Azure as a public Community
service:

- API: Azure Container Apps using `docker/Dockerfile.azure-api`.
- UI: Azure Static Web Apps using `apps/sandbox-ui`.
- Image registry: Azure Container Registry.
- CI/CD: GitHub Actions with Azure OIDC.

The implementation workflows are:

- `.github/workflows/deploy-azure-api.yml`
- `.github/workflows/deploy-azure-static-ui.yml`

Set `AZURE_DEPLOY_ENABLED=true` only after the Azure resources, GitHub
variables, and Static Web Apps deployment token are configured. Use
`CAVRA_PUBLIC_API_BASE_URL` and `CAVRA_CORS_ORIGINS` to bind the static UI to the
published API.

Full operator guide: [Azure Community SaaS Deployment](azure-community-saas-deployment.md).

This is a Community deployment path. It does not add Enterprise tenant
isolation, private policy packs, live connectors, SMTP/report-provider delivery,
or AISPM production readiness gates.

## Azure Trial And Enterprise

Trial and Enterprise Azure deployments are implemented in the private
`Huzefaaa2/cavra-enterprise` repository. They cover the Trial portal and license
request workflow, authenticated evaluator/operator access, time-limited trial
licenses, private package delivery, guided AISPM labs, expiry and revocation,
the private Enterprise control plane, Entra ID OIDC/SSO, RBAC, tenant
isolation, private policy packs, live connectors, report delivery, runtime
workflow validation, and AISPM production validation.

Public-safe architecture guide:
[Azure Trial And Enterprise Deployment](azure-trial-enterprise-deployment.md).

## Configuration

Configure production paths with environment variables instead of source changes.
Core public Community settings include:

- `CAVRA_ACTIVITY_STORE` or `CAVRA_ACTIVITY_DB` for decision and session
  persistence.
- `CAVRA_INVENTORY_STORE` or `CAVRA_INVENTORY_DB` for repository and rollout
  persistence.
- `CAVRA_INTEGRATION_STORE` or `CAVRA_INTEGRATION_DB` for integration
  inventory persistence.
- `CAVRA_EVIDENCE_ARTIFACT_ROOT` for allowlisted evidence artifact retrieval.
- `CAVRA_PUBLIC_API_BASE_URL` for the static console's API base URL.
- `CAVRA_CORS_ORIGINS` for restricted browser/API origins.

## Storage

Run `cavra ops stores` before release validation or pilot handoff to confirm
the active JSON and SQLite persistent stores.

## Backup

Run `cavra ops backup --output .cavra/backups/production-check` before upgrade,
pilot reset, or release evidence capture.

## Restore

Run `cavra ops restore .cavra/backups/production-check/manifest.json --target-dir /tmp/cavra-restore-test`
to validate backup checksums in a test directory before any live restore.

## CORS/API

Run `curl http://127.0.0.1:8000/deployment/production-readiness` in the API
environment and confirm restricted CORS, persistent stores, evidence artifact
root, policy catalog, and optional Go readiness checks.

## GitHub Pages

Run `python scripts/validate-sandbox-portal.py`,
`python scripts/validate-console-closeout.py`, and
`python scripts/validate-community-ga-path.py` before publishing the public
GitHub Pages portal.

## Guide Validation

Production deployment guide coverage is enforced by
`scripts/validate-production-deployment-guide.py` and documented in
[production-deployment-guide-validation.md](production-deployment-guide-validation.md).

Self-hosted enterprise deployments should add persistent storage, OIDC, RBAC, SIEM export, immutable evidence storage, and approval workflow providers.

OIDC/RBAC deployment references:

- Microsoft Entra ID: `examples/identity/entra-id-oidc-rbac`
- Okta: `examples/identity/okta-oidc-rbac`

See [OIDC/RBAC deployment](oidc-rbac-deployment.md) for the operator flow.

Immutable evidence storage deployment references:

- AWS S3 Object Lock: `examples/immutable-storage/aws-s3-object-lock`
- Azure Blob immutability: `examples/immutable-storage/azure-blob-immutability`

See [immutable evidence storage](immutable-evidence-storage.md) for the operator flow.
