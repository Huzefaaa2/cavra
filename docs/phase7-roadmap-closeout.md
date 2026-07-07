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

## What Becomes New Roadmap Work

Create a new roadmap item only when the work changes CAVRA itself, such as:

- a new validator type;
- a new API or CLI command;
- a new connector or deployment target;
- a new AISPM/posture capability;
- a new evidence schema;
- a new trust, compliance, or buyer-facing artifact;
- a new documented edition or packaging model.

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

