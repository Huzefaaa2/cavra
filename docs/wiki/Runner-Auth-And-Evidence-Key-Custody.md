# Runner Auth And Evidence Key Custody

CAVRA release-governance runners can authenticate with CI-provider OIDC JWTs or HMAC-signed runner claims, and can sign daemon evidence streams with an HMAC key. This document defines the public-safe operating model for custody, rotation, and audit retention.

## Runner Authentication Modes

Preferred mode: CI-provider OIDC.

- GitHub Actions: grant `id-token: write`; the runner wrapper requests a short-lived JWT from `ACTIONS_ID_TOKEN_REQUEST_URL` using `ACTIONS_ID_TOKEN_REQUEST_TOKEN`.
- GitLab CI: configure `id_tokens` and expose the JWT through `CAVRA_GITLAB_OIDC_TOKEN`, `GITLAB_OIDC_TOKEN`, a custom `CAVRA_RUNNER_AUTH_OIDC_TOKEN_ENV`, or legacy `CI_JOB_JWT_V2`.
- Azure Pipelines: use `SYSTEM_OIDCREQUESTURI` with `SYSTEM_ACCESSTOKEN` or `CAVRA_AZURE_OIDC_REQUEST_TOKEN`; `CAVRA_AZURE_OIDC_TOKEN` may be used when the token is acquired by a separate approved step.

Fallback mode: HMAC-signed runner claims.

- Store `CAVRA_RUNNER_AUTH_HMAC_KEY` only in the CI secret store or an enterprise secret manager.
- Use `CAVRA_RUNNER_AUTH_KEY_ID` to identify the active signing key without exposing the secret.
- Prefer OIDC for cloud-hosted CI and reserve HMAC for air-gapped or restricted runners without provider JWT support.

## Daemon Evidence Signing

Daemon evidence signing uses `CAVRA_DAEMON_EVIDENCE_HMAC_KEY` and `CAVRA_DAEMON_EVIDENCE_KEY_ID`.

- The key signs hash-chained JSONL evidence records.
- The key must never be written into evidence artifacts, release bundles, logs, or repository files.
- Publish `release-governance-evidence-verification.json` with the daemon evidence JSONL so auditors can see chain and signature verification status.

## Rotation Cadence

Recommended cadence:

- CI-provider OIDC: rely on provider-issued short-lived JWTs and rotate trusted JWKS through provider metadata.
- Runner HMAC key: rotate at least quarterly, immediately after runner image compromise, and after any CI secret exposure.
- Daemon evidence HMAC key: rotate at least quarterly and before major release trains or regulated audit windows.
- Key IDs: use stable, time-scoped IDs such as `ci-runner-2026-q2` and `ci-evidence-2026-q2`.

Rotation workflow:

1. Create the new secret in the CI secret store.
2. Deploy the daemon with the new `*_KEY_ID`.
3. Run both old and new verification paths during the transition window when operationally required.
4. Stop signing new records with the old key.
5. Retain the old key in the restricted verifier vault only for historical evidence verification.
6. Mark the old key retired in the change record and remove it from runner execution scopes.

## JWKS Trust Configuration

Use provider metadata whenever possible:

- GitHub Actions issuer: `https://token.actions.githubusercontent.com`
- GitHub Actions JWKS: `https://token.actions.githubusercontent.com/.well-known/jwks`
- GitLab issuer: the `CI_SERVER_URL` value for the instance, for example `https://gitlab.com`
- GitLab JWKS: `${CI_SERVER_URL}/oauth/discovery/keys`
- Azure Pipelines issuer and JWKS vary by organization and tenant; configure them explicitly from approved Azure DevOps and Entra metadata.

Pin issuer and audience values in CI configuration. Do not accept arbitrary issuer, audience, or JWKS values from pull request input.

## Evidence Retention

Publish and retain the full `.cavra/go-daemon/` directory for release-governance checks:

- `runner-auth-claims.json`
- `release-governance-response.json`
- `release-governance-evidence.jsonl`
- `release-governance-evidence-verification.json`

The OIDC JWT itself is not retained by default. Daemon evidence redacts OIDC bearer tokens and keeps the public runner identity claims required for audit.

## Required Controls

Release-governance CI should enforce:

- Verified runtime package before runner use.
- Provider OIDC token acquisition or HMAC runner claim signing.
- Pinned issuer, audience, and JWKS trust configuration for OIDC.
- Hash-chained daemon evidence signing.
- Evidence verifier CLI execution.
- Publication of the evidence verification report as a CI artifact.
- Quarterly key rotation and incident-triggered key revocation.

## User Stories

- As a CI platform owner, I can use provider-native OIDC instead of storing long-lived runner authentication secrets.
- As a release manager, I can prove a release-governance check came from an approved CI provider and repository.
- As an auditor, I can verify daemon evidence signatures without receiving live signing keys.
- As a security engineer, I can rotate runner and evidence keys without breaking historical evidence verification.

## Enterprise Challenge Solved

Enterprise release gates need both identity assurance and evidence integrity. Provider-native OIDC reduces long-lived secret exposure, while key custody and verification reports make CAVRA runner checks defensible during audits, incident reviews, and regulated release approvals.
