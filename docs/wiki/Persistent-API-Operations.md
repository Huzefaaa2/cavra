# Persistent API Operations

Phase 6 now includes backup, restore, and retention controls for CAVRA's persistent API stores.

## What It Provides

- Store status reporting for evidence metadata, approvals, registry, activity, repository inventory, and integration inventory.
- Checksum-backed backups for active JSON and SQLite stores.
- Restore with checksum validation and non-overwrite default behavior.
- Retention-plan artifacts in JSON and Markdown.
- Read-only API endpoints for store status and retention planning.

## CLI

```bash
cavra ops stores
cavra ops backup --output .cavra/backups/20260518
cavra ops restore .cavra/backups/20260518/manifest.json --target-dir /tmp/cavra-restore-test
cavra ops retention-plan --output .cavra/operations/retention --retention-days 2555 --legal-hold
```

Restore to a test directory before restoring to configured live paths. Live restore requires `--overwrite` when files already exist.

## API

- `GET /operations/stores`
- `GET /operations/retention-plan`

Backup and restore are CLI-only so file-system restore authority stays with operators rather than the unauthenticated demo API.

## User Stories

- As an SRE, I can back up all CAVRA API stores before migrations and releases.
- As an auditor, I can review retention, legal hold, backup, and restore-test controls.
- As a platform engineer, I can restore into a test directory and verify data before touching live stores.

## Enterprise Challenge Solved

CAVRA governance records become enterprise evidence only if they survive outages, migrations, releases, and operator mistakes. Persistent API operations make the operational data lifecycle explicit and testable.

## Next

The next recommended Phase 6 step is policy rollout drill-downs and OIDC-ready console auth/RBAC boundaries.
