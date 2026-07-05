# Customer Lifecycle Executive Rollup

The customer lifecycle executive rollup is the R7.7 closeout gate for a Managed
or Enterprise customer lifecycle. It aggregates the sanitized Phase 7 customer
packets into one executive-safe record that can be reviewed without exposing
customer names, emails, private notes, pricing, contract values, raw contracts,
or raw evidence.

It follows:

- customer live evidence intake
- customer evidence-room closeout
- customer closeout handoff
- customer operating review
- customer renewal and expansion readiness
- customer renewal outcome closeout

The rollup is intentionally a control artifact, not a commercial record. Actual
customer evidence rooms, commercial terms, support records, and customer names
remain private deployment material.

## Generate Examples

```bash
python3 scripts/validate_customer_lifecycle_rollup.py \
  --export-dir dist/customer-lifecycle-rollup
```

CLI equivalent:

```bash
cavra release customer-lifecycle-rollup \
  --export-dir dist/customer-lifecycle-rollup
```

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

## Required Rollup Areas

- R7.1 customer live evidence intake
- R7.2 customer evidence-room closeout
- R7.3 customer closeout handoff
- R7.4 customer operating review
- R7.5 customer renewal and expansion readiness
- R7.6 customer renewal outcome closeout
- executive owner references
- implementation closeout summary
- operating health summary
- value realization summary
- risk and security summary
- renewal outcome summary
- expansion plan summary
- next lifecycle checkpoint

## Privacy Controls

The validator blocks public packets that contain commercial terms, contract
values, renewal amounts, customer names, customer emails, raw contracts, pricing,
or private notes. The public artifact should contain sanitized references,
readiness results, owner references, control states, and archive pointers only.
