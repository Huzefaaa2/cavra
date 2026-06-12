# Hosted Sandbox Deployment Freshness

Status: ready

This public-safe packet explains how CAVRA distinguishes a ready local AISPM
portal build from a stale deployed GitHub Pages site. The current static portal
includes the build sentinel
`community-v1.0.0-aispm-release-evidence-index`.

## Validator

```bash
python scripts/validate-hosted-sandbox-deployment-freshness.py
```

By default, the validator checks local repository files, workflow wiring,
documentation references, and the static portal marker. To check the live hosted
site, run:

```bash
CAVRA_CHECK_LIVE_SANDBOX=true python scripts/validate-hosted-sandbox-deployment-freshness.py
```

## Required Hosted Markers

- `AISPM Trial Lab Notebook Readiness`
- `Release Evidence Index`
- `CSO Report Center`
- `Report Delivery Setup Readiness`
- `Report Operations Readiness`
- `Report Governance Readiness`
- `Report Assurance Readiness`
- `Report Response Readiness`
- `Report Trial Operations Readiness`
- `cavra-aispm-report-catalog-packet.json`
- `cavra-aispm-report-delivery-setup-packet.json`
- `cavra-aispm-report-operations-readiness-packet.json`
- `cavra-aispm-report-governance-readiness-packet.json`
- `cavra-aispm-report-assurance-readiness-packet.json`
- `cavra-aispm-report-response-readiness-packet.json`
- `cavra-aispm-report-trial-operations-readiness-packet.json`
- `cavra-aispm-release-evidence-index-packet.json`
- `community-v1.0.0-aispm-release-evidence-index`

If local validation passes but live validation fails, the repository is ready
and the hosted GitHub Pages deployment is stale. Rerun the deploy workflow,
wait for Pages publication, and rerun `npm run validate:sandbox:hosted`.

## Public Safety Boundary

This packet checks public static portal markers and release evidence links only.
It does not include customer data, private package credentials, license secrets,
raw prompts, Enterprise source code, or tenant telemetry.
