# Evidence Trust-Root Distribution

CAVRA supports distributable evidence trust-root packages for Ed25519 evidence verification in CI, reviewer workstations, API services, audit tooling, and offline environments.

## How It Works

```bash
cavra evidence trust-root .cavra/keys/prod-public.pem \
  --output .cavra/keys/prod-trust-root.json \
  --key-id prod-evidence-2026-q2

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
  --key-id prod-evidence-2026-q2
```

The distribution command writes `evidence-trust-roots.json`, `trust-root-distribution-manifest.json`, `trust-root-distribution.md`, and `checksums.txt`.

## User Stories

- As an auditor, I can verify historical evidence with public trust roots.
- As Platform Security, I can rotate signing keys without breaking old evidence.
- As Release Engineering, I can enforce approved key IDs in CI and PR review.
- As an offline operator, I can import one documented package with checksums and approved distribution channels.

## Enterprise Challenge Solved

Trust-root distribution packages give every verifier the same approved signing-key set and checksum-protected operator handoff. This reduces ambiguity around evidence origin, key rotation, historical verification, revoked keys, and restricted-network import.

See repository source page: `docs/evidence-trust-root-distribution.md`.
