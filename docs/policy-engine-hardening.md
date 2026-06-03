# Policy Engine Hardening

Phase 2 strengthens CAVRA policy behavior so regulated teams can trust policy decisions before enforcement expands.

## Delivered Capabilities

- Strict JSON Schema validation through `schemas/policy.schema.json`.
- Validation for policy metadata, filesystem rules, command rules, Git controls, MCP trust controls, compliance mappings, approval sections, and evidence sections.
- Policy inheritance with parent policy pack resolution through `metadata.inherits`.
- Overlay compilation for repository or business-unit policy overrides.
- Normalized compiled policy output for review, signing, and future parity tests.
- Semantic policy diff output that reports added, removed, and changed policy paths.
- Ed25519 local policy signing key generation through `cavra policy keygen`.
- Signature metadata files through `cavra policy sign`, including Ed25519 and backward-compatible HMAC modes.
- Signature verification through `cavra policy verify`, including digest mismatch, public-key fingerprint, and signature mismatch detection.
- Backward compatibility with legacy SHA-256 `.sig` files.

## CLI Usage

Validate one policy pack:

```bash
cavra policy validate policies/cavra-ai-agent-baseline
```

Compile a policy pack:

```bash
cavra policy compile --policy-pack cavra-ai-agent-baseline
```

Compile with an overlay:

```bash
cavra policy compile \
  --policy-pack cavra-ai-agent-baseline \
  --overlay .cavra/repository-policy.yaml
```

Compare two policy packs:

```bash
cavra policy diff policies/cavra-ai-agent-baseline policies/cavra-banking-baseline
```

Generate an Ed25519 keypair, then sign and verify a policy:

```bash
cavra policy keygen \
  --output .cavra/policy-signing \
  --key-id community-ga-policy-key

cavra policy sign policies/cavra-ai-agent-baseline/policy.yaml \
  --signer platform-security \
  --private-key .cavra/policy-signing/community-ga-policy-key.private.pem \
  --key-id community-ga-policy-key

cavra policy verify policies/cavra-ai-agent-baseline/policy.yaml \
  --public-key .cavra/policy-signing/community-ga-policy-key.public.pem
```

Legacy HMAC local tamper checks remain available through `--key`, but Ed25519
is the recommended Community GA policy signing workflow.

## Policy Inheritance

Policy packs can inherit from another pack:

```yaml
metadata:
  id: cavra-repository-prod
  title: Repository Production Policy
  description: Repository override for production service
  version: 1.0.0
  inherits: cavra-ai-agent-baseline
filesystem:
  require_approval_write:
    - "services/payment/**"
commands:
  block:
    - "kubectl apply*--context*prod*"
```

Inheritance merges list-based rules and preserves child metadata. This supports enterprise baseline, business-unit baseline, repository override, and exception layers.

## Enterprise Value

Policy hardening solves policy drift, weak review evidence, and untestable governance. Security and platform teams can validate policies before rollout, compile normalized policy output for review, compare changes semantically, and verify that policies were not modified after approval.

## User Stories

- As a platform engineer, I can validate every policy pack before rollout.
- As a CISO, I can require signed policy metadata before enforcement.
- As an auditor, I can compare policy changes and understand what control paths changed.
- As a repository owner, I can inherit enterprise defaults while adding local stricter controls.

## Validation

Phase 2 validation covers:

- All bundled policy packs validate against `schemas/policy.schema.json`.
- Policy inheritance merges parent and child controls.
- Policy diff reports added, removed, and changed paths.
- Policy signatures verify and detect tampering.
- Ed25519 policy signatures verify with a public key and fail on digest,
  fingerprint, or signature mismatch.
- Golden decision snapshots cover critical Community file, command, Git, MCP,
  and strict-mode decisions.
- CLI compile, validate, diff, sign, and verify commands run locally.

## Next Recommended Phase

Phase 3: Evidence Hub and Attestation.

The next production risk is evidence integrity. CAVRA should create signed evidence bundles with manifests, checksums, PR attestation, compliance mapping, and SIEM-ready event exports.
