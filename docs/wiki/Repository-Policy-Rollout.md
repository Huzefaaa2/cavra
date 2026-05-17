# Repository Inventory and Policy Rollout

Phase 6 now includes durable repository scope and policy rollout visibility.

## What It Provides

- JSON and SQLite persistence for governed repositories.
- JSON and SQLite persistence for policy rollout records.
- API filters for owner, policy pack, status, risk tier, rollout state, rollout mode, and repository.
- Console views for repository inventory, rollout progress, and rollout detail.
- Evidence references so rollout records can point back to CAVRA decisions, bundles, or attestations.

## How To Use

Configure JSON persistence:

```bash
export CAVRA_INVENTORY_STORE=.cavra/api/inventory.json
```

Configure SQLite persistence:

```bash
export CAVRA_INVENTORY_DB=.cavra/api/inventory.db
cavra evidence migrate --sqlite .cavra/api/inventory.db
```

Create or update repository inventory:

```bash
curl -X POST http://127.0.0.1:8000/repositories \
  -H 'content-type: application/json' \
  -d '{"repository":"payments/api","owner":"payments-platform","policy_pack":"cavra-banking-baseline","risk_tier":"regulated","status":"active"}'
```

Create or update policy rollout state:

```bash
curl -X POST http://127.0.0.1:8000/policy-rollouts \
  -H 'content-type: application/json' \
  -d '{"repository":"payments/api","policy_pack":"cavra-banking-baseline","mode":"strict","state":"active","coverage_percent":100}'
```

## User Stories

- As a CISO, I can see which repositories are protected by which policy pack.
- As a platform engineer, I can track rollout mode before moving teams from audit-only to enforcement.
- As an auditor, I can map policy coverage to evidence references and persisted decision records.

## Enterprise Challenge Solved

Large enterprises cannot govern AI coding agents repository by repository through spreadsheets. CAVRA now provides an API-backed inventory and rollout view so repository coverage, ownership, risk, and enforcement mode can be inspected centrally.

## Next

The next recommended work is hosted attestation artifact retrieval and deeper OIDC-authenticated console sessions.
