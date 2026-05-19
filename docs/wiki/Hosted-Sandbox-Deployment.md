# Hosted Sandbox Deployment

CAVRA now includes a GitHub Pages deployment workflow for the static Before the Agent Acts sandbox and evidence console.

## Delivered

- `.github/workflows/deploy-sandbox.yml`
- JavaScript validation for `config.js` and `sandbox.js` with `node --check`.
- Static artifact build from `apps/sandbox-ui`.
- Optional `CAVRA_PUBLIC_API_BASE_URL` Pages config for API-backed scenario runs.
- Before the Agent Acts sample evidence packaged for the download action.
- SVG diagram assets included in the artifact.
- GitHub Pages Actions configuration, artifact upload, and deployment from `main`.
- Post-deploy smoke validation for the public page, JavaScript, stylesheet, brand assets, C4 diagram, and downloadable evidence.

## How To Use

After merge to `main`:

```bash
gh workflow run deploy-sandbox.yml --repo Huzefaaa2/cavra --ref main
```

GitHub Pages is enabled for Actions publishing. The public sandbox URL is:

```text
https://huzefaaa2.github.io/cavra/
```

## User Stories

- As a prospect, I can evaluate the sandbox without credentials.
- As a CISO, I can inspect decision outcomes and evidence concepts from a browser.
- As a developer, I can find the Claude Code MCP setup command from the same surface.
- As a platform evaluator, I can connect the hosted sandbox to a deployed CAVRA API and run backend-generated policy decisions.
- As a design partner, I can jump from the sandbox to current release notes, release integrity details, and roadmap context.
- As a product stakeholder, I can see aggregate public demo run counters without adding external analytics.

## Enterprise Challenge Solved

The hosted sandbox shortens enterprise review by giving security, platform, and audit stakeholders a consistent demo surface before they install anything. When an API URL is configured, the same page runs real backend scenarios and persists evidence metadata plus activity records. Telemetry-free public run counters summarize those records without browser tracking, and release-note links keep design-partner demos tied to the latest implementation context.

## Next

Add approved rollback execution workflows and SIEM/ITSM audit export for promotion execution records.
