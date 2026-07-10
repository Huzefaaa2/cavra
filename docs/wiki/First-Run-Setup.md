# First-Run Setup

CAVRA includes a built-in setup path for new Community operators. It creates a
safe default environment, demo workspace, validation scenarios, SMTP/report
metadata, and policy-action catalog so users can prove the product immediately
without inventing local risky files by hand.

Start here:

```bash
cavra setup init --workspace-name local-community
cavra setup demo-env --output .cavra/demo-workspace
cavra setup validate --record-decisions
cavra setup complete
```

Or run the local setup wizard:

```bash
cavra setup wizard
```

The setup flow covers:

- default setup state at `.cavra/setup-state.json`;
- fake demo files for secret, Terraform, IAM, Kubernetes, shell, Git, and MCP
  policy decisions;
- AISPM activity seeding from validation decisions;
- SMTP setup by secret reference only;
- policy action catalog inspection and draft change planning;
- API endpoints under `/setup/*` and `/policy-action-catalog`.

Full guide: [CAVRA First-Run Setup](https://github.com/Huzefaaa2/cavra/blob/main/docs/first-run-setup.md).
