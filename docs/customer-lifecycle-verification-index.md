# CAVRA Customer Lifecycle Verification Index

The customer lifecycle verification index is the R7.11 phase-level closeout
gate for CAVRA Managed and Enterprise lifecycle operations. It verifies that
the public R7 customer lifecycle chain is complete from R7.1 through R7.10.

The index checks that every customer lifecycle gate has:

- a live sanitized example packet;
- a live result packet with the expected readiness key set to `true`;
- a validator script;
- a GitHub Actions workflow;
- a focused test file;
- a repository documentation page;
- a wiki documentation page;
- a customer-safe validator command.

It does not embed customer names, customer email addresses, raw evidence,
private notes, pricing, contract values, renewal amounts, raw contracts, legal
terms, or commercial terms.

## Covered Gates

| Gate | Contract |
| --- | --- |
| R7.1 | Customer Live Evidence Intake |
| R7.2 | Customer Evidence Room Closeout |
| R7.3 | Customer Closeout Handoff |
| R7.4 | Customer Operating Review |
| R7.5 | Customer Renewal And Expansion Readiness |
| R7.6 | Customer Renewal Outcome Closeout |
| R7.7 | Customer Lifecycle Executive Rollup |
| R7.8 | Customer Lifecycle Archive Manifest |
| R7.9 | Customer Lifecycle Public Status Summary |
| R7.10 | Customer Lifecycle Final Release Seal |

## Generate Examples

```bash
python3 scripts/validate_customer_lifecycle_verification_index.py \
  --export-dir examples/customer-lifecycle-verification-index \
  --repo-root .
```

This writes:

- `customer-lifecycle-verification-index.sample.json`
- `customer-lifecycle-verification-index.live.sanitized.example.json`
- `customer-lifecycle-verification-index.sample.result.json`
- `customer-lifecycle-verification-index.live.sanitized.result.json`

## Validate Phase 7 Closeout

```bash
python3 scripts/validate_customer_lifecycle_verification_index.py \
  --index examples/customer-lifecycle-verification-index/customer-lifecycle-verification-index.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

Completion condition:

```json
{
  "ready_for_customer_lifecycle_verification_index": true,
  "blocker_count": 0,
  "warning_count": 0
}
```

The same gate is available through the CLI:

```bash
PYTHONPATH=src python3 -m cavra.cli release customer-lifecycle-verification-index \
  --index examples/customer-lifecycle-verification-index/customer-lifecycle-verification-index.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

## Public Repository Boundary

The public repository provides the verification-index contract, examples,
validator, CLI command, tests, docs, and CI workflow. Real customer evidence
locations, production archive stores, support handoff records, release-note
approval systems, commercial terms, and customer-specific communications remain
deployment-specific.
