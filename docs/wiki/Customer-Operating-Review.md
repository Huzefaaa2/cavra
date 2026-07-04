# Customer Operating Review

The customer operating review packet is the recurring post-closeout Managed and
Enterprise health gate.

It is sanitized and reference based. It verifies that success metrics, evidence
freshness, support/SLA health, AISPM posture, exclusions, and renewal checkpoint
readiness remain acceptable after the initial closeout.

## Required Review Areas

- closeout handoff readiness
- customer success owner
- security owner
- support owner
- executive sponsor
- success metrics
- evidence freshness
- support/SLA health
- AISPM posture and drift
- open exclusions
- renewal checkpoint
- next review schedule

## Validate The Live Sanitized Review

```bash
python3 scripts/validate_customer_operating_review.py \
  --packet examples/customer-operating-review/customer-operating-review.live.sanitized.example.json \
  --require-live
```

CLI equivalent:

```bash
cavra release customer-operating-review \
  --packet examples/customer-operating-review/customer-operating-review.live.sanitized.example.json \
  --require-live
```

Completion condition:

```json
{
  "ready_for_customer_operating_review": true,
  "blocker_count": 0,
  "warning_count": 0
}
```

## Operating Pattern

1. Validate the closeout handoff packet.
2. Gather sanitized operating-review refs.
3. Validate the operating-review packet.
4. Record the review in the customer evidence room.
5. Schedule the next review or renewal checkpoint.
