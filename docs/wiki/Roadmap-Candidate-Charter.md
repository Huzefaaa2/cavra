# CAVRA Roadmap Candidate Charter

The roadmap candidate charter is the gate after the [Roadmap Intake Gate](roadmap-intake-gate.md). The intake gate decides whether a request is allowed to become product roadmap work by returning `new_product_roadmap_candidate`. The charter gate proves that an accepted product candidate has enough scope, ownership, acceptance criteria, evidence boundary, test planning, documentation planning, and release control to become a future phase or roadmap item.

This gate does not add `R7.62`. It protects the closed `R7.61` boundary by requiring a clean product charter before any future roadmap expansion.

## What It Proves

The charter requires sanitized references for:

- source roadmap intake result;
- candidate, sponsor, product owner, architecture owner, and roadmap boundary;
- capability statement, included product surfaces, excluded scope, dependencies, and customer value;
- acceptance criteria for API/CLI contracts, docs surfaces, evidence model, public contract boundary, release gate, security boundary, and test plan;
- implementation, test, docs, rollback, release-owner, and review-cadence plans;
- final charter decision and target future phase reference.

## Generate Templates

```bash
python3 scripts/validate_roadmap_candidate_charter.py \
  --export-dir examples/roadmap-candidate-charter
```

Installed/operator CLI equivalent:

```bash
cavra release roadmap-candidate-charter \
  --export-dir examples/roadmap-candidate-charter
```

## Validate A Live Sanitized Charter

```bash
python3 scripts/validate_roadmap_candidate_charter.py \
  --charter examples/roadmap-candidate-charter/roadmap-candidate-charter.live.sanitized.example.json \
  --require-live
```

Installed/operator CLI equivalent:

```bash
cavra release roadmap-candidate-charter \
  --charter examples/roadmap-candidate-charter/roadmap-candidate-charter.live.sanitized.example.json \
  --require-live
```

The completion condition is:

```json
{
  "ready_for_roadmap_candidate_charter": true,
  "decision": "ready_for_product_roadmap_planning",
  "blocker_count": 0
}
```

## Required Acceptance Criteria

| Criterion | Purpose |
| --- | --- |
| API or CLI contract defined | The candidate has an explicit operator or integration surface. |
| Docs surface defined | The candidate has a documentation and wiki surface. |
| Evidence model defined | The candidate has a sanitized evidence and result model. |
| Public contract boundary defined | The candidate distinguishes public repo contract from private operations. |
| Release gate defined | The candidate has a completion condition and release validator. |
| Security boundary defined | The candidate has a redaction and trust boundary. |
| Test plan defined | The candidate has focused tests and regression scope. |

## Evidence Boundary

Do not commit customer identities, tenant names, email addresses, SMTP credentials, connector tokens, alert payloads, raw logs, raw prompts, model data, pricing, contracts, legal terms, or private release notes.

Commit only sanitized references such as `charter://`, `product://`, `roadmap://`, `plan://`, `test://`, `docs://`, `security://`, `architecture://`, `workflow://`, or `sample://`.

## Relationship To Future Roadmap Work

The charter is not itself a new product phase. It is the required precondition before a future phase can be opened. If the upstream intake decision is `live_operations_evidence`, this charter blocks and the work should remain in private evidence rooms or operating packets.
