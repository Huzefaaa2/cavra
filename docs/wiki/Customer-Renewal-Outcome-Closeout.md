# Customer Renewal Outcome Closeout

The customer renewal outcome closeout packet validates that a Managed or
Enterprise renewal cycle has produced a sanitized, reviewable outcome without
publishing customer names, pricing, contract terms, private notes, or raw
evidence.

It follows [Customer Renewal And Expansion Readiness](Customer-Renewal-And-Expansion-Readiness.md)
and proves that the lifecycle can move from renewal readiness into outcome
archive, expansion activation, and the next customer-success operating cycle.

## Required Areas

- renewal readiness result
- account owner
- customer success owner
- commercial owner
- security owner
- executive sponsor
- finance operations owner
- renewal decision
- expansion decisions
- risk closeout
- value confirmation
- contract handoff
- lifecycle archive
- next success plan

## Validate The Live Sanitized Packet

```bash
python3 scripts/validate_customer_renewal_outcome.py \
  --packet examples/customer-renewal-outcome/customer-renewal-outcome.live.sanitized.example.json \
  --require-live
```

CLI equivalent:

```bash
cavra release customer-renewal-outcome \
  --packet examples/customer-renewal-outcome/customer-renewal-outcome.live.sanitized.example.json \
  --require-live
```

Completion condition:

```json
{
  "ready_for_customer_renewal_outcome_closeout": true,
  "blocker_count": 0,
  "warning_count": 0
}
```
