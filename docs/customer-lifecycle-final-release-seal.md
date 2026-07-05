# CAVRA Customer Lifecycle Final Release Seal

The customer lifecycle final release seal is the R7.10 closeout gate for Managed
and Enterprise customer lifecycle operations. It turns the R7 customer lifecycle
chain into one final, customer-safe readiness packet for release notes, public
status communication, support handoff, and archive verification.

The seal binds to the R7.9 customer lifecycle public status packet. It does not
embed customer names, email addresses, private notes, raw evidence, pricing,
contract values, raw contracts, renewal amounts, or commercial terms.

## What It Verifies

- The lifecycle public status packet is live, sanitized, and blocker-free.
- Required release, customer success, security, support, communications, and
  archive owner references are present.
- Required lifecycle components are sealed:
  - lifecycle public status;
  - archive manifest;
  - executive rollup;
  - renewal outcome;
  - operating review;
  - evidence room;
  - live evidence intake.
- Release publication refs are customer-safe.
- Final release controls are true for public status, archive, release notes,
  customer-success handoff, support handoff, security acceptance,
  communications acceptance, and redaction boundaries.
- A customer-safe completion statement is present.

## Generate Examples

```bash
python3 scripts/validate_customer_lifecycle_final_seal.py \
  --export-dir examples/customer-lifecycle-final-seal
```

This writes:

- `customer-lifecycle-final-seal.sample.json`
- `customer-lifecycle-final-seal.live.sanitized.example.json`
- `customer-lifecycle-final-seal.sample.result.json`
- `customer-lifecycle-final-seal.live.sanitized.result.json`

## Validate Final Readiness

```bash
python3 scripts/validate_customer_lifecycle_final_seal.py \
  --packet examples/customer-lifecycle-final-seal/customer-lifecycle-final-seal.live.sanitized.example.json \
  --require-live
```

Completion condition:

```json
{
  "ready_for_customer_lifecycle_final_release_seal": true,
  "blocker_count": 0,
  "warning_count": 0
}
```

The same gate is available through the CLI:

```bash
PYTHONPATH=src python3 -m cavra.cli release customer-lifecycle-final-seal \
  --packet examples/customer-lifecycle-final-seal/customer-lifecycle-final-seal.live.sanitized.example.json \
  --require-live
```

## Public Repository Boundary

The public repository provides the contract, examples, validator, CLI command,
tests, docs, and CI workflow. Real customer lifecycle evidence, private archive
locations, release-note approvals, support handoff records, commercial terms,
customer identities, and immutable evidence storage remain deployment-specific.
