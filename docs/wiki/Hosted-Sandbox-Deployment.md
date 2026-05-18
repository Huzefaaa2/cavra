# Hosted Sandbox Deployment

CAVRA now includes a GitHub Pages deployment workflow for the static Before the Agent Acts sandbox and evidence console.

## Delivered

- `.github/workflows/deploy-sandbox.yml`
- JavaScript validation with `node --check`.
- Static artifact build from `apps/sandbox-ui`.
- SVG diagram assets included in the artifact.
- GitHub Pages configuration, artifact upload, and deployment from `main`.

## How To Use

After merge to `main`:

```bash
gh workflow run deploy-sandbox.yml --repo Huzefaaa2/cavra --ref main
```

Record the resulting Pages URL in README and wiki after the first successful deployment.

## User Stories

- As a prospect, I can evaluate the sandbox without credentials.
- As a CISO, I can inspect decision outcomes and evidence concepts from a browser.
- As a developer, I can find the Claude Code MCP setup command from the same surface.

## Enterprise Challenge Solved

The hosted sandbox shortens enterprise review by giving security, platform, and audit stakeholders a consistent demo surface before they install anything.

## Next

Run the deployment from `main`, add the public URL, add post-deploy smoke checks, and connect the sandbox to backend-driven scenarios.
