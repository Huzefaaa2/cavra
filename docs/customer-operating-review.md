# Customer Operating Review

The customer operating review packet is the recurring Managed and Enterprise
post-closeout health gate. It starts after the customer closeout handoff and is
intended for monthly, quarterly, or renewal-driven review cycles.

The public packet is sanitized. It contains only refs and health controls for
success metrics, evidence freshness, support/SLA health, AISPM posture, open
exclusions, and renewal checkpoints.

## What It Proves

- the closeout handoff remains ready
- customer success, security, support, and executive sponsor refs exist
- success metrics are current
- evidence-room freshness is current
- support/SLA health is acceptable
- AISPM posture and drift are acceptable
- open exclusions have been reviewed
- renewal checkpoint and next review are scheduled

## Generate Examples

```bash
python3 scripts/validate_customer_operating_review.py \
  --export-dir dist/customer-operating-review
```

Equivalent CLI:

```bash
cavra release customer-operating-review \
  --export-dir dist/customer-operating-review
```

## Validate Review

```bash
python3 scripts/validate_customer_operating_review.py \
  --packet examples/customer-operating-review/customer-operating-review.live.sanitized.example.json \
  --require-live
```

Equivalent CLI:

```bash
cavra release customer-operating-review \
  --packet examples/customer-operating-review/customer-operating-review.live.sanitized.example.json \
  --require-live
```

The completion condition is:

```json
{
  "ready_for_customer_operating_review": true,
  "blocker_count": 0,
  "warning_count": 0
}
```

## Operating Sequence

1. Validate customer closeout handoff.
2. Collect sanitized review refs from customer success, security, support, and
   AISPM operations.
3. Validate the customer operating review packet.
4. Record the review result in the customer evidence room.
5. Schedule the next review or renewal checkpoint.
