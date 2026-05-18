# Activity Persistence

Phase 6 starts durable operational visibility for CAVRA sessions and decisions.

## Current Implementation

- JSON and SQLite stores for runtime sessions and decisions.
- `POST /decisions` now persists evaluated decisions and updates the session summary.
- `GET /decisions` supports filters for session, agent, repository, policy pack, decision outcome, severity, action type, limit, and offset.
- `GET /sessions` supports filters for agent, repository, policy pack, state, limit, and offset.
- Console Activity Explorer shows persisted sessions and decisions with enterprise-friendly filters.
- SQLite migration `004_activity_sessions_decisions.sql` creates indexed activity tables.

## Configuration

Use JSON persistence for local pilots:

```bash
export CAVRA_ACTIVITY_STORE=.cavra/api/activity.json
```

Use SQLite persistence for self-hosted API deployments:

```bash
export CAVRA_ACTIVITY_DB=.cavra/activity.db
cavra evidence migrate --sqlite .cavra/activity.db
```

The shared migration command applies evidence, approval, registry, and activity migrations.

## User Stories

- As a CISO, I can review blocked and approved AI-agent actions across repositories.
- As a platform engineer, I can filter decisions by policy pack, repository, severity, and agent.
- As an auditor, I can reconstruct a session from durable decision records.

## Enterprise Challenge Solved

Activity persistence turns local pre-action decisions into searchable operational records. Security, audit, and platform teams can inspect what agents attempted, which controls fired, and which sessions generated risk.

## Next

- Add vendor-specific ITSM, ChatOps, and SIEM connector execution hooks.
- Add Azure DevOps required-check template.
