# Evidence Trust-Root Distribution

CAVRA evidence trust roots let reviewers and automation verify Ed25519-signed evidence without access to private signing keys.

## Production Flow

1. Platform Security generates an Ed25519 keypair in a controlled environment.
2. Platform Security exports a trust root from the public key.
3. Release Engineering combines active and historical trust roots into a trust-root bundle.
4. CI, reviewer workstations, API services, and audit jobs consume the same trust-root bundle.
5. Evidence verification requires the expected `key_id` and rejects revoked or mismatched keys.

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

cavra evidence verify .cavra/evidence/latest \
  --trust-root .cavra/keys/evidence-trust-roots.json \
  --key-id prod-evidence-2026-q2 \
  --minimum-retention-days 2555
```

## Enterprise Controls

- Store private keys in a KMS, HSM, or sealed CI secret store.
- Store trust-root bundles in source control or governed configuration.
- Require approval before adding, retiring, or revoking production trust roots.
- Distribute the new bundle before signing evidence with a new key.
- Keep retired roots for historical evidence verification.
- Mark compromised roots as `revoked` and investigate all matching signatures.

## User Stories

- As an auditor, I can verify historical evidence with the public trust-root bundle.
- As a platform security engineer, I can rotate signing keys without breaking old attestations.
- As a release manager, I can require evidence to be signed by the approved production key ID.

## Enterprise Value

Trust-root bundles make evidence verification repeatable across CI, reviewers, security operations, and audit. They reduce the risk that AI-agent activity is accepted without proof of origin, integrity, and approved retention.
