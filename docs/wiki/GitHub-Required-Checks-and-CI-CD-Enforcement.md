# Required Checks and CI/CD Enforcement

CAVRA now includes required-check templates for GitHub, GitLab CI, and Azure DevOps.

## Delivered

- `.github/workflows/cavra-governance.yml` can be used as a protected-branch required check named `cavra-required-check`.
- The workflow validates policy packs, runs lint/tests, generates an evidence bundle, verifies evidence, verifies PR attestation, and uploads `cavra-required-check-evidence`.
- `examples/github-actions/cavra-required-check.yml` provides a starter downstream workflow.
- `examples/github-actions/cavra-enterprise-enforcement.yml` provides trust-root, key-ID, retention, and signed-policy enforcement.
- `examples/gitlab-ci/cavra-required-check.gitlab-ci.yml` provides the same governance pattern for GitLab CI.
- `examples/azure-pipelines/cavra-required-check.azure-pipelines.yml` provides Azure Pipelines enforcement for Azure Repos Build validation policies.

## How to Enforce

Enable branch protection for `main`, require status checks before merge, and select `cavra-required-check`.

For Azure DevOps, create a pipeline from `examples/azure-pipelines/cavra-required-check.azure-pipelines.yml`, add `CAVRA_EVIDENCE_SIGNING_KEY` as a secret pipeline variable, then add the pipeline as a Required Azure Repos Build validation policy on the protected branch.

## User Stories

- As a platform engineer, I can make CAVRA a required merge check.
- As a reviewer, I can inspect PR attestation evidence before approving.
- As an auditor, I can prove governance ran before merge.
- As a security engineer, I can require trust-root signatures and retention thresholds.

## Enterprise Value

Required checks turn CAVRA evidence and policy validation into a merge gate. This helps regulated teams adopt AI coding agents across GitHub, GitLab, and Azure DevOps without losing branch protection, review evidence, or auditability.

## Next

Go daemon client helpers and public sandbox URL validation after deployment from `main`.
