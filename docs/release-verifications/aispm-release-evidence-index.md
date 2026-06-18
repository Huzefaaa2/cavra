# AISPM Release Evidence Index

Status: ready

This public-safe index gives reviewers one place to find CAVRA AISPM release
verification packets, hosted Pages smoke evidence, post-deploy artifact
contracts, and Enterprise Trial lab notebook readiness.

## Portal Packet

The AISPM dashboard renders the Release Evidence Index and can copy or download
`cavra-aispm-release-evidence-index-packet.json` from the public portal.

## Evidence Items

| Evidence | Markdown | Packet | Validator |
| --- | --- | --- | --- |
| AISPM Launch Readiness Rollup | `docs/release-verifications/aispm-launch-readiness-rollup.md` | `docs/release-verifications/aispm-launch-readiness-rollup.json` | `scripts/validate-aispm-launch-readiness.py` |
| Launch Board Pack Artifact Index | `docs/release-verifications/aispm-launch-board-pack-artifact-index.md` | `docs/release-verifications/aispm-launch-board-pack-artifact-index.json` | `scripts/validate-aispm-launch-artifacts.py` |
| AISPM Report Catalog Readiness | `docs/release-verifications/aispm-report-catalog-readiness.md` | `docs/release-verifications/aispm-report-catalog-readiness.json` | `scripts/validate-aispm-report-catalog-readiness.py` |
| AISPM Report Delivery Setup Readiness | `docs/release-verifications/aispm-report-delivery-setup-readiness.md` | `docs/release-verifications/aispm-report-delivery-setup-readiness.json` | `scripts/validate-aispm-report-delivery-setup-readiness.py` |
| AISPM Report Operations Readiness | `docs/release-verifications/aispm-report-operations-readiness.md` | `docs/release-verifications/aispm-report-operations-readiness.json` | `scripts/validate-aispm-report-operations-readiness.py` |
| AISPM Report Governance Readiness | `docs/release-verifications/aispm-report-governance-readiness.md` | `docs/release-verifications/aispm-report-governance-readiness.json` | `scripts/validate-aispm-report-governance-readiness.py` |
| AISPM Report Assurance Readiness | `docs/release-verifications/aispm-report-assurance-readiness.md` | `docs/release-verifications/aispm-report-assurance-readiness.json` | `scripts/validate-aispm-report-assurance-readiness.py` |
| AISPM Report Response Readiness | `docs/release-verifications/aispm-report-response-readiness.md` | `docs/release-verifications/aispm-report-response-readiness.json` | `scripts/validate-aispm-report-response-readiness.py` |
| AISPM Report Trial Operations Readiness | `docs/release-verifications/aispm-report-trial-operations-readiness.md` | `docs/release-verifications/aispm-report-trial-operations-readiness.json` | `scripts/validate-aispm-report-trial-operations-readiness.py` |
| AISPM Pilot Control Readiness | `docs/release-verifications/aispm-pilot-control-readiness.md` | `docs/release-verifications/aispm-pilot-control-readiness.json` | `scripts/validate-aispm-pilot-control-readiness.py` |
| AISPM v1.0 Public Release Readiness | `docs/release-verifications/aispm-v1.0-public-release-readiness.md` | `docs/release-verifications/aispm-v1.0-public-release-readiness.json` | `scripts/validate-aispm-v100-public-release.py` |
| AISPM Final Announcement Readiness | `docs/release-verifications/aispm-final-announcement-readiness.md` | `docs/release-verifications/aispm-final-announcement-readiness.json` | `scripts/validate-aispm-final-announcement-readiness.py` |
| AISPM Visual Smoke Validation | `docs/release-verifications/aispm-visual-smoke-validation.md` | `docs/release-verifications/aispm-visual-smoke-validation.json` | `npm run validate:sandbox:visual` |
| Hosted Sandbox Pages Smoke | `docs/release-verifications/hosted-sandbox-pages-smoke-validation.md` | `docs/release-verifications/hosted-sandbox-pages-smoke-validation.json` | `npm run validate:sandbox:hosted` |
| Hosted Sandbox Deployment Freshness | `docs/release-verifications/hosted-sandbox-deployment-freshness.md` | `docs/release-verifications/hosted-sandbox-deployment-freshness.json` | `scripts/validate-hosted-sandbox-deployment-freshness.py` |
| Hosted Sandbox Operator Release Status | `docs/release-verifications/hosted-sandbox-operator-release-status.md` | `docs/release-verifications/hosted-sandbox-operator-release-status.json` | `scripts/validate-hosted-sandbox-operator-status.py` |
| Hosted Sandbox Post-Deploy Evidence | `docs/release-verifications/hosted-sandbox-post-deploy-evidence.md` | `docs/release-verifications/hosted-sandbox-post-deploy-evidence.json` | `scripts/validate-hosted-sandbox-deploy-evidence.py` |
| Trial Lab Notebook Readiness | `docs/release-verifications/aispm-trial-lab-notebook-publication-readiness-summary.md` | `docs/release-verifications/aispm-trial-lab-notebook-publication-readiness-summary.json` | `scripts/validate-aispm-trial-lab-notebook.py --check-summary` |
| Phase B Closeout Verification | `docs/aispm-phase-b-closeout-verification.md` | `docs/aispm-phase-b-closeout-verification.md` | `scripts/validate-sandbox-portal.py` |

## Validation

```bash
python scripts/validate-aispm-release-evidence-index.py
```

The validator checks portal DOM IDs, JavaScript packet export functions,
workflow wiring, README links, wiki links, and public-safety boundaries.

## Public Safety Boundary

This index includes public release verification and portal readiness references
only. It excludes customer records, raw prompts, private trial package tokens,
license signing keys, private registry credentials, Enterprise source code, and
tenant telemetry.
