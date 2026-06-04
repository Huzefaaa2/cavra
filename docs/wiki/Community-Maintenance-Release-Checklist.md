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
| Python package metadata | `scripts/validate-python-package-metadata.py` | Build output has no setuptools metadata warnings, `twine check` passes, BUSL-1.1 license metadata is present, project URLs are declared, and packaged schemas are included. |
| Release workflow guards | `.github/workflows/publish-pypi.yml` and `.github/workflows/go-release.yml` | PyPI publishing only runs for manual dispatch or `pypi-v*` releases, and Go runtime release packaging only runs for manual dispatch or `go-runtime-v*` releases. |
| Artifact checksums | Release artifacts and verification packet | Wheel and source distribution checksums match release metadata. |
| Install smoke | Clean virtual environment | Wheel installs and `cavra version` returns the expected version. |
| Public boundary | `scripts/validate-boundaries.sh .` | No prohibited Enterprise, customer, private key, or paid policy-pack material is present. |
| CI evidence | Required GitHub checks | Community CI, security scan, required check, CodeQL, and test matrix complete successfully. |

## Required Evidence Packet

Every maintenance release should include a machine-readable JSON evidence
packet. The schema is maintained at
`docs/release-verifications/community-maintenance-release.schema.json`, with a
safe example at
`examples/release-verifications/community-maintenance-release.example.json`.

## Next Recommendation

Convert Community v0.1.2 dry-run into an official maintenance release after maintainer approval and artifact publication.
