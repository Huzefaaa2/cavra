# Community GA User-Verifiable Path

This page ties the public CAVRA Community GA release into one operator-verifiable
path. It connects Policy, Evidence, Console, Go Runtime readiness, and Release
Verification so maintainers, auditors, platform teams, and CISOs can inspect the
same release story from public artifacts.

## Validation Command

Run the validator from the repository root:

```bash
python scripts/validate-community-ga-path.py
```

Expected success output:

```text
CAVRA Community GA path validation passed.
```

## GA Path Map

| Area | Public Evidence | User-Verifiable Check |
| --- | --- | --- |
| Policy | `docs/community-ga-release-checklist.md`, `docs/release-packets/community-ga-v0.1.0.json` | Policy signing, policy validation, runtime modes, and golden decisions are required Community GA gates. |
| Evidence | `docs/release-packets/community-ga-v0.1.0.md`, `docs/release-verifications/community-v0.1.0-post-release-verification.md` | Release packet and post-release verification show gate status, artifact checksums, install smoke, and public boundary status. |
| Console | `apps/sandbox-ui`, `docs/sandbox-portal-smoke-validation.md`, `docs/console-closeout-operator-experience.md` | Portal smoke validation and console closeout validation prove public routes, operator journeys, and documentation links remain coherent. |
| Go Runtime | `docs/release-packets/community-ga-v0.1.0.json`, `docs/go-backend-promotion.md` | Go runtime readiness is explicit. For Community GA v0.1.0, Go remains disabled/not promoted and Python remains authoritative. |
| Release Verification | `docs/releases/community-v0.1.0.md`, `docs/release-verifications/community-v0.1.0-post-release-verification.json`, `.github/workflows/verify-community-release.yml` | Release notes, artifact verification, README/wiki navigation, and manual verification workflow are linked. |

## Operator Runbook

1. Start with the current public release:
   `docs/releases/community-v0.1.0.md`.
2. Confirm the release packet:
   `docs/release-packets/community-ga-v0.1.0.json`.
3. Confirm post-release artifact verification:
   `docs/release-verifications/community-v0.1.0-post-release-verification.json`.
4. Run the public release validators:

   ```bash
   python scripts/validate-release-packets.py
   python scripts/validate-maintenance-release-evidence.py
   python scripts/validate-community-release-note-freshness.py
   python scripts/validate-community-release-index.py
   python scripts/validate-community-release-readiness-dashboard.py
   python scripts/validate-sandbox-portal.py
   python scripts/validate-console-closeout.py
   python scripts/validate-community-ga-path.py
   scripts/validate-boundaries.sh .
   ```

5. Confirm CI evidence in the public workflows:
   `.github/workflows/community-ci.yml`,
   `.github/workflows/security-scan.yml`,
   `.github/workflows/release-community.yml`, and
   `.github/workflows/cavra-governance.yml`.
6. Confirm GitHub Release artifacts exist at
   `https://github.com/Huzefaaa2/cavra/releases/tag/community-v0.1.0`.
7. Keep Go Runtime promoted only when readiness, promotion, rollback,
   rehearsal, and drill evidence are complete. Otherwise, treat disabled Go as
   the correct Community GA state.

## Public Boundary

This path is public Community Edition release evidence only. It does not expose
Enterprise source code, private policy packs, SaaS backend implementation,
license-service internals, customer evidence, private connector configuration,
provider credentials, private signing keys, billing records, or private trial
package paths.

## User Stories

- As a maintainer, I can verify the full Community GA story with one documented
  path before publishing release changes.
- As an auditor, I can trace Community GA from release notes to packet,
  verification evidence, console checks, and public boundary status.
- As a platform engineer, I can confirm policy, CI, console, and runtime
  readiness gates without needing private Enterprise repositories.
- As a CISO, I can see that Go Runtime promotion is explicit and not silently
  enabled without rollback and readiness evidence.

## Enterprise Challenge Solved

Regulated teams need proof that a release is not just tagged, but governed end
to end. This GA path turns CAVRA Community release evidence into a public,
repeatable audit trail that a buyer, maintainer, platform owner, or auditor can
verify without private access.

## Next Recommendation

Archive the post-publication Community v0.1.1 verifier output and begin the
next maintenance-release readiness slice.
