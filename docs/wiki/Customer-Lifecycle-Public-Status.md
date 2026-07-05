# Customer Lifecycle Public Status Summary

The customer lifecycle public status summary is the R7.9 customer-facing status
packet for Managed and Enterprise lifecycle closeout. It is derived from the
customer lifecycle archive manifest and contains sanitized references, approved
summary text, publication controls, and support handoff refs.

It follows [Customer Lifecycle Archive Manifest](Customer-Lifecycle-Archive-Manifest.md).

## Required Areas

- deployment status
- security posture
- evidence status
- operating cadence
- renewal outcome
- next steps
- support handoff refs
- publication controls

## Validate The Live Sanitized Packet

```bash
python3 scripts/validate_customer_lifecycle_status.py \
  --packet examples/customer-lifecycle-status/customer-lifecycle-status.live.sanitized.example.json \
  --require-live
```

CLI equivalent:

```bash
cavra release customer-lifecycle-status \
  --packet examples/customer-lifecycle-status/customer-lifecycle-status.live.sanitized.example.json \
  --require-live
```

Completion condition:

```json
{
  "ready_for_customer_lifecycle_public_status": true,
  "blocker_count": 0,
  "warning_count": 0
}
```
