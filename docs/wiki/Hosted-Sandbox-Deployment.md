# Hosted Sandbox Deployment

CAVRA now includes a GitHub Pages deployment workflow for the static Before the Agent Acts sandbox and evidence console.

## Delivered

- `.github/workflows/deploy-sandbox.yml`
- JavaScript validation with `node --check`.
- Static artifact build from `apps/sandbox-ui`.
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

## Enterprise Challenge Solved

The hosted sandbox shortens enterprise review by giving security, platform, and audit stakeholders a consistent demo surface before they install anything.

## Next

Merge the smoke-check update, rerun the deployment from `main`, confirm the smoke job passes, and connect the sandbox to backend-driven scenarios.
