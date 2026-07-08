# CAVRA Roadmap Intake Gate

The roadmap intake gate keeps the public CAVRA roadmap from turning into an endless operating loop. It classifies incoming work before a roadmap row is added.

Use it after [Phase 7 Roadmap Closeout](phase7-roadmap-closeout.md) whenever a new request could be confused with another R7 cycle.

## What It Decides

The gate returns one of three decisions:

| Decision | Meaning |
| --- | --- |
| `live_operations_evidence` | The request is routine customer operations and should be captured in private evidence rooms, release packets, customer-success records, or support systems. |
| `new_product_roadmap_candidate` | The request changes CAVRA itself and can be considered for a new roadmap item. |
| `needs_architect_review` | The request type is unclear and needs manual triage before implementation. |

## Operating Evidence Requests

These should not add new R7 rows:

- customer monitoring cycle;
- customer operating review;
- drift remediation;
- evidence-room maintenance;
- private customer closeout;
- private live validation;
- public scorecard refresh;
- renewal review;
- support case.

## Product Roadmap Candidates

These may become new roadmap work:

- new product capability;
- new API or CLI command;
- new validator family;
- new connector;
- new deployment target;
- new AISPM or posture capability;
- new evidence schema;
- new trust artifact;
- new buyer-facing surface;
- new edition or packaging model.

## Generate Templates

```bash
python3 scripts/validate_roadmap_intake_gate.py \
  --export-dir examples/roadmap-intake-gate
```

Installed/operator CLI equivalent:

```bash
cavra release roadmap-intake-gate \
  --export-dir examples/roadmap-intake-gate
```

## Validate A Live Sanitized Intake Packet

```bash
python3 scripts/validate_roadmap_intake_gate.py \
  --packet examples/roadmap-intake-gate/roadmap-intake-gate.product-candidate.live.sanitized.example.json \
  --require-live
```

Installed/operator CLI equivalent:

```bash
cavra release roadmap-intake-gate \
  --packet examples/roadmap-intake-gate/roadmap-intake-gate.product-candidate.live.sanitized.example.json \
  --require-live
```

The completion condition is:

```json
{
  "ready_for_roadmap_intake_decision": true,
  "blocker_count": 0
}
```

## Evidence Boundary

Do not commit customer identities, tenant names, email addresses, SMTP credentials, connector tokens, alert payloads, raw logs, raw prompts, model data, pricing, contracts, legal terms, or private release notes.

Commit only sanitized references such as `roadmap://`, `product://`, `evidence://`, `operations://`, `ticket://`, `workflow://`, `github://`, `docs://`, or `sample://`.

## Relationship To Phase 7 Closeout

Phase 7 closes at `R7.61`. The intake gate does not add `R7.62`; it protects the boundary by forcing every future request through a clear classification before implementation.
