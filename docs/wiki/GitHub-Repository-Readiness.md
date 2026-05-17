# GitHub Repository Readiness

Repository: `Huzefaaa2/cavra`

## Access

- Codex GitHub access: verified with admin permission through GitHub CLI.
- Local remote: `https://github.com/Huzefaaa2/cavra.git`.
- Default branch: `main`.
- Wiki and Issues: enabled.
- VS Code support: recommended extensions and settings are included under `.vscode/`.

## Main Branch Protection

`main` is protected with:

- Pull request review required.
- One approving review required.
- Stale reviews dismissed.
- Conversation resolution required.
- Force pushes disabled.
- Branch deletion disabled.

## Security and Quality Features

Enabled:

- Secret scanning.
- Secret scanning push protection.
- Dependabot alerts.
- Dependabot security updates.
- Auto-merge.
- Update branch.
- Delete branch on merge.

Added:

- Dependabot config.
- CodeQL workflow.
- PR template.
- CODEOWNERS.
- Feature and security-control issue templates.
- VS Code workspace recommendations.

## Next Hardening After PR Merge

- Require stable `Test` workflow status checks on `main`.
- Require CodeQL after the first successful run.
- Consider CODEOWNER review requirement.
- Add SBOM and signed release workflows.
