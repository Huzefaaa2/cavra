# Customer Closeout Handoff

The customer closeout handoff packet is the Managed and Enterprise bridge from
validated evidence-room readiness to customer-facing release and operating
review.

It is reference based and sanitized. It contains owner refs, communication refs,
operating-review refs, known-exclusion refs, and handoff controls only.

## Required Handoff Areas

- evidence-room readiness
- release owner
- customer success owner
- security owner
- release approver
- announcement reference
- evidence-room reference
- handoff ticket reference
- support path reference
- next operating review reference
- known exclusions

## Validate The Live Sanitized Handoff

```bash
python3 scripts/validate_customer_closeout_handoff.py \
  --packet examples/customer-closeout-handoff/customer-closeout-handoff.live.sanitized.example.json \
  --require-live
```

CLI equivalent:

```bash
cavra release customer-closeout-handoff \
  --packet examples/customer-closeout-handoff/customer-closeout-handoff.live.sanitized.example.json \
  --require-live
```

Completion condition:

```json
{
  "ready_for_customer_closeout_handoff": true,
  "blocker_count": 0,
  "warning_count": 0
}
```

## Operating Pattern

1. Validate customer-live evidence intake.
2. Validate the customer evidence-room index.
3. Validate the closeout handoff packet.
4. Deliver the customer announcement through the private deployment workflow.
5. Begin the recurring operating-review cadence.
