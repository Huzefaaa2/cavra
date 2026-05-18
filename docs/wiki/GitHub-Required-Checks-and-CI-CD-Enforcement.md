# GitHub Required Checks and CI/CD Enforcement

CAVRA now includes required-check templates for GitHub and CI/CD enforcement examples for GitHub Actions and GitLab CI.

## Delivered

- `.github/workflows/cavra-governance.yml` can be used as a protected-branch required check named `cavra-required-check`.
- The workflow validates policy packs, runs lint/tests, generates an evidence bundle, verifies evidence, verifies PR attestation, and uploads `cavra-required-check-evidence`.
- `examples/github-actions/cavra-required-check.yml` provides a starter downstream workflow.
- `examples/github-actions/cavra-enterprise-enforcement.yml` provides trust-root, key-ID, retention, and signed-policy enforcement.
- `examples/gitlab-ci/cavra-required-check.gitlab-ci.yml` provides the same governance pattern for GitLab CI.

## How to Enforce

Enable branch protection for `main`, require status checks before merge, and select `cavra-required-check`.

## User Stories

- As a platform engineer, I can make CAVRA a required merge check.
- As a reviewer, I can inspect PR attestation evidence before approving.
- As an auditor, I can prove governance ran before merge.
- As a security engineer, I can require trust-root signatures and retention thresholds.

## Enterprise Value

Required checks turn CAVRA evidence and policy validation into a merge gate. This helps regulated teams adopt AI coding agents without losing branch protection, review evidence, or auditability.

## Next

Azure DevOps required-check enforcement, immutable evidence store deployment references, and OIDC/RBAC deployment bundles.
