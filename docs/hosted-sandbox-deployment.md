# Hosted Sandbox Deployment

The hosted sandbox deployment workflow publishes the static CAVRA evidence console through GitHub Pages after merge to `main`.

## Workflow

Workflow file: `.github/workflows/deploy-sandbox.yml`

The workflow:

- Runs on manual dispatch and pushes to `main` that affect the sandbox, docs, or workflow file.
- Validates `apps/sandbox-ui/sandbox.js` with `node --check`.
- Copies `apps/sandbox-ui` into a static `public/` artifact.
- Includes SVG diagrams from `docs/diagrams`.
- Configures GitHub Pages.
- Uploads a Pages artifact.
- Deploys only when the workflow runs on `refs/heads/main`.

## How To Run

After the branch is merged to `main`, run:

```bash
gh workflow run deploy-sandbox.yml --repo Huzefaaa2/cavra --ref main
```

The GitHub Pages deployment URL should then be recorded in the README and wiki.

## User Stories

- As a prospect, I can open the sandbox without cloud credentials or a local install.
- As a CISO, I can see CAVRA decisions, evidence, and deployment readiness from a browser.
- As a developer, I can copy the Claude Code MCP setup command from the same product surface.

## Enterprise Challenge Solved

Security and platform buyers need a short, credible product walkthrough before design-partner workshops. The hosted sandbox makes CAVRA reviewable from a static URL while the API-backed console can still be deployed behind enterprise identity for production use.

## Current Limits

- Public URL validation requires the workflow to run from `main`.
- The static sandbox uses built-in sample data when no API is configured.
- Backend-driven sandbox runs remain a future Phase 9 enhancement.

## Next Recommended Work

1. Merge the workflow to `main`.
2. Run the Pages deployment.
3. Add the public sandbox URL to README and wiki.
4. Add a post-deploy smoke check that verifies the page, JavaScript, and key diagram assets.
5. Add backend-driven scenario runs when the public demo is connected to a deployed API.
