# Phase 6 Ecosystem Expansion Rollup

The Phase 6 rollup is the public closeout gate for the R6 ecosystem expansion
workstream. It summarizes:

- R6.1 benchmark and SLO regression gates;
- R6.2 generic agent adapter SDK and action taxonomy;
- R6.3 AI red-team and supply-chain gates;
- R6.4 zero-trust reference deployments.

The rollup intentionally separates two different states:

| State | Meaning |
| --- | --- |
| `ready_for_phase6_public_contract_release` | The public repository contains validated contracts, examples, docs, workflows, and tests for all R6 gates. |
| `ready_for_customer_live_phase6_closeout` | A customer or managed deployment has supplied real live evidence for benchmark runs, adapters, red-team closeout, and zero-trust deployment smoke tests. |

The public repository can satisfy the first state. The second state must be
provided by a real customer environment or managed deployment.

## Generate The Rollup

```bash
python3 scripts/validate_phase6_rollup.py \
  --repo-root . \
  --export-dir dist/phase6-rollup
```

CLI equivalent:

```bash
cavra release phase6-rollup --repo-root .
cavra release phase6-rollup --repo-root . --export-dir dist/phase6-rollup
```

## Validate The Checked-In Rollup

```bash
python3 scripts/validate_phase6_rollup.py \
  --packet examples/phase6-rollup/phase6-ecosystem-rollup.json \
  --repo-root .
```

Expected public result:

```text
ready_for_phase6_public_contract_release: true
ready_for_customer_live_phase6_closeout: false
status: ready_with_customer_live_warnings
```

## Customer Live Closeout

To close Phase 6 for a real customer or managed deployment, supply live evidence
references for every R6 gate and run:

```bash
python3 scripts/validate_phase6_rollup.py \
  --packet <customer-phase6-rollup.json> \
  --repo-root . \
  --require-customer-live
```

Required customer evidence categories:

| Gate | Required live evidence |
| --- | --- |
| R6.1 | Tenant benchmark run, production HA evidence, failure drill recording. |
| R6.2 | Provider adapter install, customer action fixture, tenant runtime evaluation. |
| R6.3 | Customer prompt suite, proprietary scanner plugin, red-team closeout. |
| R6.4 | Docker Compose smoke, Helm template, Terraform validate, Azure what-if, scanner operation. |

The customer live completion condition is:

```text
ready_for_customer_live_phase6_closeout: true
blocker_count: 0
warning_count: 0
```

## Public Artifacts

The checked-in rollup packet is:

- `examples/phase6-rollup/phase6-ecosystem-rollup.json`

The checked-in validation result is:

- `examples/phase6-rollup/phase6-ecosystem-rollup-result.json`

The CI workflow is:

- `.github/workflows/phase6-rollup.yml`
