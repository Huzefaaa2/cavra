# Customer Renewal And Expansion Readiness

The customer renewal and expansion readiness packet validates that a Managed or
Enterprise customer has enough operating evidence to renew confidently and
evaluate expansion opportunities.

It is sanitized and reference based. It checks value realization, adoption
depth, AISPM posture continuity, unresolved risk, expansion candidates, and the
commercial handoff.

## Required Areas

- operating review readiness
- account owner
- customer success owner
- commercial owner
- security owner
- executive sponsor
- value realization
- adoption depth
- posture continuity
- unresolved risk
- expansion candidates
- commercial handoff
- next checkpoint

## Validate The Live Sanitized Packet

```bash
python3 scripts/validate_customer_renewal_expansion.py \
  --packet examples/customer-renewal-expansion/customer-renewal-expansion.live.sanitized.example.json \
  --require-live
```

CLI equivalent:

```bash
cavra release customer-renewal-expansion \
  --packet examples/customer-renewal-expansion/customer-renewal-expansion.live.sanitized.example.json \
  --require-live
```

Completion condition:

```json
{
  "ready_for_customer_renewal_expansion": true,
  "blocker_count": 0,
  "warning_count": 0
}
```
