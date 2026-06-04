# Community Maintenance Release Checklist

This checklist governs public CAVRA Community maintenance releases after the
first Community GA publication. It makes every future Community tag repeatable,
auditable, and safe to announce without relying on private Enterprise evidence.

## Scope

Use this checklist for public Community Edition patch, minor, and maintenance
releases. It does not approve Enterprise source code, trial-only packages, paid
policy packs, SaaS backend artifacts, license-service internals, customer
records, private signing keys, private deployment evidence, or private container
registries.

## Required Gates

| Gate | Required Evidence | Pass Condition |
| --- | --- | --- |
| Release notes | `docs/releases/<version>.md` | Notes describe the public Community change, artifact links, verification status, and boundary notice. |
| Changelog | `CHANGELOG.md` | The release has a dated entry or an unreleased entry ready to move when tagged. |
| README link | `README.md` | README links the release notes, verification packet, and release page. |
| Wiki link | `docs/wiki/Home.md` and live wiki | Wiki navigation links release notes, verification packet, and runbook pages. |
| Verification workflow | `Verify Community Release` | Manual workflow runs against the tag, version, and expected artifact checksums. |
| Artifact checksums | Release artifacts and verification packet | Wheel and source distribution checksums match release metadata. |
| Install smoke | Clean virtual environment | Wheel installs and `cavra version` returns the expected version. |
| Public boundary | `scripts/validate-boundaries.sh .` | No prohibited Enterprise, customer, private key, or paid policy-pack material is present. |
| CI evidence | Required GitHub checks | Community CI, security scan, required check, CodeQL, and test matrix complete successfully. |

## Operator Runbook

1. Prepare the release notes:

   ```bash
   $EDITOR docs/releases/community-vX.Y.Z.md
   ```

2. Update README, changelog, roadmap status, and wiki-ready pages.

3. Build and publish the public Community release artifacts using the public
   release workflow.

4. Run the manual verification workflow:

   ```text
   GitHub Actions -> Verify Community Release -> Run workflow
   ```

5. Record the verification result:

   ```bash
   python3 scripts/verify-community-release-artifacts.py \
     --tag community-vX.Y.Z \
     --version X.Y.Z \
     --wheel-sha256 <expected-wheel-sha256> \
     --sdist-sha256 <expected-sdist-sha256>
   ```

6. Create a maintenance-release evidence packet under
   `docs/release-verifications/` using the template in
   `docs/community-maintenance-release-evidence-template.md`.

7. Validate public release evidence:

   ```bash
   python3 scripts/validate-maintenance-release-evidence.py
   python3 scripts/validate-release-packets.py
   bash scripts/validate-boundaries.sh .
   python3 -m pytest -q
   ```

8. Sync the live wiki after merge.

## Release States

`ready_for_publication`: all required gates pass, artifacts are verified, docs
are linked, and there are no accepted risks.

`ready_with_accepted_risk`: no public-boundary or artifact-integrity blockers
exist, but a low-risk documentation or announcement follow-up has an owner,
expiry date, and compensating control.

`blocked`: checksum verification fails, install smoke fails, public boundary
validation fails, required GitHub checks fail, release notes are missing, or
README/wiki links are stale.

## Required Evidence Packet

Every maintenance release should include a machine-readable JSON evidence
packet. The schema is maintained at
`docs/release-verifications/community-maintenance-release.schema.json`, with a
safe example at
`examples/release-verifications/community-maintenance-release.example.json`.

## Next Recommendation

Create a Community release index page that summarizes public Community tags,
release notes, verification packets, publication state, and next action.
