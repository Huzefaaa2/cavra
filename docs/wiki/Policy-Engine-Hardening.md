# Policy Engine Hardening

Phase 2 is complete.

## What Changed

CAVRA policy behavior is now stricter and more reviewable:

- JSON Schema validation for policy packs.
- Policy inheritance with `metadata.inherits`.
- Normalized policy compilation.
- Semantic policy diff output.
- Policy signature metadata.
- Policy verification with tamper detection.

## Commands

```bash
cavra policy validate policies/cavra-ai-agent-baseline
cavra policy compile --policy-pack cavra-ai-agent-baseline
cavra policy diff policies/cavra-ai-agent-baseline policies/cavra-banking-baseline
cavra policy sign policies/cavra-ai-agent-baseline/policy.yaml --signer platform-security
cavra policy verify policies/cavra-ai-agent-baseline/policy.yaml
```

## Enterprise Value

Policy hardening gives platform and security teams a defensible policy lifecycle. Policies can be validated before rollout, compiled for review, compared semantically, inherited by repository-specific overlays, and verified against tampering after approval.

## User Stories

- As a platform engineer, I can validate all policy packs before rollout.
- As a CISO, I can prove which policy version governed a repository.
- As an auditor, I can compare policy changes by control path.
- As a repository owner, I can inherit enterprise policy while adding stricter local controls.

## Next Phase

Phase 3: Evidence Hub and Attestation.
