# CAVRA Roadmap Future Phase Registry

The roadmap future phase registry is the gate after the [Roadmap Future Phase Opening Gate](roadmap-future-phase-opening-gate.md). The opening gate proves a future phase may be opened. The registry records the approved future phase as a sanitized, reviewable entry with ownership, public-contract boundary, release gate, backlog, status reporting, and exit criteria references.

This registry does not add `R7.62`. It records future phase candidates outside the closed Phase 7 row sequence so CAVRA can plan genuinely new product work without reopening the endless R7 loop.

## What It Proves

The registry requires sanitized references for:

- source future phase opening gate result;
- registry owner, review cadence, registry reference, and R7.61 roadmap boundary;
- phase ID, title, source opening gate, owners, public-contract boundary, backlog, release gate, status report, and exit criteria;
- registry decision and target registry reference;
- redaction controls proving no private customer, tenant, credential, raw log, raw alert, raw prompt, model, contract, or private release material is present.

## Generate Templates

```bash
python3 scripts/validate_roadmap_future_phase_registry.py \
  --export-dir examples/roadmap-future-phase-registry
```

Installed/operator CLI equivalent:

```bash
cavra release roadmap-future-phase-registry \
  --export-dir examples/roadmap-future-phase-registry
```

## Validate A Live Sanitized Registry

```bash
python3 scripts/validate_roadmap_future_phase_registry.py \
  --registry examples/roadmap-future-phase-registry/roadmap-future-phase-registry.live.sanitized.example.json \
  --require-live
```

Installed/operator CLI equivalent:

```bash
cavra release roadmap-future-phase-registry \
  --registry examples/roadmap-future-phase-registry/roadmap-future-phase-registry.live.sanitized.example.json \
  --require-live
```

The completion condition is:

```json
{
  "ready_for_roadmap_future_phase_registry": true,
  "decision": "ready_to_register_future_phase",
  "blocker_count": 0
}
```

## Required Registry Entry Fields

| Field | Purpose |
| --- | --- |
| Phase ID reference | Gives the future phase a stable sanitized identity. |
| Source opening gate reference | Links the entry back to the approved phase-opening gate. |
| Phase and architecture owners | Proves the future phase has named ownership. |
| Public contract boundary | Separates public repository scope from private delivery evidence. |
| Initial backlog reference | Shows the phase has actionable implementation work. |
| Release gate reference | Defines how completion will be proven. |
| Status report reference | Defines where progress will be reported. |
| Exit criteria reference | Defines how the phase closes. |

## Evidence Boundary

Do not commit customer identities, tenant names, email addresses, SMTP credentials, connector tokens, alert payloads, raw logs, raw prompts, model data, pricing, contracts, legal terms, or private release notes.

Commit only sanitized references such as `registry://`, `phase://`, `charter://`, `product://`, `roadmap://`, `plan://`, `test://`, `docs://`, `security://`, `architecture://`, `workflow://`, `github://`, or `sample://`.

## Relationship To Future Roadmap Work

The future phase registry is not itself a new product phase. It is the controlled ledger for future phases after intake, charter, and phase-opening gates have passed.

If the upstream phase-opening gate is blocked or rejected, this registry blocks and the work should remain in private evidence rooms, operating packets, or customer-success records.
