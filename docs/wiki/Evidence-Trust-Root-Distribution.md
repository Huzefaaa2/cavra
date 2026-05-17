# Evidence Trust-Root Distribution

CAVRA supports distributable evidence trust-root bundles for Ed25519 evidence verification.

## How It Works

```bash
cavra evidence trust-root .cavra/keys/prod-public.pem \
  --output .cavra/keys/prod-trust-root.json \
  --key-id prod-evidence-2026-q2

cavra evidence trust-bundle .cavra/keys/prod-trust-root.json \
  --output .cavra/keys/evidence-trust-roots.json

cavra evidence verify .cavra/evidence/latest \
  --trust-root .cavra/keys/evidence-trust-roots.json \
  --key-id prod-evidence-2026-q2
```

## User Stories

- As an auditor, I can verify historical evidence with public trust roots.
- As Platform Security, I can rotate signing keys without breaking old evidence.
- As Release Engineering, I can enforce approved key IDs in CI and PR review.

## Enterprise Challenge Solved

Trust-root bundles give every verifier the same approved signing-key set. This reduces ambiguity around evidence origin, key rotation, historical verification, and revoked keys.

See repository source page: `docs/evidence-trust-root-distribution.md`.
