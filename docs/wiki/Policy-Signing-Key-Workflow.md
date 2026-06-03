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

## Sign A Policy

```bash
cavra policy sign policies/cavra-ai-agent-baseline/policy.yaml \
  --signer platform-security \
  --private-key .cavra/policy-signing/community-ga-policy-key.private.pem \
  --key-id community-ga-policy-key
```

## Verify A Policy

```bash
cavra policy verify policies/cavra-ai-agent-baseline/policy.yaml \
  --public-key .cavra/policy-signing/community-ga-policy-key.public.pem
```

Use Ed25519 for GA signing workflows. Use HMAC only for local tamper checks or
legacy automation that has not migrated yet.
