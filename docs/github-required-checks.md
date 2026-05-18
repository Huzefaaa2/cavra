# GitHub Required Checks and CI/CD Enforcement

CAVRA can run as a required branch-protection check so AI-assisted changes cannot merge without policy validation, evidence verification, and PR attestation verification.

## Delivered Workflow

The repository workflow `.github/workflows/cavra-governance.yml` is now structured as a required-check candidate:

- Check name: `cavra-required-check`
- Trigger: pull requests and manual workflow dispatch
- Controls: policy-pack validation, CAVRA policy inventory, Ruff linting, pytest, evidence bundle generation, evidence verification, PR attestation verification, and evidence artifact upload
- Artifact: `cavra-required-check-evidence`

To enforce it on `main`, add `cavra-required-check` to required status checks in GitHub branch protection.

## Repository Setup

1. Go to repository settings.
2. Open Branches.
3. Edit the `main` branch protection rule.
4. Enable Require status checks to pass before merging.
5. Select `cavra-required-check`.
6. Keep required review, stale review dismissal, conversation resolution, and force-push protection enabled.

For production evidence signatures, add `CAVRA_EVIDENCE_SIGNING_KEY` as a GitHub Actions secret. Without the secret, the sample workflow uses a deterministic demo HMAC key so template validation still works in local and open-source demonstration repositories.

## Reusable Templates

Copy one of these templates into downstream repositories:

- `examples/github-actions/cavra-required-check.yml`: starter GitHub required check that validates a policy pack, creates evidence if none exists, verifies the bundle, verifies PR attestation, and uploads evidence.
- `examples/github-actions/cavra-enterprise-enforcement.yml`: stricter GitHub workflow for signed policy packs, trust-root evidence verification, key IDs, retention minimums, and artifact enforcement.
- `examples/gitlab-ci/cavra-required-check.gitlab-ci.yml`: GitLab CI equivalent for teams that want the same governance control outside GitHub.

## User Stories

- As a platform engineer, I can make CAVRA a required merge check so AI-assisted pull requests cannot bypass governance.
- As a reviewer, I can open the CAVRA evidence artifact and inspect the PR attestation before approving.
- As an auditor, I can prove that policy validation, evidence verification, and attestation verification ran before merge.
- As a security engineer, I can require trust-root signatures and retention thresholds for regulated repositories.

## Enterprise Challenge Solved

Required checks convert CAVRA from advisory tooling into a merge gate. Enterprises can standardize AI coding controls across repositories, preserve evidence for audits, and prevent undocumented AI-generated changes from merging without verifier-ready attestation.

## Next

The next recommended implementation step is policy-pack approval and signature workflow before write-back publishing.
