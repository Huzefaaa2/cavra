# Repository Inventory and Policy Rollout

Phase 6 now persists repository scope and policy rollout status for the CAVRA console and API.

## Feature Summary

CAVRA tracks governed repositories and the policies applied to them through JSON or SQLite stores. This gives platform, security, and audit teams a durable view of which repositories are active, who owns them, which policy pack is assigned, how risky the repository is, and whether the rollout is planned, active, paused, or retired.

## API Surface

Repository inventory:

- `GET /repositories`
- `POST /repositories`
- `GET /repositories/{repository_id}`

Policy rollout:

- `GET /policy-rollouts`
- `POST /policy-rollouts`
- `GET /policy-rollouts/{rollout_id}`
- `GET /policy-rollout-details/{rollout_id}`

Supported repository filters are `provider`, `owner`, `policy_pack`, `status`, and `risk_tier`.

Supported rollout filters are `repository`, `policy_pack`, `state`, `mode`, and `owner`.

## Persistence

Default JSON store:

```bash
.cavra/api/inventory.json
```

Override the JSON location:

```bash
export CAVRA_INVENTORY_STORE=.cavra/api/inventory.json
```

Use SQLite:

```bash
export CAVRA_INVENTORY_DB=.cavra/api/inventory.db
cavra evidence migrate --sqlite .cavra/api/inventory.db
```

The migration `005_repository_policy_rollout.sql` creates `inventory_repositories` and `inventory_policy_rollouts` with indexes for the common console and API filters.

## Console

The sandbox console now includes repository and rollout views. It can run with bundled sample data or use the API when `/console/config` exposes the `repositories` and `policy_rollouts` endpoints.

Operators can filter repositories by owner, policy pack, and risk tier. They can filter rollout records by state and mode to find active enforcement, planned rollouts, paused policy deployments, or break-glass exceptions. The rollout detail view joins rollout state with repository ownership, policy pack metadata, matching decision activity, integration readiness, and rollout readiness checks.

Rollout changes can now be previewed through `POST /policy-rollouts/change-plan` and applied through `POST /policy-rollouts/apply-change`. Plans show before/after state, changed fields, risk level, approval requirement, and operator notes. The console includes a Policy Authoring and Rollout Changes section for draft policy preview and rollout transition workflows.

## User Stories

- As a CISO, I can see which repositories are governed and which policy pack protects each one.
- As a platform engineer, I can track rollout state before moving repositories from audit-only to enforcement.
- As an auditor, I can connect repository policy coverage to evidence references and decision records.

## Enterprise Challenge Solved

Enterprises adopting AI coding agents need a central answer to: which repositories are governed, who owns them, what policy mode is active, and where the audit evidence is stored. Repository inventory and policy rollout persistence turn CAVRA from isolated runtime checks into an operational control plane that can support rollout governance, audit readiness, and phased adoption.

## Next Work

The next recommended step is daemon and CI runner examples for typed release governance enforcement requests.
