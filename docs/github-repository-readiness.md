# GitHub Repository Readiness

Repository: `Huzefaaa2/cavra`

## Access

- GitHub CLI access from Codex: verified with admin permission.
- Local remote: `https://github.com/Huzefaaa2/cavra.git`.
- Default branch: `main`.
- Wiki: enabled and published.
- Issues: enabled.
- VS Code support: `.vscode/extensions.json` and `.vscode/settings.json` added for Python, Ruff, YAML, GitHub Actions, GitHub PRs, and Mermaid.

## Branch Protection

`main` is protected with:

- Pull request review required.
- One approving review required.
- Stale reviews dismissed on new commits.
- Conversation resolution required.
- Force pushes disabled.
- Branch deletion disabled.

Status check requirements should be tightened after the productization PR lands and GitHub has stable check names from `Test` and `CodeQL` workflows.

## Security and Quality Features

Enabled at repository level:

- Secret scanning.
- Secret scanning push protection.
- Dependabot alerts.
- Dependabot security updates.
- Auto-merge.
- Update branch button.
- Delete branch on merge.

Added in repository:

- Dependabot configuration for Python and GitHub Actions.
- CodeQL workflow for Python.
- Pull request template.
- CODEOWNERS.
- Feature and security-control issue templates.

## Documentation Discipline

Every release should update:

- `README.md`
- `docs/cavra-productization-report.md`
- `docs/current-feature-inventory.md`
- Relevant docs under `docs/`
- Relevant wiki pages under `docs/wiki/` and the GitHub Wiki
- Diagrams under `docs/diagrams/` when architecture or workflow changes

## Next Fine-Tuning

After PR #1 is merged:

- Require the stable `Test` workflow checks on `main`.
- Require CodeQL once the workflow has produced its first successful run.
- Consider requiring CODEOWNER review.
- Add release signing and SBOM generation in CI.
