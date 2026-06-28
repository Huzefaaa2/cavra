# Hosted Sandbox Deployment Freshness

Status: ready

This public-safe packet explains how CAVRA distinguishes a ready local AISPM
portal build from a stale deployed GitHub Pages site. The current static portal
includes the build sentinel
`community-v1.1.0-public-product-site`.

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

- `Runtime Authority for AI coding agents`
- `The Runtime Authority platform for governing AI coding agents across software delivery.`
- `Why Enterprises Deploy CAVRA`
- `Product Demonstration Environment`
- `Downloads`
- `Before the agent acts, CAVRA decides.`
- `AI Security Posture Management`
- `Run Public Demo`
- `Request Enterprise Trial`
- `Trial Field Guide`
- `GitHub Wiki e-book`
- `community-v1.1.0-public-product-site`
- `sandbox.js`

If local validation passes but live validation fails, the repository is ready
and the hosted GitHub Pages deployment is stale. Rerun the deploy workflow,
wait for Pages publication, and rerun `npm run validate:sandbox:hosted`.

## Public Safety Boundary

This packet checks public static portal markers and release evidence links only.
It does not include customer data, private package credentials, license secrets,
raw prompts, Enterprise source code, or tenant telemetry.
