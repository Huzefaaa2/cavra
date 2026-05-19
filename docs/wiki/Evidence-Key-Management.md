# Evidence Key Management

CAVRA evidence bundles can be signed with Ed25519 keys and verified through a public key or trust-root document.

## Production Flow

```bash
cavra evidence generate-keypair --private-key .cavra/keys/prod-private.pem --public-key .cavra/keys/prod-public.pem
cavra evidence trust-root .cavra/keys/prod-public.pem --output .cavra/keys/prod-trust-root.json --key-id prod-evidence-2026-q2
cavra evidence trust-bundle .cavra/keys/prod-trust-root.json --output .cavra/keys/evidence-trust-roots.json
cavra evidence trust-distribution .cavra/keys/prod-trust-root.json --output .cavra/keys/trust-root-distribution --distribution-id prod-trust-roots-2026-q2
cavra evidence bundle --output .cavra/evidence/latest --private-key .cavra/keys/prod-private.pem --key-id prod-evidence-2026-q2
cavra evidence verify .cavra/evidence/latest --trust-root .cavra/keys/evidence-trust-roots.json --key-id prod-evidence-2026-q2
```

## Rotation Guidance

- Generate a new keypair before rotation.
- Publish the updated trust-root distribution package before signing release evidence.
- Keep retired trust roots for historical verification.
- Mark compromised keys as `revoked`.
- Do not commit private keys.

See repository source page: `docs/evidence-key-management.md`.
