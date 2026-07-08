# Phase 6 Ecosystem Expansion Rollup

The Phase 6 rollup is the public closeout gate for the R6 ecosystem expansion
workstream. It summarizes:

- R6.1 benchmark and SLO regression gates;
- R6.2 generic agent adapter SDK and action taxonomy;
- R6.3 AI red-team and supply-chain gates;
- R6.4 zero-trust reference deployments.

## What The Rollup Proves

| State | Meaning |
| --- | --- |
| `ready_for_phase6_public_contract_release` | The public repository contains validated contracts, examples, docs, workflows, and tests for all R6 gates. |
| `ready_for_customer_live_phase6_closeout` | A customer or managed deployment has supplied real live evidence for benchmark runs, adapters, red-team closeout, and zero-trust deployment smoke tests. |

The public repository can satisfy the public-contract state. Customer live
closeout must come from a real managed or enterprise deployment.

## Validate

```bash
python3 scripts/validate_phase6_rollup.py \
  --packet examples/phase6-rollup/phase6-ecosystem-rollup.json \
  --repo-root .
```

CLI equivalent:

```bash
cavra release phase6-rollup --repo-root .
```

Expected public result:

```text
ready_for_phase6_public_contract_release: true
ready_for_customer_live_phase6_closeout: false
status: ready_with_customer_live_warnings
```

## Customer Live Evidence

Customer live closeout requires:

| Gate | Required live evidence |
| --- | --- |
| R6.1 | Tenant benchmark run, production HA evidence, failure drill recording. |
| R6.2 | Provider adapter install, customer action fixture, tenant runtime evaluation. |
| R6.3 | Customer prompt suite, proprietary scanner plugin, red-team closeout. |
| R6.4 | Docker Compose smoke, Helm template, Terraform validate, Azure what-if, scanner operation. |

Run with `--require-customer-live` only when those references are present.

Related pages: [Benchmark SLO Regression Gates](Benchmark-SLO-Regression-Gates.md),
[Generic Agent Adapter SDK And Action Taxonomy](Generic-Agent-Adapter-SDK-And-Action-Taxonomy.md),
[AI Red-Team And Supply-Chain Gates](AI-Red-Team-And-Supply-Chain-Gates.md), and
[Zero-Trust Reference Deployments](Zero-Trust-Reference-Deployments.md).

## Roadmap Normalization

Phase 6 is closed for public-contract implementation. R6.1 through R6.4 are
marked complete because their validators, live-sanitized examples, docs,
workflows, tests, and rollup bindings are present and the Phase 6 rollup returns
`ready_for_phase6_public_contract_release: true` with no blockers.

The remaining customer-live state is expected to stay deployment-specific until
a Managed or Enterprise environment attaches real benchmark, adapter,
red-team, and zero-trust deployment evidence refs.
