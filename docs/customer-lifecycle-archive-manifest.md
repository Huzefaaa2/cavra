# Customer Lifecycle Archive Manifest

The customer lifecycle archive manifest is the R7.8 closeout gate for Managed
and Enterprise customer lifecycle operations. It binds the customer lifecycle
executive rollup to the final archive refs, retention controls, verifier refs,
and audit handoff refs required to preserve lifecycle evidence without exposing
private customer material.

The archive manifest follows [Customer Lifecycle Executive Rollup](customer-lifecycle-executive-rollup.md).

## Generate Examples

```bash
python3 scripts/validate_customer_lifecycle_archive.py \
  --export-dir dist/customer-lifecycle-archive
```

CLI equivalent:

```bash
cavra release customer-lifecycle-archive \
  --export-dir dist/customer-lifecycle-archive
```

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

## Required Manifest Areas

- lifecycle executive rollup result
- archive owner refs
- customer success owner ref
- security owner ref
- compliance owner ref
- operations owner ref
- executive rollup archive section
- evidence room archive section
- audit manifest section
- retention policy section
- verifier bundle section
- handoff record section
- retention policy refs
- verifier refs
- audit handoff controls

## Privacy Controls

The public manifest must contain sanitized references and control metadata only.
The validator blocks customer names, customer emails, private notes, raw
contracts, raw evidence, pricing, contract values, renewal amounts, and
commercial terms.
