# CAVRA Phase 7 Roadmap Closeout

Phase 7 originally started as the Managed and Enterprise customer lifecycle hardening phase: live evidence intake, evidence-room closeout, customer handoff, operating review, renewal readiness, archive, public status, verification, announcement, and retrospective controls.

The later R7 rows extended that lifecycle into repeated Phase 8 public-scorecard monitoring cycles. Those rows are useful as implementation evidence, but the pattern can repeat forever. This closeout gate normalizes the roadmap so Phase 7 has a real finish line.

## Normalized Status

R7.1 through R7.4 are now marked `Completed`. They were previously left as `In Progress` even though the implementation artifacts already existed and the current validation gates pass.

| Gate | Normalized Status | Validation |
| --- | --- | --- |
| R7.1 Customer live evidence intake | Completed | `ready_for_customer_live_evidence_intake: true`, zero blockers |
| R7.2 Customer evidence-room closeout | Completed | `ready_for_customer_evidence_room_closeout: true`, zero blockers |
| R7.3 Customer closeout handoff | Completed | `ready_for_customer_closeout_handoff: true`, zero blockers |
| R7.4 Customer operating review | Completed | `ready_for_customer_operating_review: true`, zero blockers |

## Phase 7 Stop Rule

Phase 7 closes at R7.61.

R7.60 remains the final implemented recurring public-scorecard monitoring readiness artifact in the Phase 7 roadmap sequence. R7.61 is the closeout gate that freezes the Phase 7 roadmap loop and moves future repeated customer-health, monitoring, scorecard, and remediation cycles into live operations evidence.

Future work should not add R7.62, R7.63, or more monitoring-cycle rows unless it introduces a genuinely new product capability, public contract, API, CLI command, validator family, deployment model, or buyer-facing trust surface.

Run the [Roadmap Intake Gate](roadmap-intake-gate.md) before adding any future roadmap item. It classifies a request as live operations evidence, a new product roadmap candidate, or needing architect review.

If the intake gate returns `new_product_roadmap_candidate`, run the [Roadmap Candidate Charter](roadmap-candidate-charter.md) before opening a future phase. The charter proves scope, ownership, acceptance criteria, docs/test/release plans, public-contract boundaries, and redaction controls.

If the charter passes, run the [Roadmap Future Phase Opening Gate](Roadmap-Future-Phase-Opening-Gate.md) before creating a future phase or row set. The gate proves phase owner, product owner, architecture owner, milestones, dependencies, exit criteria, test/docs/release/security controls, rollback planning, and the R7.61 boundary reference. It still does not add `R7.62`.

If the opening gate passes, run the [Roadmap Future Phase Registry](Roadmap-Future-Phase-Registry.md) to record the approved future phase with sanitized ownership, backlog, release gate, status report, public-contract boundary, and exit-criteria refs. The registry is a future-phase ledger, not a continuation of R7.

After the registry passes, run the [Roadmap Future Work Governance Index](Roadmap-Future-Work-Governance-Index.md) as the one-pass closeout for intake, charter, opening, and registry results. The index closes the future-work governance chain without reopening R7.

For executive status or future-phase planning, run the [Roadmap Governance Quickcheck](Roadmap-Governance-Quickcheck.md). It validates the R7.61 completion boundary and the future-work governance index together without adding another roadmap row.

## What Continues After Closeout

The following continue as customer operations, not as endless roadmap rows:

- running customer operating reviews;
- refreshing public-safe scorecards;
- collecting monitoring-cycle evidence;
- remediating drift;
- updating customer evidence rooms;
- preparing renewal and expansion packets;
- archiving customer-safe closeout artifacts.

Those activities belong in live evidence rooms, release packets, customer-success systems, and private Enterprise operations records.

Use `python3 scripts/validate_roadmap_intake_gate.py --require-live` or `cavra release roadmap-intake-gate --require-live` to record that classification with sanitized references.

Use `python3 scripts/validate_roadmap_candidate_charter.py --require-live` or `cavra release roadmap-candidate-charter --require-live` only for requests that the intake gate already classified as product candidates.

Use `python3 scripts/validate_roadmap_future_phase_opening_gate.py --require-live` or `cavra release roadmap-future-phase-opening-gate --require-live` only after the candidate charter passes.

Use `python3 scripts/validate_roadmap_future_phase_registry.py --require-live` or `cavra release roadmap-future-phase-registry --require-live` only after the future phase opening gate passes.

Use `python3 scripts/validate_roadmap_future_work_governance_index.py --require-live` or `cavra release roadmap-future-work-governance-index --require-live` as the final one-pass governance check for future product work.

Use `python3 scripts/validate_roadmap_governance_quickcheck.py --repo-root . --require-live` or `cavra release roadmap-governance-quickcheck --repo-root . --require-live` as the operator shortcut for proving the roadmap boundary and future-work governance chain together.

## Roadmap Boundary

The public roadmap is now closed for the numbered rows currently listed in the
tracker: R0.1 through R7.61 are complete for their stated public-contract scope.
Phase 7 is therefore `Completed` in the phase summary. Managed and Enterprise
customers still need real deployment validation, but that work is recorded as
live operations evidence rather than new R7 rows.

## What Becomes New Roadmap Work

Create a new roadmap item only when the work changes CAVRA itself, such as:

- a new validator type;
- a new API or CLI command;
- a new connector or deployment target;
- a new AISPM/posture capability;
- a new evidence schema;
- a new trust, compliance, or buyer-facing artifact;
- a new documented edition or packaging model.

If a request does not meet those criteria, classify it as `live_operations_evidence` and attach it to the relevant customer evidence room or operating packet.

## Verification Commands

```bash
python3 scripts/validate_customer_live_evidence.py \
  --packet examples/customer-live-evidence/customer-live-evidence.live.sanitized.example.json \
  --require-live

python3 scripts/validate_customer_evidence_room.py \
  --index examples/customer-evidence-room/customer-evidence-room.live.sanitized.example.json \
  --require-live

python3 scripts/validate_customer_closeout_handoff.py \
  --packet examples/customer-closeout-handoff/customer-closeout-handoff.live.sanitized.example.json \
  --require-live

python3 scripts/validate_customer_operating_review.py \
  --packet examples/customer-operating-review/customer-operating-review.live.sanitized.example.json \
  --require-live

python3 -m pytest \
  tests/test_customer_live_evidence.py \
  tests/test_customer_evidence_room.py \
  tests/test_customer_closeout_handoff.py \
  tests/test_customer_operating_review.py \
  -q
```

Current result: all four validators return ready with zero blockers, and the focused test suite passes.
