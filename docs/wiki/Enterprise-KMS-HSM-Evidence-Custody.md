# Enterprise KMS/HSM Evidence Custody

CAVRA R3.1 defines a public-safe KMS/HSM evidence signing, key rotation, custody policy, revocation, and independent verifier readiness contract for Enterprise and Managed deployments.

R3.1 is public-repository complete. The closeout boundary is documented in [Enterprise KMS/HSM Evidence Custody R3.1 Closeout](Enterprise-KMS-HSM-Evidence-Custody-R3.1-Closeout.md). Real KMS/HSM key identifiers, signer logs, operator approvals, custody exports, revocation transcripts, verifier handoff packets, provider account details, and tenant evidence remain Managed or Enterprise evidence-room records.

## Implemented Foundation

| Component | Purpose |
| --- | --- |
| `build_enterprise_evidence_custody_contract` | Defines supported signing providers, algorithms, custody boundaries, rotation cadence, and verifier commands. |
| `validate_enterprise_evidence_custody_packet` | Validates sample or live KMS/HSM custody evidence packets. |
| `scripts/validate_enterprise_evidence_custody.py` | CLI validator for public sample packets and private live packets. |
| `examples/evidence/enterprise-evidence-custody.sample.json` | Public-safe packet showing the expected evidence shape. |
| `examples/evidence/enterprise-evidence-custody.live.sanitized.example.json` | Sanitized live-mode example that passes `--require-live` without exposing real customer infrastructure. |
| `.github/workflows/enterprise-evidence-custody.yml` | CI workflow for sample validation and manual strict live validation. |
| `tests/test_evidence_custody.py` | Contract, sample, live-mode, blocker, and workflow tests. |

## Required Evidence

- External KMS, HSM, Vault Transit, or PKCS#11 signing provider.
- Non-exportable private signing keys.
- Dual-control custody and separation of duties.
- Rotation cadence of 90 days or less.
- Rotation overlap of at least 7 days.
- Retired keys retained for historical verification.
- Emergency revocation drill evidence.
- Public trust-root distribution for independent verifiers.
- Offline evidence bundle and PR attestation verification.

## Validation

Public/sample validation:

```bash
python3 scripts/validate_enterprise_evidence_custody.py \
  --packet examples/evidence/enterprise-evidence-custody.sample.json \
  --output dist/test/enterprise-evidence-custody-sample.json
```

Private live validation:

```bash
python3 scripts/validate_enterprise_evidence_custody.py \
  --packet .cavra/enterprise/enterprise-evidence-custody-live.json \
  --require-live \
  --output dist/enterprise/enterprise-evidence-custody-result.json
```

Sanitized live-mode template validation:

```bash
python3 scripts/validate_enterprise_evidence_custody.py \
  --packet examples/evidence/enterprise-evidence-custody.live.sanitized.example.json \
  --require-live
```

R3.1 is public-repository complete when the sample and sanitized live-mode packet validate, tests pass, and the closeout boundary is documented. A specific Managed or Enterprise deployment is production-complete only when its private live packet returns `ready_for_enterprise_live_evidence_custody: true`, `blocker_count: 0`, and `warning_count: 0`.

Detailed repo document: [Enterprise KMS/HSM Evidence Custody](https://github.com/Huzefaaa2/cavra/blob/main/docs/evidence-kms-hsm-custody.md).
