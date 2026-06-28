# Community GA Control Hardening Sync

This public-safe sync records the first Community GA Control Hardening batch.

## Delivered

- Ed25519 policy signing key generation through `cavra policy keygen`.
- Ed25519 policy signing through `cavra policy sign --private-key`.
- Ed25519 policy verification through `cavra policy verify --public-key`.
- Backward-compatible HMAC policy signature support.
- Golden decision snapshot coverage for critical Community decisions.
- Explicit runtime policy mode summaries for `audit_only`, `enforce`, `strict`,
  and `break_glass`.
- Production deployment guide validation updates for the public Community path.
- README, roadmap, docs, and wiki-source synchronization.

## Public Boundary

This batch does not include Enterprise source code, customer keys, production
private keys, customer policy packs, paid policy packs, KMS/HSM identifiers,
private approval-router integrations, license-service implementation, SaaS
backend source, customer evidence, or production provisioning records.

## Next Recommendation

Continue Community GA Control Hardening with production deployment validation
automation for the public Community install path.
