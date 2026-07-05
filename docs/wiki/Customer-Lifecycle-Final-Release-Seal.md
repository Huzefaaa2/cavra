# Customer Lifecycle Final Release Seal

The customer lifecycle final release seal is the R7.10 phase-close packet for
CAVRA Managed and Enterprise customer lifecycle operations. It converts the
R7.9 public status summary and the earlier lifecycle artifacts into one final,
customer-safe release record.

Use it when the customer lifecycle is ready for final release-note mention,
customer success handoff, support handoff, archive verification, and public
status communication.

## Seal Chain

```mermaid
flowchart LR
  A[Live evidence intake] --> B[Evidence room]
  B --> C[Closeout handoff]
  C --> D[Operating review]
  D --> E[Renewal expansion]
  E --> F[Renewal outcome]
  F --> G[Executive rollup]
  G --> H[Archive manifest]
  H --> I[Public status]
  I --> J[Final release seal]
```

## Required Checks

- Live sanitized lifecycle public status is ready.
- Release, customer success, security, support, communications, and archive
  owner refs are present.
- Lifecycle public status, archive manifest, executive rollup, renewal outcome,
  operating review, evidence room, and live evidence intake are sealed.
- Release publication refs are sanitized.
- Final controls are true for release notes, handoffs, security acceptance,
  communications acceptance, and redaction boundaries.
- No customer identities, raw evidence, private notes, pricing, contract values,
  renewal amounts, raw contracts, or commercial terms are embedded.

## Run The Gate

```bash
python3 scripts/validate_customer_lifecycle_final_seal.py \
  --packet examples/customer-lifecycle-final-seal/customer-lifecycle-final-seal.live.sanitized.example.json \
  --require-live
```

Ready means:

```json
{
  "ready_for_customer_lifecycle_final_release_seal": true,
  "blocker_count": 0,
  "warning_count": 0
}
```

## Related Files

- `src/cavra/customer_lifecycle_final_seal.py`
- `scripts/validate_customer_lifecycle_final_seal.py`
- `examples/customer-lifecycle-final-seal/`
- `.github/workflows/customer-lifecycle-final-seal.yml`
- `tests/test_customer_lifecycle_final_seal.py`
