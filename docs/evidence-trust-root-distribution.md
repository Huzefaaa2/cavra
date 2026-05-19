# Evidence Trust-Root Distribution

CAVRA evidence trust roots let reviewers and automation verify Ed25519-signed evidence without access to private signing keys.

## Production Flow

1. Platform Security generates an Ed25519 keypair in a controlled environment.
2. Platform Security exports a trust root from the public key.
3. Release Engineering combines active and historical trust roots into a trust-root bundle.
4. Release Engineering exports an offline trust-root distribution package.
5. CI, reviewer workstations, API services, and audit jobs consume the same trust-root bundle.
6. Evidence verification requires the expected `key_id` and rejects revoked or mismatched keys.

```bash
cavra evidence generate-keypair \
  --private-key .cavra/keys/prod-private.pem \
  --public-key .cavra/keys/prod-public.pem

cavra evidence trust-root .cavra/keys/prod-public.pem \
  --output .cavra/keys/prod-trust-root.json \
  --key-id prod-evidence-2026-q2 \
  --owner platform-security

cavra evidence trust-bundle .cavra/keys/prod-trust-root.json \
  --output .cavra/keys/evidence-trust-roots.json

cavra evidence trust-distribution .cavra/keys/prod-trust-root.json \
  --output .cavra/keys/trust-root-distribution \
  --environment regulated-prod \
  --distribution-id prod-trust-roots-2026-q2 \
  --channel source-control \
  --channel offline-media

cavra evidence verify .cavra/evidence/latest \
  --trust-root .cavra/keys/evidence-trust-roots.json \
  --key-id prod-evidence-2026-q2 \
  --minimum-retention-days 2555
```

## Distribution Package

`cavra evidence trust-distribution` writes:

- `evidence-trust-roots.json`: public trust-root bundle for verification.
- `trust-root-distribution-manifest.json`: distribution metadata, environment, channels, key summaries, and operator steps.
- `trust-root-distribution.md`: human-readable operator handoff.
- `checksums.txt`: SHA-256 checksums for the distribution artifacts.

The package is public trust material only. It must never include private evidence-signing keys.

## Enterprise Controls

- Store private keys in a KMS, HSM, or sealed CI secret store.
- Store trust-root distribution packages in source control or governed configuration.
- Require approval before adding, retiring, or revoking production trust roots.
- Distribute and checksum-verify the new bundle before signing evidence with a new key.
- Keep retired roots for historical evidence verification.
- Mark compromised roots as `revoked` and investigate all matching signatures.

## User Stories

- As an auditor, I can verify historical evidence with the public trust-root bundle.
- As a platform security engineer, I can rotate signing keys without breaking old attestations.
- As a release manager, I can require evidence to be signed by the approved production key ID.
- As an offline environment operator, I can import one documented trust-root package with checksums and approved distribution channels.

## Enterprise Value

Trust-root distribution packages make evidence verification repeatable across CI, reviewers, security operations, audit, and restricted networks. They reduce the risk that AI-agent activity is accepted without proof of origin, integrity, approved retention, and approved trust material distribution.
