# Phase 5 Policy Lifecycle And Event Core Closeout

The Phase 5 closeout gate is the public finish line for the policy lifecycle and
event-driven monitoring workstream. It verifies that the repository contains
validated public contracts, examples, docs, workflows, and tests for:

- R5.1 OPA/Rego policy path;
- R5.2 policy lifecycle tooling;
- R5.3 continuous monitoring event core.

The closeout intentionally separates public repository readiness from
customer-live readiness.

| State | Meaning |
| --- | --- |
| `ready_for_phase5_public_contract_release` | The public repository contains validated contracts, live-sanitized examples, docs, workflows, and tests for all R5 gates. |
| `ready_for_customer_live_phase5_closeout` | A Managed or Enterprise deployment has supplied real live evidence refs for customer policy PRs, policy rollout, OPA runtime deployment, monitoring dashboards, and event-bus operation. |

The public repository can satisfy the first state. The second state is supplied
by a real customer environment or managed deployment without exposing tenant
names, policy contents, private approval records, queue configuration, or
dashboard payloads.

## Generate The Closeout Packet

```bash
python3 scripts/validate_phase5_policy_event_closeout.py \
  --repo-root . \
  --export-dir dist/phase5-closeout
```

CLI equivalent:

```bash
cavra release phase5-closeout --repo-root .
cavra release phase5-closeout --repo-root . --export-dir dist/phase5-closeout
```

## Validate The Checked-In Packet

```bash
python3 scripts/validate_phase5_policy_event_closeout.py \
  --packet examples/phase5-closeout/phase5-policy-event-core-closeout.json \
  --repo-root .
```

Expected public result:

```text
ready_for_phase5_public_contract_release: true
ready_for_customer_live_phase5_closeout: false
status: ready_with_customer_live_warnings
```

## Customer-Live Closeout

To close Phase 5 for a real Managed or Enterprise deployment, attach
deployment-specific evidence references for every R5 gate and run:

```bash
python3 scripts/validate_phase5_policy_event_closeout.py \
  --packet <customer-phase5-closeout.json> \
  --repo-root . \
  --require-customer-live
```

Required customer evidence categories:

| Gate | Required live evidence |
| --- | --- |
| R5.1 | Customer policy PR, OPA runtime deployment, policy review approval. |
| R5.2 | Customer UI validation, policy rollout approval, rollback rehearsal. |
| R5.3 | Customer event-bus config, monitor dashboard, event-bus evidence. |

The customer live completion condition is:

```text
ready_for_customer_live_phase5_closeout: true
blocker_count: 0
warning_count: 0
```

## Public Artifacts

The checked-in closeout packet is:

- `examples/phase5-closeout/phase5-policy-event-core-closeout.json`

The checked-in validation result is:

- `examples/phase5-closeout/phase5-policy-event-core-closeout-result.json`

The CI workflow is:

- `.github/workflows/phase5-policy-event-closeout.yml`

With this gate complete, Phase 5 can be marked complete in the roadmap and the
next implementation focus moves to Phase 6 normalization and closeout review.
