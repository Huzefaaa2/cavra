# Customer Lifecycle Public Status Summary

The customer lifecycle public status summary is the R7.9 customer-facing status
packet for Managed and Enterprise lifecycle closeout. It is derived from the
customer lifecycle archive manifest and contains only sanitized references,
customer-safe status language, publication controls, and support handoff refs.

It follows [Customer Lifecycle Archive Manifest](customer-lifecycle-archive-manifest.md).

## Generate Examples

```bash
python3 scripts/validate_customer_lifecycle_status.py \
  --export-dir dist/customer-lifecycle-status
```

CLI equivalent:

```bash
cavra release customer-lifecycle-status \
  --export-dir dist/customer-lifecycle-status
```

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

## Required Status Areas

- deployment status
- security posture
- evidence status
- operating cadence
- renewal outcome
- next steps
- support handoff refs
- publication controls

## Privacy Controls

The public status packet must not include customer names, customer emails,
private notes, raw evidence, raw contracts, pricing, contract values, renewal
amounts, or commercial terms. The packet is suitable for customer-facing status
communication because it contains sanitized refs and approved summary language
only.
