# CAVRA Roadmap Future Phase Opening Gate

The roadmap future phase opening gate is the gate after the [Roadmap Candidate Charter](roadmap-candidate-charter.md). The intake gate classifies a request. The candidate charter proves the request is a valid product candidate. This gate proves the candidate is ready to become a future product phase because owners, scope, milestones, dependencies, release controls, test controls, docs controls, security review, rollback planning, and the roadmap boundary are all present.

This gate does not add `R7.62`. It protects the closed `R7.61` boundary by requiring explicit phase-opening evidence before a future roadmap phase can be created.

## What It Proves

The gate requires sanitized references for:

- source roadmap candidate charter result;
- phase candidate, source charter, phase owner, product owner, architecture owner, and roadmap boundary;
- future phase name, problem statement, scope, milestones, dependencies, and exit criteria;
- backlog, implementation plan, test plan, docs plan, release gate, rollback plan, and security review;
- final phase-opening decision and target future phase reference;
- redaction controls proving no private customer, tenant, credential, raw log, raw alert, raw prompt, model, contract, or private release material is present.

## Generate Templates

```bash
python3 scripts/validate_roadmap_future_phase_opening_gate.py \
  --export-dir examples/roadmap-future-phase-opening-gate
```

Installed/operator CLI equivalent:

```bash
cavra release roadmap-future-phase-opening-gate \
  --export-dir examples/roadmap-future-phase-opening-gate
```

## Validate A Live Sanitized Gate

```bash
python3 scripts/validate_roadmap_future_phase_opening_gate.py \
  --gate examples/roadmap-future-phase-opening-gate/roadmap-future-phase-opening-gate.live.sanitized.example.json \
  --require-live
```

Installed/operator CLI equivalent:

```bash
cavra release roadmap-future-phase-opening-gate \
  --gate examples/roadmap-future-phase-opening-gate/roadmap-future-phase-opening-gate.live.sanitized.example.json \
  --require-live
```

The completion condition is:

```json
{
  "ready_for_roadmap_future_phase_opening": true,
  "decision": "ready_to_open_future_product_phase",
  "blocker_count": 0
}
```

## Required Opening Controls

| Control | Purpose |
| --- | --- |
| Backlog reference | Shows the candidate has an implementation backlog, not only an idea. |
| Implementation plan | Defines the product build path. |
| Test plan | Defines focused, regression, and release validation expectations. |
| Documentation plan | Defines README, docs, wiki, and operator guidance impact. |
| Release gate | Defines the validator or release condition that proves completion. |
| Rollback plan | Defines how the change can be withdrawn or safely disabled. |
| Security review | Defines trust, redaction, and architecture review ownership. |

## Evidence Boundary

Do not commit customer identities, tenant names, email addresses, SMTP credentials, connector tokens, alert payloads, raw logs, raw prompts, model data, pricing, contracts, legal terms, or private release notes.

Commit only sanitized references such as `phase://`, `charter://`, `product://`, `roadmap://`, `plan://`, `test://`, `docs://`, `security://`, `architecture://`, `workflow://`, `github://`, or `sample://`.

## Relationship To Future Roadmap Work

The future phase opening gate is not itself a new product phase. It is the required precondition after a successful candidate charter and before a future phase or row set is created.

If the upstream candidate charter is blocked or rejected to operations evidence, this gate blocks and the work should remain in private evidence rooms, operating packets, or customer-success records.
