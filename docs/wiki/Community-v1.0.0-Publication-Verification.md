# Community v1.0.0 Publication Readiness Verification

This wiki page mirrors the public publication readiness verification for the
CAVRA Community v1.0.0 GA publication package. The package metadata is bumped
to `1.0.0`; final GitHub Release artifacts are not published yet.

## Release Metadata

| Field | Value |
| --- | --- |
| Release | CAVRA Community v1.0.0 |
| State | `dry-run-publication-ready` |
| Tag | `community-v1.0.0` |
| Package version | `1.0.0` |
| Planned GitHub Release | <https://github.com/Huzefaaa2/cavra/releases/tag/community-v1.0.0> |
| Release notes | `docs/releases/community-v1.0.0.md` |
| Publication package | `docs/community-v1.0.0-ga-publication-package.md` |

## Gate Summary

| Gate | Status | Evidence |
| --- | --- | --- |
| RC1 feedback baseline | Pass | `docs/release-verifications/community-v1.0.0-rc.1-post-publication-verification.md` |
| Node 24 readiness baseline | Pass | Current Community workflows use Node 24-ready action versions. |
| Package metadata | Pass | `pyproject.toml` and `src/cavra/__init__.py` use `1.0.0`. |
| Final release notes | Pass | `docs/releases/community-v1.0.0.md` |
| Artifact build plan | Pass | `docs/community-v1.0.0-ga-publication-package.md` |
| Verifier inputs | Pass | Planned tag, version, wheel checksum, and source distribution checksum inputs are documented. |
| Announcement approval evidence | Pass | Draft public announcement and approval checks are documented. |
| Pre-publication wheel smoke | Pass | Local clean virtualenv install returned `cavra 1.0.0`. |
| Artifact checksums | Warn | Pending final `community-v1.0.0` artifacts and SHA-256 checksums. |
| Provenance evidence | Warn | Pending final provenance metadata. |
| Signature or keyless attestation evidence | Warn | Pending final signature or attestation evidence. |
| Install smoke | Warn | Pending clean install smoke from the final wheel and source distribution. |
| Public boundary | Pass | Enterprise source code, paid policy packs, private signing keys, private registry credentials, license-service secrets, and customer records are excluded. |

## Validation

```bash
python3 scripts/validate-community-v100-ga-publication-package.py
```

## Decision

Decision: approve final GA artifact publication preparation.

## Next Recommendation

Merge the Community v1.0.0 metadata bump, create the community-v1.0.0 tag from main, build and upload final GitHub Release assets, then record final checksums, provenance, verifier defaults, and post-publication verification.
