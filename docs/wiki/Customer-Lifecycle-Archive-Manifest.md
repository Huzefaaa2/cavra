# Customer Lifecycle Archive Manifest

The customer lifecycle archive manifest is the final R7 archive index for
Managed and Enterprise lifecycle closeout. It binds the lifecycle executive
rollup to immutable archive refs, retention controls, verifier refs, and audit
handoff refs without publishing customer names, pricing, raw contracts, raw
evidence, or private notes.

It follows [Customer Lifecycle Executive Rollup](Customer-Lifecycle-Executive-Rollup.md).

## Required Areas

- lifecycle executive rollup result
- archive owner refs
- lifecycle archive sections
- retention controls
- verifier refs
- audit handoff controls
- privacy controls

## Validate The Live Sanitized Manifest

```bash
python3 scripts/validate_customer_lifecycle_archive.py \
  --packet examples/customer-lifecycle-archive/customer-lifecycle-archive.live.sanitized.example.json \
  --require-live
```

CLI equivalent:

```bash
cavra release customer-lifecycle-archive \
  --packet examples/customer-lifecycle-archive/customer-lifecycle-archive.live.sanitized.example.json \
  --require-live
```

Completion condition:

```json
{
  "ready_for_customer_lifecycle_archive_manifest": true,
  "blocker_count": 0,
  "warning_count": 0
}
```
