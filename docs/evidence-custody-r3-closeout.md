# CAVRA Enterprise KMS/HSM Evidence Custody R3.1 Closeout

Last updated: 2026-07-07

R3.1 is closed for the public CAVRA repository. The repo now contains the KMS/HSM evidence custody contract, validator, sample packet, sanitized live-mode packet, strict CI gate, docs, and tests needed to prove the implementation boundary without exposing real customer custody data.

Real KMS/HSM key identifiers, signer logs, operator approvals, custody review exports, revocation drill transcripts, verifier handoff packets, provider account details, tenant names, and customer evidence-room records belong to Managed or Enterprise deployment evidence rooms, not public source.

## What Is Complete

- Evidence custody contract for KMS, managed HSM, Vault Transit, and PKCS#11-style signing providers.
- Readiness validator for sample and live evidence custody packets.
- Public-safe sample custody packet.
- Sanitized live-mode packet at `examples/evidence/enterprise-evidence-custody.live.sanitized.example.json`.
- Strict live validation workflow for public-safe live-mode validation.
- Supported provider, algorithm, and custody boundary checks.
- Non-exportable private key and external signing enforcement checks.
- Dual-control custody, separation-of-duties, and break-glass policy checks.
- Rotation cadence, overlap, historical verification retention, and emergency revocation drill checks.
- Trust-root distribution, checksum, retired-key, and verifier access checks.
- Independent verifier and PR attestation verification checks.
- Audit evidence references for custody review, rotation approval, revocation drill, and verifier handoff.

## Evidence Boundary

Public evidence proves the implementation contract, validation behavior, and sanitized live readiness path. Private Enterprise and Managed deployments attach the real provider references, signer logs, HSM/KMS administrator evidence, rotation approvals, revocation drill records, trust-root distribution artifacts, and independent verifier handoff evidence.

## Verification

Public sample contract validation:

```bash
python3 scripts/validate_enterprise_evidence_custody.py \
  --packet examples/evidence/enterprise-evidence-custody.sample.json \
  --output dist/test/enterprise-evidence-custody-sample.json
```

Sanitized live-style validation:

```bash
python3 scripts/validate_enterprise_evidence_custody.py \
  --packet examples/evidence/enterprise-evidence-custody.live.sanitized.example.json \
  --require-live \
  --output dist/test/enterprise-evidence-custody-live-sanitized-result.json
```

Tests:

```bash
python3 -m pytest tests/test_evidence_custody.py -q
python3 -m ruff check src/cavra/evidence_custody.py scripts/validate_enterprise_evidence_custody.py tests/test_evidence_custody.py
```

Expected sanitized live-style result:

```json
{
  "ready_for_enterprise_live_evidence_custody": true,
  "status": "ready",
  "blocker_count": 0,
  "warning_count": 0
}
```

## R3.2 Handoff

R3.2 immutable append-only audit logging must consume the same custody assumptions: non-exportable signing keys, trust-root distribution, retired-key verification, revocation handling, independent verifier commands, and private evidence-room ownership for real customer provider logs.
