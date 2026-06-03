# Policy Signing Key Workflow

This public Community workflow hardens policy integrity for CAVRA GA readiness.
It supports local Ed25519 policy signing while preserving the existing HMAC
signature metadata path for local tamper checks.

## Boundary

The public repository may include signing commands, public-key verification
guidance, and synthetic examples. It must not contain production private keys,
customer signing keys, KMS/HSM identifiers, Enterprise approval workflows,
customer policy packs, paid policy packs, or private signing-service
implementation details.

## Generate A Local Keypair

```bash
cavra policy keygen \
  --output .cavra/policy-signing \
  --key-id community-ga-policy-key
```

This writes:

- `.cavra/policy-signing/community-ga-policy-key.private.pem`
- `.cavra/policy-signing/community-ga-policy-key.public.pem`

Store private keys in an operator-managed secret store. Commit only approved
public trust material when your governance process allows it.

## Sign A Policy

```bash
cavra policy sign policies/cavra-ai-agent-baseline/policy.yaml \
  --signer platform-security \
  --private-key .cavra/policy-signing/community-ga-policy-key.private.pem \
  --key-id community-ga-policy-key
```

The command writes `policy.yaml.sig.json` with:

- schema version;
- `Ed25519` algorithm;
- policy SHA-256 digest;
- key identifier;
- public-key fingerprint;
- signer;
- signature value.

## Verify A Policy

```bash
cavra policy verify policies/cavra-ai-agent-baseline/policy.yaml \
  --public-key .cavra/policy-signing/community-ga-policy-key.public.pem
```

Verification fails when:

- the policy digest changed after signing;
- the public key is missing for Ed25519 signatures;
- the public-key fingerprint does not match the signature metadata;
- the signature bytes do not verify.

## HMAC Compatibility

Existing local HMAC signing remains supported:

```bash
cavra policy sign policies/cavra-ai-agent-baseline/policy.yaml \
  --signer platform-security \
  --key "$CAVRA_POLICY_SIGNING_KEY"

cavra policy verify policies/cavra-ai-agent-baseline/policy.yaml \
  --key "$CAVRA_POLICY_SIGNING_KEY"
```

Use Ed25519 for GA signing workflows. Use HMAC only for local tamper checks or
legacy automation that has not migrated yet.

## User Stories

- As a platform engineer, I can sign policy packs with an asymmetric key before
  rollout.
- As a reviewer, I can verify policy integrity without access to the signing
  private key.
- As an auditor, I can see the signer, key ID, digest, algorithm, and
  verification outcome.

## Next Step

Continue Community GA Control Hardening with the golden decision snapshot suite,
runtime mode hardening, production deployment guide validation, and docs/wiki
sync.
