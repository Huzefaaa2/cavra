# CAVRA Roadmap Governance Quickcheck

The roadmap governance quickcheck is the operator shortcut for proving the public roadmap is closed and the future-work governance chain is usable.

It does not add a roadmap row and does not reopen `R7`. It runs the normalized `R7.61` completion boundary and the [Roadmap Future Work Governance Index](Roadmap-Future-Work-Governance-Index) together so operators can answer one question:

> Is the roadmap closed, and is future product work governed before it becomes a new phase?

## What It Proves

The quickcheck requires:

- the public roadmap phase summary remains complete;
- all 91 numbered rows remain `Completed`;
- the final numbered row remains `R7.61`;
- README, docs, and wiki status text still preserve the live-operations boundary;
- the future-work governance chain has live intake, charter, opening, registry, and index results;
- the index returns `ready_to_close_future_work_governance_chain`;
- no future work is being smuggled into `R7.62` or later rows.

## Generate Operator Results

```bash
python3 scripts/validate_roadmap_governance_quickcheck.py \
  --repo-root . \
  --export-dir examples/roadmap-governance-quickcheck
```

Installed/operator CLI equivalent:

```bash
cavra release roadmap-governance-quickcheck \
  --repo-root . \
  --export-dir examples/roadmap-governance-quickcheck
```

## Validate The Live Quickcheck

```bash
python3 scripts/validate_roadmap_governance_quickcheck.py \
  --repo-root . \
  --require-live
```

Installed/operator CLI equivalent:

```bash
cavra release roadmap-governance-quickcheck \
  --repo-root . \
  --require-live
```

The completion condition is:

```json
{
  "ready_for_roadmap_governance_quickcheck": true,
  "decision": "ready_to_operate_closed_roadmap_governance",
  "blocker_count": 0,
  "warning_count": 0
}
```

## Relationship To The Other Gates

| Layer | Purpose |
| --- | --- |
| Roadmap Completion Boundary | Proves the public R0-R7 roadmap is complete and stops at `R7.61`. |
| Roadmap Intake Gate | Classifies new requests before roadmap expansion. |
| Roadmap Candidate Charter | Proves accepted product candidates have scope, owners, criteria, and release controls. |
| Roadmap Future Phase Opening Gate | Proves a future phase can be opened without reopening R7. |
| Roadmap Future Phase Registry | Records approved future phases outside the R7 sequence. |
| Roadmap Future Work Governance Index | Aggregates intake, charter, opening, and registry results. |
| Roadmap Governance Quickcheck | Runs the completion boundary and governance index in one operator command. |

## Evidence Boundary

The quickcheck is public-safe. It should contain only repository status, sanitized refs, and validation results. Do not attach private customer names, tenant names, raw logs, raw alerts, raw prompts, connector tokens, SMTP secrets, contracts, pricing, legal terms, or private release notes.

Use this quickcheck before publishing executive status, opening a future phase, or answering whether the public roadmap is still closed.
