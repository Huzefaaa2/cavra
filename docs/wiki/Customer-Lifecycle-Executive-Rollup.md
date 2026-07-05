# Customer Lifecycle Executive Rollup

The customer lifecycle executive rollup is the final R7 executive-safe packet
for Managed and Enterprise customer lifecycle review. It aggregates the sanitized
customer evidence intake, evidence room, handoff, operating review, renewal
readiness, and renewal outcome closeout gates into one reviewable status record.

It does not publish customer names, pricing, contract terms, private notes, raw
contracts, or raw evidence. Live customer material stays in the private customer
evidence room.

## Required Gates

- R7.1 customer live evidence intake
- R7.2 customer evidence-room closeout
- R7.3 customer closeout handoff
- R7.4 customer operating review
- R7.5 customer renewal and expansion readiness
- R7.6 customer renewal outcome closeout

## Validate The Live Sanitized Packet

```bash
python3 scripts/validate_customer_lifecycle_rollup.py \
  --packet examples/customer-lifecycle-rollup/customer-lifecycle-rollup.live.sanitized.example.json \
  --require-live
```

CLI equivalent:

```bash
cavra release customer-lifecycle-rollup \
  --packet examples/customer-lifecycle-rollup/customer-lifecycle-rollup.live.sanitized.example.json \
  --require-live
```

Completion condition:

```json
{
  "ready_for_customer_lifecycle_executive_rollup": true,
  "blocker_count": 0,
  "warning_count": 0
}
```
