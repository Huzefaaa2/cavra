# Release Signing Operations

CAVRA Go runtime release packages now include a public-safe signing operations manifest named `cavra-runtime.signing-operations.json`.

The manifest does not contain private keys, license secrets, customer material, or proprietary enterprise release logic. It records the release signing control model that operators and auditors need before a runtime package is promoted to developer workstations, CI runners, or air-gapped environments.

## What The Manifest Proves

`scripts/package_go_release.py` writes `cavra-runtime.signing-operations.json` before checksums, SLSA provenance, detached signatures, and release evidence are finalized. The package verifier treats this manifest as required release evidence.

The manifest records:

- Active signing key identifier through `active_key_id`.
- Signing algorithm, currently `Ed25519`.
- Whether signing is required for the release.
- Custody model for where private signing material must live.
- The public repository boundary for signing keys.
- Quarterly or incident-triggered key rotation policy.
- Replacement-key overlap guidance for planned rotations.
- Emergency revocation evidence requirements.
- Emergency actions for disabling a compromised signing secret and rebuilding replacement packages.

## Operator Workflow

Production signing keys must be stored outside this repository in an approved secret manager or GitHub Actions secret. The public repository only references the signing key by ID.

```bash
export CAVRA_GO_RELEASE_SIGNING_KEY="$(op read op://release/cavra-go-runtime/signing-key)"

python3 scripts/package_go_release.py \
  --dist dist/go-runtime \
  --version v0.1.0 \
  --commit "$GITHUB_SHA" \
  --ref "$GITHUB_REF" \
  --event release \
  --key-id cavra-go-release-2026-q2 \
  --signing-required
```

Each production release should attach the generated manifest to the release change record with:

- `release-evidence.json`
- `checksums.txt`
- `cavra-runtime.provenance.intoto.json`
- Detached `*.sig.json` signatures
- `offline-trust-root-bootstrap.json`
- `cavra-runtime.signing-operations.json`

## Verification

The verifier rejects a Go runtime package when the signing operations manifest is missing, lacks required controls, disagrees with checksums, mismatches release evidence, uses an unsupported algorithm, omits key custody boundaries, or lacks rotation and revocation evidence.

```bash
cavra release verify-go-package dist/go-runtime
```

Required controls:

- `release-signing-key-id-declared`
- `private-key-public-boundary-documented`
- `quarterly-key-rotation-policy`
- `incident-triggered-revocation-policy`
- `emergency-revocation-evidence-required`
- `replacement-key-overlap-guidance`
- `signed-release-evidence-required`

## Planned Key Rotation

During a planned rotation:

1. Create the replacement key in the approved secret manager.
2. Package the release with a new `--key-id`.
3. Publish release evidence with the new key ID.
4. Verify signatures from both old and new key IDs during the overlap window.
5. Retire the old key after all active release channels have moved.

The repository does not store the private key or the rotation secret. It stores only verifier-readable evidence that the release followed the rotation policy.

## Emergency Revocation

Emergency revocation is required when private-key exposure, unauthorized signing, or release tampering is suspected.

Required evidence:

- Revoked key ID
- Affected release versions
- Revocation timestamp
- Replacement key ID
- Operator approver
- New signed release evidence
- Customer advisory reference

Required actions:

- Disable the compromised signing secret.
- Remove affected release artifacts from promotion channels.
- Publish a revocation advisory.
- Rebuild and sign replacement packages with a new key ID.
- Verify replacement packages before promotion resumes.

## User Stories

- As a release manager, I can prove which signing key ID authorized a Go runtime release without exposing private signing material.
- As an auditor, I can verify that key rotation and emergency revocation procedures are part of every package.
- As a platform owner, I can block runtime promotion when a package lacks signing operations evidence.
- As an incident commander, I can identify the required revocation evidence before replacement packages are promoted.

## Enterprise Challenge Solved

Regulated enterprises need more than a signed binary. They need evidence that private keys are not in source control, release signing keys can rotate, and compromised keys can be revoked without improvising during an incident. CAVRA now packages those controls into verifier-enforced release metadata while preserving the open-core boundary.

## Next Work

The next recommended implementation step is to add acknowledgement audit delivery history filters and delivery health dashboards.
