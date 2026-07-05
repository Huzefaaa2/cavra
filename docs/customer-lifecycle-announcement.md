# CAVRA Customer Lifecycle Closeout Announcement Packet

The customer lifecycle closeout announcement packet is the R7.12 customer-safe
release communication gate for CAVRA Managed and Enterprise lifecycle closeout.
It consumes the R7.11 customer lifecycle verification index and produces a
sanitized announcement contract for release notes, public status, support
handoff, and operator handoff.

It does not embed customer names, customer email addresses, raw evidence,
private notes, pricing, contract values, renewal amounts, raw contracts, legal
terms, or commercial terms.

## What It Verifies

- The R7.11 verification index is live, sanitized, ready, and blocker-free.
- Release, customer success, security, support, and communications owner refs
  are present.
- Required announcement sections are complete:
  - headline;
  - customer-safe summary;
  - what is ready;
  - evidence and trust;
  - support and next steps;
  - operator handoff.
- Release-note refs and operator-handoff refs are sanitized.
- Announcement controls confirm release-note approval, customer-safe language,
  support path verification, operator handoff, and redaction boundaries.

## Generate Examples

```bash
python3 scripts/validate_customer_lifecycle_announcement.py \
  --export-dir examples/customer-lifecycle-announcement \
  --repo-root .
```

This writes:

- `customer-lifecycle-announcement.sample.json`
- `customer-lifecycle-announcement.live.sanitized.example.json`
- `customer-lifecycle-announcement.sample.result.json`
- `customer-lifecycle-announcement.live.sanitized.result.json`

## Validate Announcement Readiness

```bash
python3 scripts/validate_customer_lifecycle_announcement.py \
  --packet examples/customer-lifecycle-announcement/customer-lifecycle-announcement.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

Completion condition:

```json
{
  "ready_for_customer_lifecycle_announcement_packet": true,
  "blocker_count": 0,
  "warning_count": 0
}
```

The same gate is available through the CLI:

```bash
PYTHONPATH=src python3 -m cavra.cli release customer-lifecycle-announcement \
  --packet examples/customer-lifecycle-announcement/customer-lifecycle-announcement.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

## Public Repository Boundary

The public repository provides the announcement contract, examples, validator,
CLI command, tests, docs, and CI workflow. Real release-note publication,
customer-specific communication, commercial context, support records, and
operator evidence remain deployment-specific.
