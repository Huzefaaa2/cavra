# Evidence Key Management

CAVRA evidence bundles can be signed with Ed25519 keys and verified through either a public key or a trust-root document.

## Key IDs

Each Ed25519 manifest signature includes:

- `algorithm`: `Ed25519`
- `key_id`: a stable signing-key identifier
- `public_key_sha256`: SHA-256 fingerprint of the public key PEM
- `value`: base64-encoded signature

Use explicit key IDs for production keys:

```bash
cavra evidence generate-keypair \
  --private-key .cavra/keys/prod-evidence-private.pem \
  --public-key .cavra/keys/prod-evidence-public.pem

cavra evidence trust-root .cavra/keys/prod-evidence-public.pem \
  --output .cavra/keys/prod-evidence-trust-root.json \
  --key-id prod-evidence-2026-q2 \
  --owner platform-security

cavra evidence trust-bundle .cavra/keys/prod-evidence-trust-root.json \
  --output .cavra/keys/evidence-trust-roots.json

cavra evidence bundle \
  --output .cavra/evidence/latest \
  --private-key .cavra/keys/prod-evidence-private.pem \
  --key-id prod-evidence-2026-q2

cavra evidence verify .cavra/evidence/latest \
  --trust-root .cavra/keys/evidence-trust-roots.json \
  --key-id prod-evidence-2026-q2
```

## Trust Roots

A trust root is a JSON document that records the trusted public key, key ID, owner, status, fingerprint, and validity window. Store trust roots in source control or a governed configuration repository. Do not store private keys in the repository.

A trust-root bundle is a distributable JSON document containing one or more trust roots. Use it when production services, CI checks, reviewer workstations, and audit tooling need the same set of active, retired, and historical verification keys. CAVRA rejects duplicate key IDs in a bundle.

Supported trust-root statuses:

- `active`: accepted for new evidence.
- `retired`: should not sign new evidence, but may be retained for historical verification.
- `revoked`: should fail verification and trigger investigation.

## Rotation Guidance

Recommended production rotation:

1. Generate a new Ed25519 keypair.
2. Create a new trust-root document with a new `key_id`.
3. Add the trust root to the trust-root bundle.
4. Distribute the public trust-root bundle before the new key signs release evidence.
5. Sign new evidence with the new key ID.
6. Keep old trust roots for historical bundle verification.
7. Mark compromised keys as `revoked`.
8. Rotate keys at least quarterly for regulated release evidence or immediately after suspected exposure.

## Verification Guidance

For regulated pull requests, reviewers should verify:

- Manifest checksums.
- Ed25519 signature through a trust root.
- Expected key ID.
- Minimum retention period.
- PR attestation report.

```bash
cavra evidence verify .cavra/evidence/latest \
  --trust-root .cavra/keys/prod-evidence-trust-root.json \
  --key-id prod-evidence-2026-q2 \
  --minimum-retention-days 2555

cavra evidence verify-attestation .cavra/evidence/latest \
  --output .cavra/evidence/attestation
```
