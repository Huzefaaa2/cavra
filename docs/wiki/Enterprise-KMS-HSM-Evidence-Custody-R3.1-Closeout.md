# Enterprise KMS/HSM Evidence Custody R3.1 Closeout

R3.1 is closed for the public CAVRA repository. The public implementation now includes the custody contract, validator, sample packet, sanitized live-mode packet, strict live workflow, documentation, and tests required to prove the KMS/HSM evidence custody boundary.

Real provider key IDs, signer logs, operator approvals, custody reviews, revocation drill records, trust-root distribution records, verifier handoff evidence, tenant names, and customer account details remain private Managed or Enterprise evidence-room artifacts.

## Complete Public Artifacts

| Artifact | Purpose |
| --- | --- |
| `src/cavra/evidence_custody.py` | KMS/HSM evidence custody contract and readiness checks. |
| `scripts/validate_enterprise_evidence_custody.py` | CLI validator for sample, sanitized live, and private live packets. |
| `examples/evidence/enterprise-evidence-custody.sample.json` | Public sample packet. |
| `examples/evidence/enterprise-evidence-custody.live.sanitized.example.json` | Sanitized live-mode packet that passes `--require-live`. |
| `.github/workflows/enterprise-evidence-custody.yml` | Sample and strict live workflow gate. |
| `tests/test_evidence_custody.py` | Contract, blocker, live-mode, workflow, and closeout documentation tests. |

## Verification

```bash
python3 scripts/validate_enterprise_evidence_custody.py \
  --packet examples/evidence/enterprise-evidence-custody.sample.json \
  --output dist/test/enterprise-evidence-custody-sample.json

python3 scripts/validate_enterprise_evidence_custody.py \
  --packet examples/evidence/enterprise-evidence-custody.live.sanitized.example.json \
  --require-live \
  --output dist/test/enterprise-evidence-custody-live-sanitized-result.json

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

## Handoff

R3.2 immutable append-only audit logging inherits the R3.1 custody assumptions for signing, trust-root distribution, retired-key verification, revocation handling, and independent verifier access.

Detailed repo document: [CAVRA Enterprise KMS/HSM Evidence Custody R3.1 Closeout](https://github.com/Huzefaaa2/cavra/blob/main/docs/evidence-custody-r3-closeout.md).
