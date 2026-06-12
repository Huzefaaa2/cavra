# Hosted Sandbox Deployment

The hosted sandbox deployment workflow publishes the static CAVRA evidence console through GitHub Pages after merge to `main`.

## Workflow

Workflow file: `.github/workflows/deploy-sandbox.yml`

The workflow:

- Runs on manual dispatch and pushes to `main` that affect the sandbox, docs, or workflow file.
- Validates `apps/sandbox-ui/config.js` and `apps/sandbox-ui/sandbox.js` with `node --check`.
- Copies `apps/sandbox-ui` into a static `public/` artifact.
- Writes `public/config.js` from the optional `CAVRA_PUBLIC_API_BASE_URL`
  and `CAVRA_PUBLIC_TRIAL_API_URL` repository variables.
- Packages the generated Before the Agent Acts sample evidence at `evidence/before-the-agent-acts/evidence.json`.
- Includes SVG diagrams from `docs/diagrams`.
- Configures the already-enabled GitHub Pages site for GitHub Actions publishing.
- Uploads a Pages artifact.
- Deploys only when the workflow runs on `refs/heads/main`.
- Opts JavaScript-based GitHub Actions into Node.js 24 to avoid the hosted-runner Node.js 20 deprecation path.
- Runs a post-deploy smoke check against the public page, JavaScript, stylesheet, brand assets, C4 diagram asset, downloadable evidence file, and browser-rendered dashboard/AISPM routes through `scripts/validate-hosted-sandbox-pages.mjs`.
- Maintains hosted smoke evidence in
  `docs/release-verifications/hosted-sandbox-pages-smoke-validation.md` and
  `docs/release-verifications/hosted-sandbox-pages-smoke-validation.json`.
- Tracks hosted deployment freshness in
  `docs/release-verifications/hosted-sandbox-deployment-freshness.md` and
  `docs/release-verifications/hosted-sandbox-deployment-freshness.json` with
  `scripts/validate-hosted-sandbox-deployment-freshness.py` and the build
  sentinel `community-v1.0.0-aispm-release-evidence-index`.
- Generates a public-safe post-deploy evidence packet with
  `scripts/generate-hosted-sandbox-deploy-evidence.py`.
- Validates the post-deploy evidence contract with
  `scripts/validate-hosted-sandbox-deploy-evidence.py`.
- Uploads the generated evidence as the
  `cavra-hosted-sandbox-post-deploy-evidence` workflow artifact.
- Documents the generated packet contract in
  `docs/release-verifications/hosted-sandbox-post-deploy-evidence.md` and
  `docs/release-verifications/hosted-sandbox-post-deploy-evidence.json`.

## How To Run

After the branch is merged to `main`, run:

```bash
gh workflow run deploy-sandbox.yml --repo Huzefaaa2/cavra --ref main
```

GitHub Pages is enabled for Actions publishing. The public sandbox URL is:

```text
https://huzefaaa2.github.io/cavra/
```

To distinguish a local-ready portal from a stale hosted deployment, run:

```bash
python scripts/validate-hosted-sandbox-deployment-freshness.py
CAVRA_CHECK_LIVE_SANDBOX=true python scripts/validate-hosted-sandbox-deployment-freshness.py
```

If the first command passes and the second command fails, rerun the Pages
deployment workflow and wait for GitHub Pages publication before announcing the
hosted AISPM portal.

## User Stories

- As a prospect, I can open the sandbox without cloud credentials or a local install.
- As a CISO, I can see CAVRA decisions, evidence, and deployment readiness from a browser.
- As a developer, I can copy the Claude Code MCP setup command from the same product surface.
- As a platform evaluator, I can point the public sandbox at a deployed CAVRA API and run backend-generated policy decisions.

## Enterprise Challenge Solved

Security and platform buyers need a short, credible product walkthrough before design-partner workshops. The hosted sandbox makes CAVRA reviewable from a static URL while the same surface can call a deployed API for backend-generated scenario runs, persisted evidence metadata, and activity records.

## Current Limits

- Public URL validation requires the workflow to run from `main`.
- The static sandbox uses built-in sample data when no API is configured.
- Backend-driven sandbox runs require a reachable API URL and matching `CAVRA_CORS_ORIGINS`.
- Public counters require the API activity store to retain sandbox session rows.
- The generated post-deploy evidence artifact is attached to the GitHub Actions
  workflow run rather than committed back to the repository.

## Next Recommended Work

1. Promote Go to an optional backend only after audited parity and deployment tests pass.
