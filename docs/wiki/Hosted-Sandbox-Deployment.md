# Hosted Sandbox Deployment

The hosted sandbox deployment workflow publishes the static CAVRA evidence console through GitHub Pages after merge to `main`.

## Workflow

Workflow file: `.github/workflows/deploy-sandbox.yml`

The workflow:

- Runs on manual dispatch and pushes to `main` that affect the sandbox, docs, or workflow file.
- Validates `apps/sandbox-ui/config.js` and `apps/sandbox-ui/sandbox.js` with `node --check`.
- Copies `apps/sandbox-ui` into a static `public/` artifact.
- Writes `public/config.js` from the optional `CAVRA_PUBLIC_API_BASE_URL` repository variable.
- Packages the generated Before the Agent Acts sample evidence at `evidence/before-the-agent-acts/evidence.json`.
- Includes SVG diagrams from `docs/diagrams`.
- Configures the already-enabled GitHub Pages site for GitHub Actions publishing.
- Uploads a Pages artifact.
- Deploys only when the workflow runs on `refs/heads/main`.
- Opts JavaScript-based GitHub Actions into Node.js 24 to avoid the hosted-runner Node.js 20 deprecation path.
- Runs a post-deploy smoke check against the public page, JavaScript, stylesheet, brand assets, C4 diagram asset, and downloadable evidence file.

## How To Run

After the branch is merged to `main`, run:

```bash
gh workflow run deploy-sandbox.yml --repo Huzefaaa2/cavra --ref main
```

GitHub Pages is enabled for Actions publishing. The public sandbox URL is:

```text
https://huzefaaa2.github.io/cavra/
```

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

## Next Recommended Work

1. Promote Go to an optional backend only after audited parity and deployment tests pass.
